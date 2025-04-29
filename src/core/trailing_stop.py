from ..core.transaction import Transaction

class TrailingStopStrategy:
    def __init__(self, config, transaction: Transaction):
        self.config = config
        self.transaction = transaction
        self.trailing_percent = 0.05  # 5% trailing stop

    async def execute(self, token_address, dex_name, amount):
        highest_price = self.get_token_price(token_address, dex_name)
        while True:
            current_price = self.get_token_price(token_address, dex_name)
            if current_price > highest_price:
                highest_price = current_price
            elif current_price / highest_price < (1 - self.trailing_percent):
                await self.transaction.sell_token(token_address, amount, dex_name)
                break
            await asyncio.sleep(10)

    def get_token_price(self, token_address, dex_name):
        return 100  # Placeholder
