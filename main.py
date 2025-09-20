import os
import logging
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
TOKEN = os.environ.get("TELEGRAM_TOKEN")
APP_URL = os.environ.get("APP_URL")  # Optional

if not TOKEN:
    logger.error("TELEGRAM_TOKEN environment variable not found!")
    exit(1)
else:
    logger.info("Telegram bot token found ✅")

if not APP_URL:
    logger.warning("APP_URL not set. Bot will use polling mode.")

# ---------------- Command Handlers ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! 🤖\nBot is active.\nUse /info for details."
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot Info:\n"
        "- Author: Your Name\n"
        "- Version: 1.0\n"
        "- Platform: Python + Telegram Bot API\n"
        "- Hosting: Render or Local"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n/start - Start the bot\n/info - Bot info\n/help - This message"
    )

# ---------------- Main ----------------
def main():
    # Create Application
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("help", help_command))

    # Set bot commands in Telegram UI
    app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("info", "Get bot info"),
        BotCommand("help", "Show help message")
    ])

    # Start bot
    if APP_URL:
        port = int(os.environ.get("PORT", 5000))
        logger.info(f"Starting webhook at {APP_URL} on port {port}...")
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TOKEN,
            webhook_url=f"{APP_URL}/{TOKEN}"
        )
    else:
        logger.info("APP_URL not set. Starting polling mode...")
        app.run_polling()

# ---------------- Run ----------------
if __name__ == "__main__":
    main()
