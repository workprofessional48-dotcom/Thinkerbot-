import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Telegram Bot Token (Render ke env variable se lega)
TOKEN = os.getenv("8232368560:AAHd8IOXBBc_siTyi3NvUyxnlnN7ze-cPSQ")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! ✅ Your bot is live on Render.")

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/start - Start the bot\n/help - Help menu")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is polling... 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
