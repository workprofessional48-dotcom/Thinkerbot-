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
# Load environment variables safely
# --------------------------
TOKEN = os.environ.get("TELEGRAM_TOKEN")
APP_URL = os.environ.get("APP_URL")  # Optional for webhook

if not TOKEN:
    logger.error(
        "TELEGRAM_TOKEN environment variable not found! "
        "Please set your bot token correctly."
    )
    exit(1)
else:
    logger.info("Telegram bot token found ✅")

if not APP_URL:
    logger.warning(
        "APP_URL not set. Bot will fallback to polling mode."
    )

# --------------------------
# Command Handlers
# --------------------------
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(
        f"Hello {user.first_name}! 🤖\n"
        "Bot is active and ready.\n"
        "Use /info to know more about this bot."
    )

def info(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Bot Information:\n"
        "- Author: Your Name\n"
        "- Version: 1.0\n"
        "- Platform: Python + Telegram Bot API\n"
        "- Hosting: Render or Local\n"
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
    # Create Updater and Dispatcher
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("help", help_command))

    # Set bot commands in Telegram UI
    updater.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("info", "Get bot info"),
        BotCommand("help", "Show help message")
    ])

    # --------------------------
    # Webhook (Render) or Polling (fallback)
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
        logger.info("APP_URL not set. Starting bot in polling mode...")
        updater.start_polling()

    logger.info("Bot is running ✅")
    updater.idle()

# --------------------------
# Run
# --------------------------
if __name__ == "__main__":
    main()
