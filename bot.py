# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

# ================= BOT =================
TOKEN = os.getenv("BOT_TOKEN")  # ضع توكن البوت هنا أو في Environment Variable
bot = telebot.TeleBot(TOKEN)

# ================= BLOCKED WORDS =================
BLOCKED_WORDS = [
    "conflict", "violence", "violent", "resistance", "occupation",
    "zion", "zionist", "jewish", "israel", "israeli",
    "attack", "kill", "bomb", "fight", "destroy",
    "missile", "rocket", "fraud", "scam", "steadfastness"
]

# ================= EMOJIS =================
EMOJIS = ["🇵🇸", "🕊️", "🌿", "📜", "🗺️", "⏳", "✨"]

# ================= HASHTAGS =================
HASHTAGS = {
    "palestine": ["#Palestine", "#PalestinianIdentity", "#FreePalestine"],
    "gaza": ["#Gaza", "#GazaStories", "#HumanStories"],
    "maps": ["#HistoricalMaps", "#PalestineMaps", "#Cartography"],
    "nakba": ["#Nakba", "#HistoricalMemory", "#CollectiveMemory"]
}

# ================= HOOKS =================
HOOKS = {
    "en": {
        "palestine": ["exists beyond headlines and narratives",
                      "remains a reality preserved through time",
                      "lives deeply in memory and belonging"],
        "gaza": ["continues through patience and endurance",
                 "exists beyond daily headlines",
                 "carries strength through hardship"],
        "maps": ["preserves geography drawn long ago",
                 "documents land before modern narratives",
                 "holds stories beyond ink and paper"],
        "nakba": ["remains a defining historical moment",
                  "left an enduring impact on identity",
                  "lives quietly within collective memory"]
    },
    "ar": {
        "palestine": ["حقيقة قائمة تتجاوز العناوين",
                      "واقع محفوظ عبر الزمن",
                      "تعيش في الذاكرة والانتماء"],
        "gaza": ["تستمر بالصبر والتحمل",
                 "وجودها يتجاوز العناوين اليومية",
                 "تحمل القوة رغم الصعاب"],
        "maps": ["تحفظ الجغرافيا المرسومة منذ زمن",
                 "توثق الأرض قبل الروايات الحديثة",
                 "تحوي قصصاً تتجاوز الحبر والورق"],
        "nakba": ["تظل لحظة تاريخية محددة",
                  "ترك تأثيرًا دائمًا على الهوية",
                  "تعيش بهدوء في الذاكرة الجمعية"]
    }
}

TONES = ["neutral", "emotional", "documentary", "viral"]

# ================= UTIL =================
def contains_blocked(text):
    t = text.lower()
    return any(w in t for w in BLOCKED_WORDS)

def generate_hook(lang, category):
    for _ in range(10):
        text = random.choice(HOOKS[lang][category])
        if not contains_blocked(text):
            emoji = random.choice(EMOJIS)
            hashtags = " ".join(random.sample(HASHTAGS[category], 2)) + " #Hatshepsut"
            return f"{category.capitalize()} {text}\n{hashtags} {emoji}"
    return "Could not generate safe content."

# ================= KEYBOARDS =================
def category_menu(lang):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🇵🇸 Palestine", callback_data=f"cat|{lang}|palestine"),
        InlineKeyboardButton("🔥 Gaza", callback_data=f"cat|{lang}|gaza"),
        InlineKeyboardButton("🗺️ Historical Maps", callback_data=f"cat|{lang}|maps"),
        InlineKeyboardButton("🕊️ Nakba", callback_data=f"cat|{lang}|nakba"),
        InlineKeyboardButton("🎲 Surprise Me", callback_data=f"surprise|{lang}")
    )
    return kb

def action_menu(lang, category, text):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{lang}|{category}"),
        InlineKeyboardButton("📋 Copy", switch_inline_query_current_chat=text)
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Choose language / اختر اللغة:",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("🌍 English", callback_data="lang|en"),
            InlineKeyboardButton("🌍 عربي", callback_data="lang|ar")
        )
    )

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    try:
        data = call.data.split("|")

        if data[0] == "lang":
            lang = data[1]
            bot.send_message(
                call.message.chat.id,
                "Choose category:",
                reply_markup=category_menu(lang)
            )

        elif data[0] == "cat":
            lang, category = data[1], data[2]
            text = generate_hook(lang, category)
            bot.send_message(
                call.message.chat.id,
                text,
                reply_markup=action_menu(lang, category, text)
            )

        elif data[0] == "again":
            lang, category = data[1], data[2]
            text = generate_hook(lang, category)
            bot.send_message(
                call.message.chat.id,
                text,
                reply_markup=action_menu(lang, category, text)
            )

        elif data[0] == "surprise":
            lang = data[1]
            category = random.choice(list(HOOKS[lang].keys()))
            text = generate_hook(lang, category)
            bot.send_message(
                call.message.chat.id,
                text,
                reply_markup=action_menu(lang, category, text)
            )

    except Exception as e:
        print("ERROR:", e)
        bot.send_message(call.message.chat.id, "An error occurred, please try again.")

# ================= RUN =================
print("Bot is running smoothly...")
bot.infinity_polling(skip_pending=True)
