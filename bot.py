import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# جلب التوكن من إعدادات رندر
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ أنا أسمعك يا أبو جميل! البوت يعمل الآن.")

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = "+".join(context.args)
    if not prompt:
        return await update.message.reply_text("أرسل وصفاً")
    url = f"https://pollinations.ai{prompt}"
    await update.message.reply_photo(photo=url, caption="تفضل صورتك!")

if __name__ == '__main__':
    if not TOKEN:
        print("خطأ: لم يتم العثور على التوكن!")
    else:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("image", image))
        print("جاري تشغيل البوت...")
        app.run_polling()
