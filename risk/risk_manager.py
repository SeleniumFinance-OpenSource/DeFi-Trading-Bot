import asyncio
from ..core.transaction import Transaction

class RiskManager:
    def __init__(self, config):
        self.config = config
        self.transaction = Transaction(config, config.wallet, config.validator)

    async def monitor(self):
        while True:
            for token_address in self.config.portfolio:
                await self.check_position(token_address)
            await asyncio.sleep(60)

    async def check_position(self, token_address):
        balance = self.transaction.wallet.get_balance(token_address)
        if balance > self.config.max_position_size:
            await self.transaction.sell_token(token_address, balance - self.config.max_position_size, "uniswap")
