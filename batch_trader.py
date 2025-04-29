import asyncio
from ..core.transaction import Transaction

class BatchTrader:
    """Executes batch buy/sell operations for multiple tokens."""
    def __init__(self, config, transaction: Transaction):
        self.config = config
        self.transaction = transaction

    async def execute_batch(self, operations: list[dict]):
        """Executes a batch of buy/sell operations concurrently."""
        tasks = []
        for op in operations:
            if op["type"] == "buy":
                tasks.append(self.transaction.buy_token(
                    op["token_address"], op["amount"], op["dex_name"]
                ))
            elif op["type"] == "sell":
                tasks.append(self.transaction.sell_token(
                    op["token_address"], op["amount"], op["dex_name"]
                ))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for op, result in zip(operations, results):
            if isinstance(result, Exception):
                logging.error(f"Batch operation failed for {op}: {str(result)}")
            else:
                logging.info(f"Batch operation succeeded for {op}: {result}")
        return results
