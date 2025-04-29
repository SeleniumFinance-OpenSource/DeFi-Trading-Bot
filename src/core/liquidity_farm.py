from web3 import Web3

class LiquidityFarm:
    def __init__(self, config, web3: Web3):
        self.config = config
        self.web3 = web3

    def optimize_fee(self, network_name):
        # Analyze recent blocks for lowest miner fees
        latest_block = self.web3.eth.get_block("latest")
        min_gas_price = self.web3.eth.gas_price
        for tx in latest_block.transactions:
            tx_data = self.web3.eth.get_transaction(tx)
            if tx_data["gasPrice"] < min_gas_price:
                min_gas_price = tx_data["gasPrice"]
        return min_gas_price
