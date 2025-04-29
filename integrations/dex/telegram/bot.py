from telegram.ext import Application, CommandHandler
from .commands import Commands

class TelegramBot:
    def __init__(self, config, bot):
        self.config = config
        self.bot = bot
        self.app = Application.builder().token(config.telegram_token).build()
        self.commands = Commands(self.bot)

    async def start(self):
        self.app.add_handler(CommandHandler("start", self.commands.start))
        self.app.add_handler(CommandHandler("stop", self.commands.stop))
        self.app.add_handler(CommandHandler("status", self.commands.status))
        # Add other command handlers
        await self.app.run_polling()

    async def stop(self):
        await self.app.stop()
