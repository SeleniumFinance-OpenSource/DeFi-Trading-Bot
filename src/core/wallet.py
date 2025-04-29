from web3 import Web3
from .config import Config

class Wallet:
    def __init__(self, config: Config):
        self.config = config
        self.web3 = None
        self.account = None
        self.connect()

    def connect(self):
        for network in self.config.networks.values():
            self.web3 = Web3(Web3.HTTPProvider(network["rpc_url"]))
            if self.web3.is_connected():
                self.account = self.web3.eth.account.from_key(self.config.private_key)
                break

    def get_balance(self, token_address=None):
        if token_address:
            # ERC-20 token balance
            contract = self.web3.eth.contract(address=token_address, abi=self.get_erc20_abi())
            return contract.functions.balanceOf(self.account.address).call()
        return self.web3.eth.get_balance(self.account.address)

    def get_erc20_abi(self):
        # Standard ERC-20 ABI (simplified)
        return [
            {"constant": True, "inputs": [{"name": "_owner", "type": "address"}],
             "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}],
             "type": "function"}
        ]
