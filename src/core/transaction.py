from web3 import Web3
from .wallet import Wallet
from .validator import Validator

class Transaction:
    def __init__(self, config, wallet: Wallet, validator: Validator):
        self.config = config
        self.wallet = wallet
        self.validator = validator
        self.web3 = wallet.web3

    async def buy_token(self, token_address, amount, dex_name):
        dex = self.config.dexs.get(dex_name)
        if not dex:
            raise ValueError(f"DEX {dex_name} not configured")
        # Example: Uniswap V3 swap
        contract = self.web3.eth.contract(address=dex["router"], abi=dex["abi"])
        tx = contract.functions.swapExactETHForTokens(
            amount,
            [self.web3.to_checksum_address(self.config.networks["ethereum"]["weth"]), token_address],
            self.wallet.account.address,
            int(self.web3.eth.get_block("latest").timestamp + 60)
        ).build_transaction({
            "from": self.wallet.account.address,
            "value": amount,
            "gas": 200000,
            "gasPrice": self.web3.eth.gas_price,
            "nonce": self.web3.eth.get_transaction_count(self.wallet.account.address)
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.wallet.account.private_key)
        tx_hash = await self.validator.send_transaction(signed_tx)
        return tx_hash

    async def sell_token(self, token_address, amount, dex_name):
        # Similar logic for selling
        pass
