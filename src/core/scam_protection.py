import asyncio
from web3 import Web3

class ScamProtection:
    def __init__(self, config, transaction):
        self.config = config
        self.transaction = transaction
        self.web3 = transaction.web3
        self.threshold = 0.2  # 20% price drop

    async def monitor_token(self, token_address, dex_name):
        contract = self.web3.eth.contract(address=token_address, abi=self.get_erc20_abi())
        initial_price = self.get_token_price(token_address, dex_name)
        while True:
            current_price = self.get_token_price(token_address, dex_name)
            if current_price / initial_price < (1 - self.threshold):
                await self.transaction.sell_token(token_address, contract.functions.balanceOf(self.transaction.wallet.account.address).call(), dex_name)
                break
            await asyncio.sleep(60)

    def get_token_price(self, token_address, dex_name):
        # Fetch price from DEX (simplified)
        return 100  # Placeholder

    def get_erc20_abi(self):
        return [...]  # Same as in wallet.py
