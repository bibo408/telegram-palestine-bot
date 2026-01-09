```python
# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import re

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

# ================= SEMANTIC AVOIDANCE ENGINE =================
SEMANTIC_BLACKLIST = {
    "war": ["battle","fight","combat","clash"],
    "military": ["armed","forces","troops"],
    "destruction": ["ruin","devastation","wreckage"],
}

def semantic_safe(text):
    t = text.lower()
    for root, variants in SEMANTIC_BLACKLIST.items():
        if root in t:
            return False
        for v in variants:
            if v in t:
                return False
    return True

# ================= USER VARIATION LOCK =================
USER_HISTORY = {}

def seen_before(uid, key):
    USER_HISTORY.setdefault(uid, [])
    return key in USER_HISTORY[uid]

def remember(uid, key):
    USER_HISTORY.setdefault(uid, []).append(key)
    if len(USER_HISTORY[uid]) > 200:
        USER_HISTORY[uid] = USER_HISTORY[uid][-200:]

# ================= SYNONYMS ENGINE =================
SYNONYMS = {
    "historical": ["documented", "archival", "recorded"],
    "map": ["representation", "cartographic record"],
    "exists": ["persists", "remains"],
    "identity": ["presence", "essence"],
    "memory": ["remembrance", "collective memory"],
    "records": ["documents", "preserves"],
    "lives": ["endures", "continues"],
    "remains": ["stays", "persists"]
}

def smart_synonym_replace(text, loops=2):
    for _ in range(loops):
        for k, v in SYNONYMS.items():
            if random.random() < 0.3:
                text = re.sub(rf"\b{k}\b", random.choice(v), text, count=1, flags=re.I)
    return text

# ================= EMOJIS =================
EMOJIS = ["🇵🇸","🕊️","📜","⏳","🗺️","✨"]

# ================= CATEGORIES =================
CATEGORIES = {
    "palestine": "🇵🇸 فلسطين",
    "gaza": "🔥 غزة",
    "maps": "🗺️ خرائط فلسطين",
    "memory": "📜 الذاكرة الفلسطينية",
    "nakba": "🕊️ النكبة"
}

# ================= OPENINGS =================
OPENINGS = {
    "maps": [
        "This is a historical map of Palestine before 1948",
        "A documented historical map of Palestine prior to 1948",
        "This historical map records Palestine as it existed before 1948",
        "Maps showing Palestine before 1948 as a recorded reality"
    ],
    "palestine": [
        "Palestine exists as a continuous historical identity",
        "Palestine remains present through place and memory",
        "Palestine lives beyond time and narration"
    ],
    "gaza": [
        "Gaza represents lived Palestinian presence",
        "Gaza carries Palestinian identity forward",
        "Gaza reflects daily Palestinian reality"
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

# ================= SINGLE SUPER MOOD =================
MOODS = {
    "🧠 تثبيت تاريخي عميق": {
        "middles": [
            "documented carefully through names and places",
            "recorded without exaggeration or narrative noise",
            "preserved as factual historical evidence"
        ],
        "endings": [
            "as part of Palestinian historical continuity",
            "within the documented Palestinian record",
            "as a fixed historical reality"
        ]
    }
}

# ================= HASHTAGS =================
HASHTAGS = {
    "palestine": "#Palestine #History #Hatshepsut",
    "gaza": "#Gaza #Palestine #Hatshepsut",
    "maps": "#HistoricalMap #Palestine #Hatshepsut",
    "memory": "#PalestinianMemory #History #Hatshepsut",
    "nakba": "#Nakba #PalestinianMemory #Hatshepsut"
}

# ================= ANTI-FLATNESS =================
def anti_flatness(o, m, e):
    lens = [len(o.split()), len(m.split()), len(e.split())]
    return max(lens) - min(lens) >= 2

# ================= TYPOGRAPHY =================
def apply_typography(text):
    return f"<code>{text}</code>"

# ================= GENERATOR =================
def generate_hook(uid, category):
    mood = list(MOODS.keys())[0]
    for _ in range(50):
        o = random.choice(OPENINGS[category])
        m = random.choice(MOODS[mood]["middles"])
        e = random.choice(MOODS[mood]["endings"])
        emoji = random.choice(EMOJIS)

        if not anti_flatness(o, m, e):
            continue

        key = f"{o}|{m}|{e}"
        if seen_before(uid, key):
            continue

        text = f"{o},\n{m},\n{e}. {emoji}\n\n{HASHTAGS[category]}"
        text = smart_synonym_replace(text)

        if safe(text) and semantic_safe(text):
            remember(uid, key)
            return apply_typography(text)

    return apply_typography("No new safe formulation available.")

# ================= KEYBOARDS =================
def categories_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    for k, v in CATEGORIES.items():
        kb.add(InlineKeyboardButton(v, callback_data=f"cat|{k}"))
    return kb

def again_kb(category, copied=False):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{category}"))
    if not copied:
        kb.add(InlineKeyboardButton("📋 Copy", callback_data=f"copy|{category}"))
    else:
        kb.add(InlineKeyboardButton("✅ Copied", callback_data="noop"))
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, "🇵🇸 اختار القسم:", reply_markup=categories_kb())

@bot.callback_query_handler(func=lambda c: True)
def handle(c):
    uid = c.from_user.id
    data = c.data.split("|")

    if data[0] == "cat":
        cat = data[1]
        text = generate_hook(uid, cat)
        bot.send_message(c.message.chat.id, text, reply_markup=again_kb(cat))

    elif data[0] == "again":
        cat = data[1]
        text = generate_hook(uid, cat)
        bot.send_message(c.message.chat.id, text, reply_markup=again_kb(cat))

    elif data[0] == "copy":
        bot.edit_message_reply_markup(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            reply_markup=again_kb(data[1], copied=True)
        )
        bot.answer_callback_query(c.id, "Copied ✔️")

    else:
        bot.answer_callback_query(c.id)

# ================= RUN =================
print("🇵🇸 Palestinian Historical Engine running...")
bot.infinity_polling(skip_pending=True)
```
