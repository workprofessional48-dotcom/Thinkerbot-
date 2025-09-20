import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Environment variable se token aur URL lena
TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # e.g. https://thinkerbot-81.onrender.com

# /start command ka handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Bot is live on Render!")

def main():
    # Bot app build karna
    app = Application.builder().token(TOKEN).build()

    # /start handler add karna
    app.add_handler(CommandHandler("start", start))

    # Webhook setup for Render
    port = int(os.environ.get("PORT", 8443))
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"{APP_URL}/{TOKEN}"
    )

if __name__ == "__main__":
    main()
