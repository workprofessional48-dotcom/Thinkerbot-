import os
import logging
from telegram import Update, BotCommand
from telegram.ext import Updater, CommandHandler, CallbackContext

# --------------------------
# Logging setup
# --------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --------------------------
# Environment variables
# --------------------------
TOKEN = os.environ.get("TELEGRAM_TOKEN")
APP_URL = os.environ.get("APP_URL")  # Render app URL: e.g. https://my-telegram-bot.onrender.com

if not TOKEN:
    logger.error("TELEGRAM_TOKEN environment variable not found!")
    exit(1)

if not APP_URL:
    logger.warning("APP_URL not set. Webhook may not work correctly.")

# --------------------------
# Command Handlers
# --------------------------
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(
        f"Hello {user.first_name}! 🤖\n\n"
        "I am your Telegram bot.\n"
        "Use /info to get bot details."
    )

def info(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Bot Info:\n"
        "- Author: Your Name\n"
        "- Version: 1.0\n"
        "- Platform: Python + Telegram Bot API\n"
        "- Hosting: Render\n"
    )

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/info - Bot information\n"
        "/help - This help message"
    )

# --------------------------
# Main Function
# --------------------------
def main():
    # Updater & Dispatcher
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("help", help_command))

    # Set bot commands for Telegram UI
    updater.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("info", "Get bot info"),
        BotCommand("help", "Show help message")
    ])

    # --------------------------
    # Webhook for Render deployment
    # --------------------------
    if APP_URL:
        port = int(os.environ.get("PORT", 5000))
        logger.info(f"Starting webhook at {APP_URL} on port {port}...")
        updater.start_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TOKEN,
            webhook_url=f"{APP_URL}/{TOKEN}"
        )
    else:
        # Fallback to polling if APP_URL not set
        logger.info("APP_URL not set. Starting bot in polling mode...")
        updater.start_polling()

    updater.idle()
    logger.info("Bot stopped.")

# --------------------------
# Run
# --------------------------
if __name__ == "__main__":
    main()
