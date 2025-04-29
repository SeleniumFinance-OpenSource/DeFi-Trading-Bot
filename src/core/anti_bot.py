import random
import time

class AntiBot:
    def __init__(self, config):
        self.config = config

    def bypass(self, transaction):
        # Randomize transaction timing and gas to mimic human behavior
        delay = random.uniform(0.1, 0.5)
        time.sleep(delay)
        transaction["gasPrice"] = int(transaction["gasPrice"] * random.uniform(0.95, 1.05))
        return transaction
