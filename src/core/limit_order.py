from ..core.transaction import Transaction

class LimitOrderStrategy:
    def __init__(self, config, transaction: Transaction):
        self.config = config
        self.transaction = transaction

    async def place_limit_order(self, token_address, dex_name, price, amount, side="buy"):
        current_price = self.get_token_price(token_address, dex_name)
        while True:
            if side == "buy" and current_price <= price:
                await self.transaction.buy_token(token_address, amount, dex_name)
                break
            elif side == "sell" and current_price >= price:
                await self.transaction.sell_token(token_address, amount, dex_name)
                break
            await asyncio.sleep(10)

    def get_token_price(self, token_address, dex_name):
        return 100  # Placeholder
