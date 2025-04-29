from web3 import Web3
import statistics
import asyncio

class GasOptimizer:
    """Optimizes gas prices for transactions based on recent block data."""
    def __init__(self, web3: Web3):
        self.web3 = web3

    async def get_optimal_gas_price(self) -> int:
        """Calculates optimal gas price by analyzing recent blocks."""
        try:
            latest_block = self.web3.eth.get_block("latest")
            gas_prices = []
            for tx_hash in latest_block.transactions[:10]:  # Sample 10 transactions
                tx = self.web3.eth.get_transaction(tx_hash)
                gas_prices.append(tx["gasPrice"])
            
            if gas_prices:
                # Use median gas price for stability
                return int(statistics.median(gas_prices))
            return self.web3.eth.gas_price
        except Exception as e:
            logging.warning(f"Gas optimization failed: {str(e)}, using default")
            return self.web3.eth.gas_price
