# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import time

# ================= BOT INIT =================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= SAFETY FILTER =================
BLOCKED = {
    "violence","violent","attack","kill","bomb","destroy",
    "weapon","missile","rocket","war","fight","combat"
}

def safe(txt: str) -> bool:
    t = txt.lower()
    return not any(w in t for w in BLOCKED)

# ================= CATEGORIES =================
CATEGORIES = {
    "maps": "🗺️ الخرائط التاريخية",
    "palestine": "🇵🇸 فلسطين",
    "gaza": "🏙️ غزة",
    "nakba": "📜 النكبة"
}

# ================= CORE LANGUAGE ENGINE =================

SUBJECTS = {
    "maps": [
        "This historical map",
        "This preserved cartographic record",
        "This officially archived map",
        "This verified geographic document",
        "This original historical reference"
    ],
    "palestine": [
        "Palestine",
        "The land of Palestine",
        "Historic Palestine",
        "The Palestinian geographical identity",
        "The Palestinian historical presence"
    ],
    "gaza": [
        "Gaza",
        "The city of Gaza",
        "Gaza Strip",
        "Historic Gaza",
        "The Gaza region"
    ],
    "nakba": [
        "The Nakba",
        "The 1948 Nakba",
        "This historical catastrophe",
        "The Nakba event",
        "The Palestinian Nakba"
    ]
}

ACTIONS = [
    "is documented as",
    "is recorded as",
    "is clearly identified as",
    "is historically recognized as",
    "is formally preserved as",
    "is consistently referenced as",
    "is undeniably established as"
]

QUALIFIERS = [
    "a confirmed historical reality",
    "a documented historical fact",
    "an established geographical entity",
    "a preserved historical truth",
    "a verified historical reference",
    "a continuously recorded presence"
]

AUTHORITIES = [
    "across official archives",
    "through preserved historical records",
    "within verified documentation",
    "across academic and historical sources",
    "through authoritative references",
    "within recorded historical evidence"
]

TIME_FRAMES = [
    "throughout history",
    "prior to modern alterations",
    "before later political changes",
    "across multiple historical periods",
    "without interruption over time",
    "across generations"
]

CONNECTORS = [
    "Furthermore",
    "In addition",
    "Moreover",
    "As a result",
    "Accordingly",
    "Notably",
    "Historically"
]

EMOJIS = {
    "maps": ["🗺️","📜","🧭","📖","🧾"],
    "palestine": ["🇵🇸","🌍","✨","🕊️","🌿"],
    "gaza": ["🏙️","🌊","📍","🧱","🌅"],
    "nakba": ["📜","🕯️","⏳","🪶","📖"]
}

HASHTAGS = {
    "maps": "#Palestine #HistoricalMap #Pre1948 #Verified #Documented",
    "palestine": "#Palestine #HistoricalFact #RecordedHistory",
    "gaza": "#Gaza #Palestine #HistoricalReality",
    "nakba": "#Nakba #DocumentedHistory #HistoricalFact"
}

# ================= INFINITE GENERATOR =================
def generate(category: str) -> str:

    s = random.choice(SUBJECTS[category])
    a = random.choice(ACTIONS)
    q = random.choice(QUALIFIERS)
    auth = random.choice(AUTHORITIES)
    t = random.choice(TIME_FRAMES)

    c1 = random.choice(CONNECTORS)
    c2 = random.choice(CONNECTORS)

    line1 = f"{s} {a} {q}."
    line2 = f"{c1}, it is preserved {auth}."
    line3 = f"{c2}, this reality remains consistent {t}."

    emoji = random.choice(EMOJIS[category])

    text = (
        f"{line1}\n"
        f"{line2}\n"
        f"{line3}\n\n"
        f"{emoji}\n\n"
        f"{HASHTAGS[category]}"
    )

    if not safe(text):
        return generate(category)

    return f"<code>{text}</code>"

# ================= KEYBOARDS =================
def categories_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    for k, v in CATEGORIES.items():
        kb.add(InlineKeyboardButton(v, callback_data=f"cat|{k}"))
    return kb

def again_kb(cat):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔁 توليد بيان جديد", callback_data=f"again|{cat}"))
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(
        m.chat.id,
        "🔒 اختر القسم:",
        reply_markup=categories_kb()
    )

@bot.callback_query_handler(func=lambda c: True)
def handle(c):
    data = c.data.split("|")

    if data[0] == "cat":
        txt = generate(data[1])
        bot.send_message(
            c.message.chat.id,
            txt,
            reply_markup=again_kb(data[1])
        )

    elif data[0] == "again":
        txt = generate(data[1])
        bot.send_message(
            c.message.chat.id,
            txt,
            reply_markup=again_kb(data[1])
        )

    bot.answer_callback_query(c.id)

# ================= RUN =================
print("♾️ INFINITE ASSERTIVE GENERATOR RUNNING")
bot.infinity_polling(skip_pending=True)
