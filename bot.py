# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import re

# ================= BOT INIT =================
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

# ================= USER MEMORY =================
USER_HISTORY = {}
USER_PRESS = {}

def seen_before(uid, key):
    return key in USER_HISTORY.get(uid, [])

def remember(uid, key):
    USER_HISTORY.setdefault(uid, []).append(key)
    USER_HISTORY[uid] = USER_HISTORY[uid][-200:]

# ================= CATEGORIES =================
CATEGORIES = {
    "palestine": "🇵🇸 فلسطين",
    "gaza": "■ غزة",
    "maps": "🗺️ خرائط",
    "nakba": "— النكبة"
}

# ================= ASSERTIVE ENGINE =================

DECLARATIONS = {
    "palestine": [
        "Palestine is a historical fact",
        "Palestine exists as a defined reality",
        "Palestine is not a narrative, it is established",
        "Palestine is fixed in record and place"
    ],
    "gaza": [
        "Gaza is an integral Palestinian reality",
        "Gaza exists as documented Palestinian presence",
        "Gaza stands as a confirmed Palestinian fact"
    ],
    "maps": [
        "Historical maps record Palestine explicitly",
        "Pre-1948 cartography defines Palestine clearly",
        "These maps establish Palestine without ambiguity"
    ],
    "nakba": [
        "The Nakba is a documented historical event",
        "The Nakba altered Palestinian life irreversibly",
        "The Nakba is recorded fact, not interpretation"
    ]
}

POWER_CLAUSES = [
    "This requires no explanation",
    "This stands without justification",
    "This is not subject to debate",
    "This remains unaffected by denial"
]

SEALS = [
    "It stands as documented truth",
    "It remains historically fixed",
    "It is established and unaltered",
    "It is neither disputed nor erased"
]

# ================= PRESS LEVEL LOGIC =================
def build_statement(category, level):
    d = random.choice(DECLARATIONS[category])

    if level == 0:
        return f"{d}.\n{random.choice(POWER_CLAUSES)}.\n{random.choice(SEALS)}."
    elif level == 1:
        return f"{d}.\n{random.choice(SEALS)}."
    elif level == 2:
        core = d.split(" is ")[0]
        return f"{core} exists."
    else:
        core = d.split(" ")[0]
        return core + "."

# ================= HASHTAGS =================
HASHTAGS = {
    "palestine": "#Palestine #HistoricalFact",
    "gaza": "#Gaza #EstablishedReality",
    "maps": "#HistoricalMaps #RecordedTruth",
    "nakba": "#Nakba #DocumentedHistory"
}

# ================= TYPOGRAPHY =================
def apply_typography(text):
    return f"<code>{text}</code>"

# ================= GENERATOR =================
def generate(uid, category):
    USER_PRESS.setdefault(uid, 0)

    for _ in range(50):
        lvl = min(USER_PRESS[uid], 3)
        body = build_statement(category, lvl)
        emoji = random.choice(["🇵🇸", "■", "—"])
        text = f"{body} {emoji}\n\n{HASHTAGS[category]}"
        key = f"{category}|{lvl}|{body}"

        if seen_before(uid, key):
            continue
        if not safe(text):
            continue

        remember(uid, key)
        return apply_typography(text)

    return apply_typography("Statement already established.")

# ================= KEYBOARDS =================
def categories_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    for k, v in CATEGORIES.items():
        kb.add(InlineKeyboardButton(v, callback_data=f"cat|{k}"))
    return kb

def reinforce_kb(category):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🔁 Reinforce Statement", callback_data=f"again|{category}")
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(
        m.chat.id,
        "🔒 اختر الحقيقة:",
        reply_markup=categories_kb()
    )

@bot.callback_query_handler(func=lambda c: True)
def handle(c):
    uid = c.from_user.id
    data = c.data.split("|")

    if data[0] == "cat":
        USER_PRESS[uid] = 0
        cat = data[1]
        text = generate(uid, cat)
        bot.send_message(c.message.chat.id, text, reply_markup=reinforce_kb(cat))

    elif data[0] == "again":
        USER_PRESS[uid] += 1
        cat = data[1]
        text = generate(uid, cat)
        bot.send_message(c.message.chat.id, text, reply_markup=reinforce_kb(cat))

    else:
        bot.answer_callback_query(c.id)

# ================= RUN =================
print("■ ASSERTIVE FACT ENGINE RUNNING")
bot.infinity_polling(skip_pending=True)
