import os
import random
import urllib.parse

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# =========================
# إعدادات
# =========================

TOKEN = os.getenv("TELEGRAM_TOKEN")

# =========================
# أوامر البوت
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🤖 أهلاً بك في بوت الذكاء الاصطناعي

الأوامر:

/image وصف الصورة

مثال:
/image futuristic city at night
"""

    await update.message.reply_text(text)


# =========================
# توليد الصور
# =========================

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):

    prompt = " ".join(context.args)

    if not prompt:
        return await update.message.reply_text(
            "⚠️ اكتب وصف بعد الأمر /image"
        )

    await update.message.reply_text(
        "🎨 جاري توليد الصورة..."
    )

    try:

        seed = random.randint(1, 999999)

        encoded_prompt = urllib.parse.quote(prompt)

        image_url = (
            f"https://image.pollinations.ai/prompt/"
            f"{encoded_prompt}"
            f"?width=1024"
            f"&height=1024"
            f"&seed={seed}"
            f"&nologo=true"
        )

        await update.message.reply_photo(
            photo=image_url,
            caption="✅ تم التوليد بنجاح"
        )

    except Exception as e:

        print(e)

        await update.message.reply_text(
            "❌ حدث خطأ أثناء التوليد"
        )


# =========================
# تشغيل البوت
# =========================

def main():

    if not TOKEN:
        print("❌ TELEGRAM_TOKEN غير موجود")
        return

    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", image))

    print("✅ Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()
