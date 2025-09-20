import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Render ka URL (env me daloge)

app = Flask(__name__)

# Telegram application
application = Application.builder().token(TOKEN).build()

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello 👋, I am alive on Render using Webhook!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commands:\n/start - start the bot\n/help - help menu")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Flask route for webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Home route (optional)
@app.route("/")
def home():
    return "Bot is running ✅"

if __name__ == "__main__":
    # Set webhook
    import asyncio
    async def set_webhook():
        await application.bot.set_webhook(f"{APP_URL}/{TOKEN}")

    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
