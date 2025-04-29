import asyncio
from web3 import Web3

class Validator:
    def __init__(self, config):
        self.config = config
        self.web3 = None
        self.connect()

    def connect(self):
        for network in self.config.networks.values():
            self.web3 = Web3(Web3.HTTPProvider(network["rpc_url"]))
            if self.web3.is_connected():
                break

    async def send_transaction(self, signed_tx):
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = await self.wait_for_receipt(tx_hash)
        return receipt

    async def wait_for_receipt(self, tx_hash):
        while True:
            try:
                receipt = self.web3.eth.get_transaction_receipt(tx_hash)
                if receipt:
                    return receipt
            except:
                await asyncio.sleep(1)
