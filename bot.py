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

# ================= USER VARIATION LOCK =================
USER_HISTORY = {}

def seen_before(uid, key):
    if uid not in USER_HISTORY:
        USER_HISTORY[uid] = set()
    return key in USER_HISTORY[uid]

def remember(uid, key):
    USER_HISTORY[uid].add(key)

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

# ================= OPENING WORD CONTROL =================
OPENINGS = {
    "maps": [
        "This is a historical map of Palestine before 1948",
        "A documented historical map of Palestine prior to 1948",
        "This historical map records Palestine as it existed before 1948"
    ],
    "palestine": [
        "Palestine exists as a continuous identity",
        "Palestine lives beyond time and narration",
        "Palestine remains present through memory and place"
    ],
    "gaza": [
        "Gaza represents daily Palestinian presence",
        "Gaza carries Palestinian identity forward",
        "Gaza reflects lived Palestinian reality"
    ],
    "memory": [
        "Palestinian memory moves quietly through generations",
        "Memory preserves Palestinian identity without interruption",
        "This memory carries Palestine forward"
    ],
    "nakba": [
        "The Nakba reshaped Palestinian daily life",
        "The Nakba marked a historical turning point",
        "That moment in history altered Palestinian lives"
    ]
}

# ================= MOOD PRESETS =================
MOODS = {
    "🧠 هادئ توثيقي": {
        "middles": [
            "documented carefully without commentary",
            "recorded through names, places, and memory",
            "preserved without noise or exaggeration"
        ],
        "endings": [
            "as part of Palestinian historical continuity",
            "within Palestinian collective memory",
            "as a documented Palestinian reality"
        ]
    },
    "⚡ مكثف عميق": {
        "middles": [
            "beyond headlines and explanations",
            "without needing validation",
            "outside imposed narratives"
        ],
        "endings": [
            "remaining undeniably Palestinian",
            "rooted deeply in Palestinian identity",
            "connected permanently to Palestine"
        ]
    },
    "✨ تأملي إنساني": {
        "middles": [
            "through quiet remembrance",
            "through lived experience",
            "through memory carried forward"
        ],
        "endings": [
            "held gently within Palestinian memory",
            "remembered without permission",
            "kept alive through identity"
        ]
    }
}

# ================= HASHTAGS =================
HASHTAGS = {
    "palestine": "#Palestine #PalestinianIdentity #Hatshepsut",
    "gaza": "#Gaza #PalestinianMemory #Hatshepsut",
    "maps": "#HistoricalMap #Palestine #Hatshepsut",
    "memory": "#PalestinianMemory #History #Hatshepsut",
    "nakba": "#Nakba #PalestinianMemory #Hatshepsut"
}

# ================= HOOK ENGINE =================
def generate_hook(uid, category, mood):
    for _ in range(40):
        opening = random.choice(OPENINGS[category])
        middle = random.choice(MOODS[mood]["middles"])
        ending = random.choice(MOODS[mood]["endings"])
        emoji = random.choice(EMOJIS)

        key = f"{category}|{mood}|{opening}|{middle}|{ending}"
        if seen_before(uid, key):
            continue

        text = (
            f"{opening},\n"
            f"{middle},\n"
            f"{ending}. {emoji}\n\n"
            f"{HASHTAGS[category]}"
        )

        if safe(text):
            remember(uid, key)
            return f"<code>{text}</code>"

    return "<code>No new safe formulation could be generated.</code>"

# ================= KEYBOARDS =================
def categories_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    for k,v in CATEGORIES.items():
        kb.add(InlineKeyboardButton(v, callback_data=f"cat|{k}"))
    return kb

def mood_kb(category):
    kb = InlineKeyboardMarkup(row_width=1)
    for m in MOODS.keys():
        kb.add(InlineKeyboardButton(m, callback_data=f"mood|{category}|{m}"))
    return kb

def again_kb(category, mood):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{category}|{mood}")
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
    uid = c.from_user.id

    if data[0] == "cat":
        bot.send_message(
            c.message.chat.id,
            "🎭 اختار النبرة:",
            reply_markup=mood_kb(data[1])
        )

    elif data[0] == "mood":
        _, category, mood = data
        text = generate_hook(uid, category, mood)
        bot.send_message(
            c.message.chat.id,
            text,
            reply_markup=again_kb(category, mood)
        )

    elif data[0] == "again":
        _, category, mood = data
        text = generate_hook(uid, category, mood)
        bot.send_message(
            c.message.chat.id,
            text,
            reply_markup=again_kb(category, mood)
        )

# ================= RUN =================
print("🇵🇸 Advanced Palestinian Hook Engine running...")
bot.infinity_polling(skip_pending=True)
