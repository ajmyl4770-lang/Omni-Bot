import os, requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- سيرفر البقاء ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- الإعدادات ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# --- الأوامر ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 أهلاً أبو جميل! أنا بوت الذكاء الاصطناعي السريع.\nاستخدم: /image [وصف بالانجليزي]")

async def image_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt: return await update.message.reply_text("أرسل وصفاً، مثال: /image lion")
    
    # رسالة انتظار
    msg = await update.message.reply_text("🎨 جاري ابتكار صورتك... ثواني")
    
    # توليد رابط الصورة المباشر
    import random
    seed = random.randint(1, 999999)
    # استخدام رابط يحول الوصف لصورة مباشرة
    image_url = f"https://pollinations.ai{requests.utils.quote(prompt)}?width=1024&height=1024&seed={seed}"
    
    try:
        # إرسال الصورة كـ Photo مباشرة عبر الرابط
        await update.message.reply_photo(photo=image_url, caption=f"✅ تم التوليد لـ: {prompt[:50]}...")
        await msg.delete() # حذف رسالة "جاري الابتكار"
    except:
        # إذا فشل كصورة، يرسلها كرابط يفتح في المتصفح
        await update.message.reply_text(f"🔗 تعذر عرضها هنا، شاهدها عبر الرابط:\n{image_url}")

if __name__ == '__main__':
    keep_alive()
    Application.builder().token(TELEGRAM_TOKEN).build().add_handler(CommandHandler("start", start)).add_handler(CommandHandler("image", image_cmd)).run_polling()
