from ..core.transaction import Transaction

class BuyDipStrategy:
    def __init__(self, config, transaction: Transaction):
        self.config = config
        self.transaction = transaction
        self.dip_threshold = 0.1  # 10% dip

    async def execute(self, token_address, dex_name, amount):
        initial_price = self.get_token_price(token_address, dex_name)
        while True:
            current_price = self.get_token_price(token_address, dex_name)
            if current_price / initial_price < (1 - self.dip_threshold):
                await self.transaction.buy_token(token_address, amount, dex_name)
                break
            await asyncio.sleep(60)

    def get_token_price(self, token_address, dex_name):
        return 100  # Placeholder
