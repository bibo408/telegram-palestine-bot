# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

# ================= BOT INIT =================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= SAFETY FILTER =================
BLOCKED = [
    "violence","violent","attack","kill","bomb","destroy",
    "weapon","missile","rocket","war","fight","combat"
]

def safe(text):
    t = text.lower()
    return not any(w in t for w in BLOCKED)

# ================= USER MEMORY =================
USER_HISTORY = {}
USER_PRESS = {}

def remember(uid, key):
    USER_HISTORY.setdefault(uid, []).append(key)
    USER_HISTORY[uid] = USER_HISTORY[uid][-300:]

def seen(uid, key):
    return key in USER_HISTORY.get(uid, [])

# ================= UI CATEGORIES (AR ONLY) =================
CATEGORIES = {
    "maps": "🗺️ الخرائط التاريخية",
    "palestine": "🇵🇸 فلسطين",
    "gaza": "🏙️ غزة",
    "nakba": "📜 النكبة"
}

# ================= ASSERTIVE ENGLISH STATEMENTS =================
STATEMENTS = {

    "maps": [
        "This is the original historical map of Palestine before 1948",
        "This map represents Palestine as officially recorded before 1948",
        "This is an authentic cartographic record of Palestine",
        "This map documents Palestine clearly and unmistakably",
        "This is a verified historical map identifying Palestine"
    ],

    "palestine": [
        "Palestine is a historical fact",
        "Palestine exists as an established reality",
        "Palestine is documented across history and geography",
        "Palestine is fixed in official records",
        "Palestine is not a claim, it is a fact"
    ],

    "gaza": [
        "Gaza is an integral part of Palestine",
        "Gaza exists as a documented Palestinian city",
        "Gaza represents a confirmed Palestinian presence",
        "Gaza is historically and geographically Palestinian",
        "Gaza stands as a recorded Palestinian reality"
    ],

    "nakba": [
        "The Nakba is a documented historical event",
        "The Nakba represents a recorded turning point in history",
        "The Nakba is an established historical fact",
        "The Nakba is preserved in historical documentation",
        "The Nakba is not interpretation, it is record"
    ]
}

# ================= POWER SEALS =================
SEALS = [
    "This is an established historical fact",
    "This stands as documented truth",
    "This requires no justification",
    "This remains unchanged by denial",
    "This is fixed in historical record"
]

# ================= EMOJIS =================
EMOJIS = {
    "maps": ["🗺️","📍","🧭","📜","🧾","📐","🪶","📖"],
    "palestine": ["🌍","🧱","📜","⏳","🌿","✨","🕊️"],
    "gaza": ["🏙️","🌊","📍","🧱","🌅","⏳","🕊️"],
    "nakba": ["📜","⏳","🕯️","📖","🪶","🧠","🕊️"]
}

# ================= HASHTAGS =================
HASHTAGS = {
    "maps": (
        "#Palestine #HistoricalMap #Pre1948 #Documented "
        "#HistoricalRecord #Verified #Fact"
    ),
    "palestine": (
        "#Palestine #HistoricalFact #RecordedHistory "
        "#Established #Identity #Reality"
    ),
    "gaza": (
        "#Gaza #Palestine #HistoricalReality "
        "#Recorded #Geography #Fact"
    ),
    "nakba": (
        "#Nakba #DocumentedHistory #HistoricalFact "
        "#Recorded #Memory #Truth"
    )
}

# ================= TYPOGRAPHY STYLE =================
def style(text):
    return (
        "<b>— OFFICIAL RECORD —</b>\n\n"
        f"<code>{text}</code>"
    )

# ================= GENERATOR =================
def generate(uid, category):
    USER_PRESS.setdefault(uid, 0)
    level = min(USER_PRESS[uid], 2)

    for _ in range(60):
        base = random.choice(STATEMENTS[category])
        seal = random.choice(SEALS)
        emoji = random.choice(EMOJIS[category])

        if level == 0:
            body = f"{base}.\n{seal}."
        elif level == 1:
            body = f"{base}."
        else:
            body = base.split(",")[0] + "."

        text = (
            f"{body}\n\n"
            f"🇵🇸 {emoji}\n\n"
            f"{HASHTAGS[category]}"
        )

        key = f"{category}|{body}"
        if seen(uid, key):
            continue
        if not safe(text):
            continue

        remember(uid, key)
        return style(text)

    return style("The record is already established.")

# ================= KEYBOARDS (STYLED) =================
def categories_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    for k, v in CATEGORIES.items():
        kb.add(
            InlineKeyboardButton(v, callback_data=f"cat|{k}")
        )
    return kb

def again_kb(category):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🔁 تعزيز البيان", callback_data=f"again|{category}")
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(
        m.chat.id,
        "🔒 اختر القسم لعرض الحقيقة:",
        reply_markup=categories_kb()
    )

@bot.callback_query_handler(func=lambda c: True)
def handle(c):
    uid = c.from_user.id
    data = c.data.split("|")

    if data[0] == "cat":
        USER_PRESS[uid] = 0
        cat = data[1]
        txt = generate(uid, cat)
        bot.send_message(
            c.message.chat.id,
            txt,
            reply_markup=again_kb(cat)
        )

    elif data[0] == "again":
        USER_PRESS[uid] += 1
        cat = data[1]
        txt = generate(uid, cat)
        bot.send_message(
            c.message.chat.id,
            txt,
            reply_markup=again_kb(cat)
        )

    else:
        bot.answer_callback_query(c.id)

# ================= RUN =================
print("🇵🇸 ASSERTIVE ENGLISH FACT ENGINE RUNNING")
bot.infinity_polling(skip_pending=True)
