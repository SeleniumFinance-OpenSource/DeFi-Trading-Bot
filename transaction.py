import asyncio
from web3 import Web3
from .wallet import Wallet
from .validator import Validator
from .gas_optimizer import GasOptimizer
import pyo3_defi_selenium_bot  # Rust bindings

class Transaction:
    """Manages buy and sell transactions with optimized gas and anti-bot measures."""
    def __init__(self, config, wallet: Wallet, validator: Validator):
        self.config = config
        self.wallet = wallet
        self.validator = validator
        self.web3 = wallet.web3
        self.gas_optimizer = GasOptimizer(self.web3)
        self.rust_signer = pyo3_defi_selenium_bot.TransactionSigner()

    async def buy_token(self, token_address: str, amount: int, dex_name: str) -> str:
        """Executes a buy transaction for a token on the specified DEX."""
        try:
            dex = self.config.dexs.get(dex_name)
            if not dex:
                raise ValueError(f"DEX {dex_name} not configured")

            contract = self.web3.eth.contract(address=dex["router"], abi=dex["abi"])
            gas_price = await self.gas_optimizer.get_optimal_gas_price()
            tx = contract.functions.swapExactETHForTokens(
                amount,
                [self.web3.to_checksum_address(self.config.networks["ethereum"]["weth"]), token_address],
                self.wallet.account.address,
                int(self.web3.eth.get_block("latest").timestamp + 60)
            ).build_transaction({
                "from": self.wallet.account.address,
                "value": amount,
                "gas": 200000,
                "gasPrice": gas_price,
                "nonce": self.web3.eth.get_transaction_count(self.wallet.account.address)
            })

            # Apply anti-bot bypass via Rust
            tx = self.rust_signer.apply_anti_bot_bypass(tx)
            signed_tx = self.rust_signer.sign_transaction(
                tx, self.wallet.account.private_key
            )
            tx_hash = await self.validator.send_transaction(signed_tx)
            return tx_hash.hex()
        except Exception as e:
            logging.error(f"Buy transaction failed: {str(e)}")
            raise

    async def sell_token(self, token_address: str, amount: int, dex_name: str) -> str:
        """Executes a sell transaction for a token on the specified DEX."""
        try:
            dex = self.config.dexs.get(dex_name)
            if not dex:
                raise ValueError(f"DEX {dex_name} not configured")

            token_contract = self.web3.eth.contract(address=token_address, abi=self.get_erc20_abi())
            approve_tx = token_contract.functions.approve(
                dex["router"], amount
            ).build_transaction({
                "from": self.wallet.account.address,
                "gas": 100000,
                "gasPrice": await self.gas_optimizer.get_optimal_gas_price(),
                "nonce": self.web3.eth.get_transaction_count(self.wallet.account.address)
            })

            # Sign and send approval transaction
            signed_approve = self.rust_signer.sign_transaction(
                approve_tx, self.wallet.account.private_key
            )
            await self.validator.send_transaction(signed_approve)

            # Build swap transaction
            swap_tx = self.web3.eth.contract(address=dex["router"], abi=dex["abi"]).functions.swapExactTokensForETH(
                amount,
                0,  # Min amount out
                [token_address, self.web3.to_checksum_address(self.config.networks["ethereum"]["weth"])],
                self.wallet.account.address,
                int(self.web3.eth.get_block("latest").timestamp + 60)
            ).build_transaction({
                "from": self.wallet.account.address,
                "gas": 200000,
                "gasPrice": await self.gas_optimizer.get_optimal_gas_price(),
                "nonce": self.web3.eth.get_transaction_count(self.wallet.account.address) + 1
            })

            signed_swap = self.rust_signer.sign_transaction(
                swap_tx, self.wallet.account.private_key
            )
            tx_hash = await self.validator.send_transaction(signed_swap)
            return tx_hash.hex()
        except Exception as e:
            logging.error(f"Sell transaction failed: {str(e)}")
            raise

    def get_erc20_abi(self):
        """Returns standard ERC-20 ABI."""
        return [...]  # Simplified for brevity
