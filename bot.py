import requests
import io
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import os
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")


HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# روابط النماذج (أفضل المتاح مجاناً في 2026)
MODELS = {
    "image": "https://huggingface.co",
    "video": "https://huggingface.co", # نموذج فيديو سريع
    "music": "https://huggingface.co" # نموذج موسيقى
}

# دالة عامة للتعامل مع API هجينغ فيس
def query_hf(prompt, model_url):
    response = requests.post(model_url, headers=HEADERS, json={"inputs": prompt})
    if response.status_code != 200:
        return None
    return response.content

# --- أوامر البوت ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🤖 أهلاً بك في بوت الذكاء الاصطناعي الشامل!\n\n"
        "استخدم الأوامر التالية:\n"
        "🎨 /image [وصف الصورة]\n"
        "🎬 /video [وصف الفيديو]\n"
        "🎵 /music [وصف الموسيقى]\n"
    )
    await update.message.reply_text(welcome_text)

# 1. توليد الصور
async def image_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt: return await update.message.reply_text("يرجى كتابة وصف بعد الأمر.")
    
    await update.message.reply_text("🎨 جاري رسم صورتك...")
    result = query_hf(prompt, MODELS["image"])
    if result:
        await update.message.reply_photo(photo=io.BytesIO(result))
    else:
        await update.message.reply_text("⚠️ السيرفر مشغول حالياً، حاول لاحقاً.")

# 2. توليد الموسيقى
async def music_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt: return await update.message.reply_text("يرجى كتابة وصف للموسيقى.")
    
    await update.message.reply_text("🎵 جاري تأليف الموسيقى...")
    result = query_hf(prompt, MODELS["music"])
    if result:
        await update.message.reply_audio(audio=io.BytesIO(result), filename="music.mp3")
    else:
        await update.message.reply_text("⚠️ فشل توليد الموسيقى.")

# 3. توليد الفيديو (الأفلام القصيرة)
async def video_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt: return await update.message.reply_text("يرجى كتابة وصف للفيديو.")
    
    await update.message.reply_text("🎬 جاري إنتاج الفيديو (قد يستغرق دقيقة)...")
    result = query_hf(prompt, MODELS["video"])
    if result:
        await update.message.reply_video(video=io.BytesIO(result))
    else:
        await update.message.reply_text("⚠️ سيرفر الفيديو قيد المعالجة، كرر المحاولة.")

# --- تشغيل البوت ---
if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", image_cmd))
    app.add_handler(CommandHandler("music", music_cmd))
    app.add_handler(CommandHandler("video", video_cmd))
    
    print("البوت الشامل يعمل الآن...")
    app.run_polling()
