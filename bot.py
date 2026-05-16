from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import urllib.parse
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("البوت يعمل ✅")

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)

    if not prompt:
        return await update.message.reply_text(
            "اكتب وصف بعد /image"
        )

    encoded = urllib.parse.quote(prompt)

    image_url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        "?width=1024&height=1024&nologo=true"
    )

    await update.message.reply_photo(photo=image_url)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("image", image))

print("Bot Running...")
app.run_polling()
