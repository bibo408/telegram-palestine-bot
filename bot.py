# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import re
import time

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
USER_PRESS = {}

def seen_before(uid, key):
    if uid not in USER_HISTORY:
        USER_HISTORY[uid] = []
    return key in USER_HISTORY[uid]

def remember(uid, key):
    USER_HISTORY.setdefault(uid, []).append(key)
    if len(USER_HISTORY[uid]) > 200:
        USER_HISTORY[uid] = USER_HISTORY[uid][-200:]

# ================= USER PREFERENCES =================
USER_PREFS = {}

def get_prefs(uid):
    if uid not in USER_PREFS:
        USER_PREFS[uid] = {
            "typography": "mono",
            "randomness": 0.4
        }
    return USER_PREFS[uid]

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
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if line.strip().startswith("#"):
            new_lines.append(line)
            continue
        words = re.findall(r"\b\w+\b", line)
        for _ in range(loops):
            for w in words:
                lw = w.lower()
                if lw in SYNONYMS and random.random() < 0.35:
                    rep = random.choice(SYNONYMS[lw])
                    line = re.sub(rf"\b{w}\b", rep, line, count=1)
        new_lines.append(line)
    return "\n".join(new_lines)

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
        "Maps showing Palestine before 1948",

    ],
    "palestine": [
        "Palestine exists as a continuous identity",
        "Palestine lives beyond time and narration",
        "Palestine remains present through memory and place"
        "Palestine exists as a continuous identity",


    ],
    "gaza": [
        "Gaza represents daily Palestinian presence",
        "Gaza carries Palestinian identity forward",
        "Gaza reflects lived Palestinian reality"
        "Gaza represents daily Palestinian presence",


    ],
    "memory": [
        "Palestinian memory moves quietly through generations",
        "Memory preserves Palestinian identity without interruption",
        "This memory carries Palestine forward"
        "Palestinian memory moves quietly through generations",


    ],
    "nakba": [
        "The Nakba reshaped Palestinian daily life",
        "The Nakba marked a historical turning point",
        "That moment in history altered Palestinian lives"
        "The Nakba reshaped Palestinian daily life",


    ]
}

# ================= MOOD PRESETS =================
MOODS = {
    "🧠 هادئ توثيقي": {
        "middles": [
            "documented carefully without commentary",
            "recorded through names, places, and memory",
            "preserved without noise or exaggeration"
            "documented carefully without commentary",


        ],
        "endings": [
            "as part of Palestinian historical continuity",
            "within Palestinian collective memory",
            "as a documented Palestinian reality"
            "as part of Palestinian historical continuity",


        ]
    },
    "⚡ مكثف عميق": {
        "middles": [
            "beyond headlines and explanations",
            "without needing validation",
            "outside imposed narratives"
            "beyond headlines and explanations",


        ],
        "endings": [
            "remaining undeniably Palestinian",
            "rooted deeply in Palestinian identity",
            "connected permanently to Palestine"
            "remaining undeniably Palestinian",


        ]
    },
    "✨ تأملي إنساني": {
        "middles": [
            "through quiet remembrance",
            "through lived experience",
            "through memory carried forward"
            "through quiet remembrance",

        ],
        "endings": [
            "held gently within Palestinian memory",
            "remembered without permission",
            "kept alive through identity"
            "held gently within Palestinian memory",


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

# ================= ANTI-FLATNESS DETECTOR =================
def anti_flatness(o, m, e):
    lens = [len(o.split()), len(m.split()), len(e.split())]
    if max(lens) - min(lens) < 2:
        return False
    return True

# ================= TYPOGRAPHY =================
def apply_typography(text):
    return f"<code>{text}</code>"

# ================= HOOK ENGINE =================
def generate_hook(uid, category, mood):
    prefs = get_prefs(uid)
    for _ in range(60):
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

    return apply_typography("No new safe formulation could be generated.")

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

def again_kb(category, mood, copied=False):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{category}|{mood}")
    )
    if not copied:
        kb.add(
            InlineKeyboardButton("📋 Copy", callback_data=f"copy|{category}|{mood}")
        )
    else:
        kb.add(
            InlineKeyboardButton("✅ Copied", callback_data="noop")
        )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, "🇵🇸 اختار القسم:", reply_markup=categories_kb())

@bot.callback_query_handler(func=lambda c: True)
def handle(c):
    data = c.data.split("|")
    uid = c.from_user.id
    USER_PRESS.setdefault(uid, 0)

    if data[0] == "cat":
        bot.send_message(c.message.chat.id, "🎭 اختار النبرة:", reply_markup=mood_kb(data[1]))

    elif data[0] == "mood":
        USER_PRESS[uid] = 0
        _, cat, mood = data
        text = generate_hook(uid, cat, mood)
        bot.send_message(c.message.chat.id, text, reply_markup=again_kb(cat, mood))

    elif data[0] == "again":
        USER_PRESS[uid] += 1
        prefs = get_prefs(uid)
        prefs["randomness"] = min(0.9, prefs["randomness"] + 0.05)
        _, cat, mood = data
        text = generate_hook(uid, cat, mood)
        bot.send_message(c.message.chat.id, text, reply_markup=again_kb(cat, mood))

    elif data[0] == "copy":
        bot.edit_message_reply_markup(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            reply_markup=again_kb(data[1], data[2], copied=True)
        )
        bot.answer_callback_query(c.id, "Copied ✔️")

    else:
        bot.answer_callback_query(c.id)

# ================= RUN =================
print("🇵🇸 Advanced Palestinian Hook Engine running...")
bot.infinity_polling(skip_pending=True)


