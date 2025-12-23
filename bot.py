# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= BLOCKED WORDS =================
BLOCKED = [
    "conflict","violence","violent","resistance","occupation",
    "zion","zionist","jewish","israel","israeli",
    "attack","kill","bomb","destroy","rocket","missile",
    "fraud","scam"
]

def safe(text):
    t = text.lower()
    return not any(w in t for w in BLOCKED)

# ================= EMOJIS =================
EMOJIS = ["🇵🇸","🕊️","📜","⏳","🗺️","✨"]

# ================= CATEGORIES =================
CATEGORIES = {
    "palestine": "🇵🇸 فلسطين",
    "gaza": "🔥 غزة",
    "maps": "🗺️ خرائط فلسطين",
    "memory": "📜 الذاكرة الفلسطينية",
    "nakba": "🕊️ النكبة وأحداثها"
}

# ================= OPENINGS (SMART) =================
OPENINGS = {
    "maps": [
        "This is a historical map of Palestine before 1948",
        "This historical map shows Palestine prior to 1948",
        "A historical map documenting Palestine before 1948"
    ],
    "palestine": [
        "Palestine has always existed as a living identity",
        "Palestine remains present beyond time",
        "Palestine lives through memory and place"
    ],
    "gaza": [
        "Gaza represents a continuous Palestinian presence",
        "Gaza reflects daily Palestinian life",
        "Gaza holds stories shaped by time"
    ],
    "memory": [
        "Palestinian memory carries identity forward",
        "This memory passes quietly through generations",
        "This history lives without needing permission"
    ],
    "nakba": [
        "The Nakba reshaped Palestinian daily life",
        "The Nakba marked a turning point in history",
        "That moment in history changed lives forever"
    ]
}

# ================= DEVELOPMENT LAYERS =================
MIDDLES = [
    "not as a claim, but as a fact",
    "through names, places, and remembrance",
    "without needing explanation",
    "beyond narratives and timelines"
]

ENDINGS = [
    "remaining undeniably Palestinian",
    "rooted in Palestinian identity",
    "connected to Palestine forever",
    "preserved as Palestinian memory"
]

# ================= HASHTAGS =================
HASHTAGS = {
    "palestine": "#Palestine #PalestinianIdentity #Hatshepsut",
    "gaza": "#Gaza #PalestinianMemory #Hatshepsut",
    "maps": "#HistoricalMap #Palestine #Hatshepsut",
    "memory": "#Memory #PalestinianHistory #Hatshepsut",
    "nakba": "#Nakba #PalestinianMemory #Hatshepsut"
}

# ================= HOOK ENGINE =================
def generate_hook(category):
    for _ in range(20):
        o = random.choice(OPENINGS[category])
        m = random.choice(MIDDLES)
        e = random.choice(ENDINGS)
        emoji = random.choice(EMOJIS)

        text = (
            f"{o},\n"
            f"{m},\n"
            f"{e}. {emoji}\n\n"
            f"{HASHTAGS[category]}"
        )

        if safe(text):
            return f"<code>{text}</code>"

    return "<code>Could not generate safe content.</code>"

# ================= KEYBOARDS =================
def categories_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    for k,v in CATEGORIES.items():
        kb.add(InlineKeyboardButton(v, callback_data=f"cat|{k}"))
    return kb

def again_kb(category):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{category}")
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(
        m.chat.id,
        "🇵🇸 اختار القسم:",
        reply_markup=categories_kb()
    )

@bot.callback_query_handler(func=lambda c: True)
def handle(c):
    data = c.data.split("|")

    if data[0] == "cat":
        category = data[1]
        text = generate_hook(category)
        bot.send_message(
            c.message.chat.id,
            text,
            reply_markup=again_kb(category)
        )

    elif data[0] == "again":
        category = data[1]
        text = generate_hook(category)
        bot.send_message(
            c.message.chat.id,
            text,
            reply_markup=again_kb(category)
        )

# ================= RUN =================
print("🇵🇸 Smart Palestinian Hook Engine running...")
bot.infinity_polling(skip_pending=True)
