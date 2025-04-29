from abc import ABC, abstractmethod

class DEXBase(ABC):
    def __init__(self, config, network):
        self.config = config
        self.network = network
        self.web3 = network.web3

    @abstractmethod
    async def get_price(self, token_address):
        pass
