from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random
import json
import os

# -----------------------------
# ملف حفظ المحادثات (لكل مستخدم)
# -----------------------------
CONTEXT_FILE = "user_context.json"

# تحميل البيانات الموجودة أو إنشاء ملف جديد
if os.path.exists(CONTEXT_FILE):
    with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
        user_context = json.load(f)
else:
    user_context = {}

# -----------------------------
# دوال مساعدة لحفظ واسترجاع السياق
# -----------------------------
def save_context():
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(user_context, f, ensure_ascii=False, indent=2)

def update_user_context(user_id, key, value):
    if str(user_id) not in user_context:
        user_context[str(user_id)] = {}
    user_context[str(user_id)][key] = value
    save_context()

def get_user_context(user_id, key, default=None):
    return user_context.get(str(user_id), {}).get(key, default)

# -----------------------------
# دوال البوت
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    greetings = [
        "مرحباً! 😄 أنا بوت ودود، دعنا نتحدث معًا.",
        "أهلاً! سعيد برؤيتك! 🌟",
        "هلا! تحب نتحدث قليلًا؟ 😎",
        "السلام عليكم! كيف حالك اليوم؟",
        "أهلاً بك! سعيد بوجودك هنا! 🤗"
    ]
    await update.message.reply_text(random.choice(greetings))
    update_user_context(update.message.from_user.id, "last_topic", "start")

async def reply_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.lower()

    # استرجاع آخر موضوع لتخصيص الردود
    last_topic = get_user_context(user_id, "last_topic", "general")

    # -----------------------------
    # قوائم الكلمات المفتاحية
    # -----------------------------
    greetings = ["مرحبا", "اهلا", "أهلا", "هلا", "السلام عليكم", "هاي"]
    how_are_you = ["كيفك", "كيف حالك", "شو الأخبار", "كيف الأمور", "كيف يومك"]
    thanks = ["شكرا", "شكراً", "متشكر", "متشكرين", "ألف شكر"]
    goodbye = ["مع السلامة", "وداعا", "باي", "باي باي", "أراك لاحقا"]
    jokes = ["احكي نكتة", "قول نكتة", "ضحك", "مزحة", "ضحكلي"]
    feelings = ["حزين", "مكتئب", "فرحان", "سعيد", "ممل", "زهقان", "متوتر", "متحمس", "مستغرب"]
    advice = ["نصيحة", "اعطني نصيحة", "قول نصيحة", "معلومة", "نصيحة حياتية"]

    # -----------------------------
    # الردود المتنوعة
    # -----------------------------
    greeting_replies = ["أهلاً وسهلاً! 😄", "مرحبا! كيف حالك اليوم؟", "هلا! سعيد برؤيتك! 🌟", "أهلاً! تحب نتحدث قليلًا؟"]
    how_are_you_replies = ["أنا بخير، شكرًا! وأنت؟ 😄", "تمام الحمد لله، كيف يومك؟", "كل شيء على ما يرام! وأخبارك؟"]
    thanks_replies = ["على الرحب والسعة! 😊", "العفو! أي وقت 😎", "لا شكر على واجب!"]
    goodbye_replies = ["إلى اللقاء! 👋", "باي باي! أراك لاحقًا! 😄", "اعتنِ بنفسك! 🌟"]
    jokes_replies = ["مرة واحد ذهب للفضاء وقال للقمر: أهلاً صديقي! 😂", "ليش الكمبيوتر دايمًا حزين؟ لأنه عنده مشاكل بالويندوز 😅", "مرة قطة قالت للكلب: أنا أفضل منك! والكلب قال: كل واحد عنده مزاياه 😸"]
    feelings_replies = ["أوه 😔 أتمنى أن يتحسن يومك!", "واو! سعيد بسماع ذلك 😄", "أفهم شعورك تمامًا، كل شيء سيكون أفضل!", "حاول الابتسامة قليلاً 😌"]
    advice_replies = ["حاول التركيز على الأشياء الصغيرة الجميلة 😊", "خذ نفس عميق واستمتع باللحظة!", "مهم أن تهتم بنفسك أولاً 🌟", "ابتسم! 😄 الحياة أقصر من أن نضيعها"]
    default_replies = ["ممم… أحببت ما قلته!", "هههه، أنت مضحك!", "واو! لم أفكر بذلك من قبل 😲", "أخبرني شيئًا آخر! 😁"]

    # -----------------------------
    # تحديد الرد بناءً على الكلمات أو السياق
    # -----------------------------
    if any(word in text for word in greetings):
        reply = random.choice(greeting_replies)
        update_user_context(user_id, "last_topic", "greeting")
    elif any(word in text for word in how_are_you):
        reply = random.choice(how_are_you_replies)
        update_user_context(user_id, "last_topic", "how_are_you")
    elif any(word in text for word in thanks):
        reply = random.choice(thanks_replies)
        update_user_context(user_id, "last_topic", "thanks")
    elif any(word in text for word in goodbye):
        reply = random.choice(goodbye_replies)
        update_user_context(user_id, "last_topic", "goodbye")
    elif any(word in text for word in jokes):
        reply = random.choice(jokes_replies)
        update_user_context(user_id, "last_topic", "joke")
    elif any(word in text for word in feelings):
        reply = random.choice(feelings_replies)
        update_user_context(user_id, "last_topic", "feelings")
    elif any(word in text for word in advice):
        reply = random.choice(advice_replies)
        update_user_context(user_id, "last_topic", "advice")
    else:
        # الردود تعتمد على آخر موضوع لتكون أكثر شخصية
        if last_topic == "how_are_you":
            reply = "تمام! 😄 وأنت؟ حدثني عن يومك!"
        elif last_topic == "feelings":
            reply = "أتفهم شعورك… هل تريد أن نحكي أكثر؟"
        else:
            reply = random.choice(default_replies)
        update_user_context(user_id, "last_topic", "general")

    await update.message.reply_text(reply)

# -----------------------------
# إعداد البوت وتشغيله
# -----------------------------
if __name__ == "__main__":
    BOT_TOKEN = "حط توكــنــــك هنااااااااا"  

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_messages))

    print("البوت الذكي يعمل الآن... 🤖💬")
    app.run_polling()
