import telegram
import re

class TelegramMonitor:
    def __init__(self, config, transaction):
        self.config = config
        self.transaction = transaction
        self.bot = telegram.Bot(token=config.telegram_token)

    async def monitor_channels(self, channels):
        async for update in self.bot.get_updates():
            if update.message and update.message.chat.username in channels:
                contract_address = self.extract_contract_address(update.message.text)
                if contract_address:
                    await self.transaction.buy_token(contract_address, self.config.default_amount, "uniswap")

    def extract_contract_address(self, text):
        # Regex to find Ethereum-like contract addresses
        pattern = r"0x[a-fA-F0-9]{40}"
        match = re.search(pattern, text)
        return match.group(0) if match else None
