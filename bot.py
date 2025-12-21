# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

# ================= BOT =================
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
bot = telebot.TeleBot(TOKEN)

# ================= BLOCKED WORDS =================
BLOCKED_WORDS = [
    "conflict", "violence", "violent", "resistance", "occupation",
    "zion", "zionist", "jewish", "israel", "israeli",
    "attack", "kill", "bomb", "fight", "destroy",
    "missile", "rocket", "fraud", "scam"
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
        "palestine": {
            "start": "Palestine",
            "neutral": [
                "exists beyond headlines and narratives",
                "remains a reality preserved through time"
            ],
            "emotional": [
                "lives deeply in memory and belonging",
                "breathes through identity and remembrance"
            ],
            "documentary": [
                "is recorded through culture and history",
                "is documented across generations"
            ],
            "viral": [
                "is not a trend, it is a truth",
                "is a story the world keeps missing"
            ]
        }
    },
    "ar": {
        "palestine": {
            "start": "فلسطين",
            "neutral": [
                "حقيقة قائمة تتجاوز العناوين",
                "واقع محفوظ عبر الزمن"
            ],
            "emotional": [
                "تعيش في الذاكرة والانتماء",
                "تتنفس عبر الهوية والتاريخ"
            ],
            "documentary": [
                "موثقة في الثقافة والذاكرة",
                "مسجلة عبر الأجيال"
            ],
            "viral": [
                "ليست ترندًا بل حقيقة",
                "قصة يحاول العالم تجاهلها"
            ]
        }
    }
}

TONES = ["neutral", "emotional", "documentary", "viral"]

# ================= UTIL =================
def contains_blocked(text):
    t = text.lower()
    return any(w in t for w in BLOCKED_WORDS)

def generate_hook(lang, category, tone):
    data = HOOKS[lang][category]
    emoji = random.choice(EMOJIS)

    for _ in range(10):
        text = (
            f"{data['start']} {random.choice(data[tone])}\n"
            f"A story shaped by memory\n"
            f"A presence that continues"
        )

        if not contains_blocked(text):
            tags = " ".join(random.sample(HASHTAGS[category], 2))
            return f"{text}\n{tags} #Hatshepsut {emoji}"

    return None

# ================= KEYBOARDS =================
def language_menu():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🌍 English", callback_data="lang|en"),
        InlineKeyboardButton("🌍 عربي", callback_data="lang|ar")
    )
    return kb

def category_menu(lang):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🇵🇸 Palestine", callback_data=f"cat|{lang}|palestine")
    )
    return kb

def tone_menu(lang, category):
    kb = InlineKeyboardMarkup(row_width=2)
    for tone in TONES:
        kb.add(
            InlineKeyboardButton(
                tone.capitalize(),
                callback_data=f"tone|{lang}|{category}|{tone}"
            )
        )
    return kb

def again_menu(lang, category, tone):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            "🔄 Generate Again",
            callback_data=f"again|{lang}|{category}|{tone}"
        )
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Choose language / اختر اللغة:",
        reply_markup=language_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    try:
        data = call.data.split("|")

        if data[0] == "lang":
            bot.send_message(
                call.message.chat.id,
                "Choose category:",
                reply_markup=category_menu(data[1])
            )

        elif data[0] == "cat":
            bot.send_message(
                call.message.chat.id,
                "Choose tone:",
                reply_markup=tone_menu(data[1], data[2])
            )

        elif data[0] == "tone":
            _, lang, category, tone = data
            text = generate_hook(lang, category, tone)
            if text:
                bot.send_message(call.message.chat.id, text,
                                 reply_markup=again_menu(lang, category, tone))
                if CHANNEL_ID:
                    bot.send_message(CHANNEL_ID, text)

        elif data[0] == "again":
            _, lang, category, tone = data
            text = generate_hook(lang, category, tone)
            if text:
                bot.send_message(call.message.chat.id, text,
                                 reply_markup=again_menu(lang, category, tone))
                if CHANNEL_ID:
                    bot.send_message(CHANNEL_ID, text)

    except Exception as e:
        print("ERROR:", e)

# ================= RUN =================
print("Bot is running safely...")
bot.infinity_polling(skip_pending=True)
