from telegram import Update
from telegram.ext import ContextTypes

class Commands:
    def __init__(self, bot):
        self.bot = bot

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Starting DeFi Bot...")
        await self.bot.start()

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Stopping DeFi Bot...")
        await self.bot.stop()

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Bot is running" if self.bot.running else "Bot is stopped")
