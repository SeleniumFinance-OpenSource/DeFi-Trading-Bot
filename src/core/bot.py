import asyncio
import logging
from .config import Config
from .wallet import Wallet
from .transaction import Transaction
from .validator import Validator
from ..strategies.strategy_manager import StrategyManager
from ..integrations.telegram.bot import TelegramBot
from ..risk.risk_manager import RiskManager

class DeFiBot:
    def __init__(self):
        self.config = Config()
        self.wallet = Wallet(self.config)
        self.validator = Validator(self.config)
        self.transaction = Transaction(self.config, self.wallet, self.validator)
        self.strategy_manager = StrategyManager(self.config, self.transaction)
        self.risk_manager = RiskManager(self.config)
        self.telegram_bot = TelegramBot(self.config, self)
        self.running = False

    async def start(self):
        logging.info("Starting DeFi Selenium Bot...")
        self.running = True
        await asyncio.gather(
            self.strategy_manager.run(),
            self.telegram_bot.start(),
            self.risk_manager.monitor()
        )

    async def stop(self):
        logging.info("Stopping DeFi Selenium Bot...")
        self.running = False
        await self.telegram_bot.stop()

if __name__ == "__main__":
    import platform
    bot = DeFiBot()
    if platform.system() == "Emscripten":
        asyncio.ensure_future(bot.start())
    else:
        asyncio.run(bot.start())
