import os
import io
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- سيرفر وهمي لإبقاء البوت مستيقظاً ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- الإعدادات ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# --- وظائف التوليد ---

async def image_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt: 
        return await update.message.reply_text("يرجى كتابة وصف للصورة.")
    
    await update.message.reply_text("🎨 جاري التصميم الفوري... انتظر ثواني")
    
    try:
        import random
        seed = random.randint(1, 1000000)
        # الرابط المباشر للصورة
        image_url = f"https://pollinations.ai{requests.utils.quote(prompt)}?width=1024&height=1024&nologo=true&seed={seed}"
        
        # تحميل الصورة من الرابط أولاً للتأكد من سلامتها
        img_response = requests.get(image_url, timeout=30)
        if img_response.status_code == 200:
            # إرسال الصورة كملف بايتات (Buffer) لضمان وصولها لتيليجرام
            await update.message.reply_photo(photo=io.BytesIO(img_response.content), caption="✅ تم توليد صورتك بنجاح!")
        else:
            await update.message.reply_text("❌ فشل السيرفر في توليد الصورة، جرب وصفاً أقصر.")
            
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("❌ حدث خطأ في الاتصال، حاول مرة أخرى.")


# 2. توليد فيديو وموسيقى (Hugging Face)
def query_hf(prompt, model_url):
    try:
        response = requests.post(model_url, headers=HEADERS, json={"inputs": prompt}, timeout=150)
        return response.content if response.status_code == 200 else None
    except: return None

# --- أوامر البوت ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 بوت الذكاء الاصطناعي الخارق جاهز!\n\n/image [وصف]\n/video [وصف]\n/music [وصف]")

async def image_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt: 
        return await update.message.reply_text("اكتب وصفاً للصورة بعد الأمر، مثال:\n/image cat in space")
    
    await update.message.reply_text("🎨 جاري التصميم الفوري...")
    
    try:
        # توليد رابط الصورة مباشرة مع كود عشوائي لضمان التجديد في كل مرة
        import random
        seed = random.randint(1, 1000000)
        image_url = f"https://pollinations.ai{requests.utils.quote(prompt)}?width=1024&height=1024&nologo=true&seed={seed}"
        
        # إرسال الصورة عن طريق الرابط مباشرة (هذه الطريقة لا تفشل أبداً)
        await update.message.reply_photo(photo=image_url, caption="✅ تم التوليد بنجاح!")
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ غير متوقع، حاول مجدداً.")


async def video_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt: return await update.message.reply_text("اكتب وصفاً للفيديو")
    await update.message.reply_text("🎬 جاري إنتاج الفيديو (قد يستغرق وقتاً)...")
    # تم تبديل النموذج لواحد أكثر استقراراً
    result = query_hf(prompt, "https://huggingface.co")
    if result: await update.message.reply_video(video=io.BytesIO(result))
    else: await update.message.reply_text("⚠️ السيرفر مشغول، جرب المحاولة بعد قليل أو غير الوصف.")

async def music_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt: return await update.message.reply_text("اكتب وصفاً للموسيقى")
    await update.message.reply_text("🎵 جاري تأليف المقطع...")
    result = query_hf(prompt, "https://huggingface.co")
    if result: await update.message.reply_audio(audio=io.BytesIO(result), filename="music.mp3")
    else: await update.message.reply_text("❌ السيرفر لا يستجيب حالياً.")

# --- التشغيل ---
if __name__ == '__main__':
    keep_alive()
    bot = Application.builder().token(TELEGRAM_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("image", image_cmd))
    bot.add_handler(CommandHandler("video", video_cmd))
    bot.add_handler(CommandHandler("music", music_cmd))
    print("البوت يعمل الآن بأقصى سرعة...")
    bot.run_polling()
