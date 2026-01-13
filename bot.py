# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import re
import time
import hashlib

# ================= BOT INIT =================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= SAFE FILTER =================
BLOCKED = {
    "conflict","violence","violent","resistance","occupation",
    "zion","zionist","jewish","israel","israeli",
    "attack","kill","bomb","destroy","rocket","missile",
    "fraud","scam"
}

def safe(text):
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    return not any(w in BLOCKED for w in words)

SEMANTIC_BLACKLIST = {
    "war": ["battle","fight","combat","clash"],
    "military": ["armed","forces","troops"],
    "destruction": ["ruin","devastation","wreckage"],
}

def semantic_safe(text):
    t = text.lower()
    for root, variants in SEMANTIC_BLACKLIST.items():
        if re.search(rf"\b{root}\b", t):
            return False
        for v in variants:
            if re.search(rf"\b{v}\b", t):
                return False
    return True

# ================= USER MEMORY (HASH BASED) =================
USER_HISTORY = {}
MEMORY_LIMIT = 300
MEMORY_TTL = 3600 * 6  # 6 hours

def _now():
    return int(time.time())

def seen(uid, sig):
    USER_HISTORY.setdefault(uid, {})
    if sig in USER_HISTORY[uid]:
        if _now() - USER_HISTORY[uid][sig] < MEMORY_TTL:
            return True
    return False

def remember(uid, sig):
    USER_HISTORY.setdefault(uid, {})
    USER_HISTORY[uid][sig] = _now()
    if len(USER_HISTORY[uid]) > MEMORY_LIMIT:
        USER_HISTORY[uid] = dict(
            sorted(USER_HISTORY[uid].items(), key=lambda x: x[1])[-MEMORY_LIMIT:]
        )

# ================= USER PREFS =================
USER_PREFS = {}

def prefs(uid):
    USER_PREFS.setdefault(uid, {
        "randomness": 0.4,
        "style": "mono"
    })
    return USER_PREFS[uid]

# ================= TEXT BANK =================
OPENINGS = {
    "maps": [
        "This is a historical map of Palestine before 1948",
        "An archival cartographic record of Palestine prior to 1948",
        "A documented representation of Palestinian geography before 1948",
    ],
    "palestine": [
        "Palestine exists as a continuous identity",
        "Palestine lives beyond time and narration",
        "Palestine remains present through memory and place",
    ],
    "gaza": [
        "Gaza reflects lived Palestinian reality",
        "Gaza carries Palestinian identity forward",
        "Gaza represents daily Palestinian presence",
    ],
    "memory": [
        "Palestinian memory moves quietly through generations",
        "Memory preserves Palestinian identity without interruption",
        "This memory carries Palestine forward",
    ],
    "nakba": [
        "The Nakba marked a historical turning point",
        "The Nakba reshaped Palestinian daily life",
        "That moment in history altered Palestinian lives",
    ]
}

MOODS = {
    "🧠 هادئ توثيقي": {
        "middles": [
            "documented carefully through records and testimony",
            "preserved with historical accuracy and restraint",
            "recorded without commentary or exaggeration",
        ],
        "endings": [
            "as part of Palestinian historical continuity",
            "within Palestinian collective memory",
            "as a documented Palestinian reality",
        ]
    },
    "⚡ مكثف عميق": {
        "middles": [
            "beyond headlines and imposed narratives",
            "outside simplified explanations",
            "without requiring validation",
        ],
        "endings": [
            "remaining undeniably Palestinian",
            "rooted deeply in Palestinian identity",
            "connected permanently to Palestine",
        ]
    },
    "✨ تأملي إنساني": {
        "middles": [
            "through lived experience and quiet reflection",
            "through memory carried forward gently",
            "through human remembrance",
        ],
        "endings": [
            "held gently within Palestinian memory",
            "remembered without permission",
            "kept alive through identity",
        ]
    }
}

EMOJIS = ["🇵🇸","📜","🕊️","⏳","🗺️","✨"]

HASHTAGS = {
    "palestine": "#Palestine #PalestinianIdentity #Hatshepsut",
    "gaza": "#Gaza #PalestinianMemory #Hatshepsut",
    "maps": "#HistoricalMap #Palestine #Hatshepsut",
    "memory": "#PalestinianMemory #History #Hatshepsut",
    "nakba": "#Nakba #PalestinianMemory #Hatshepsut"
}

# ================= SYNONYM ENGINE =================
SYNONYMS = {
    "historical": ["documented","archival","recorded"],
    "exists": ["persists","remains","endures"],
    "memory": ["remembrance","collective memory"],
    "identity": ["presence","essence"]
}

def apply_synonyms(text, intensity):
    for word, alts in SYNONYMS.items():
        if random.random() < intensity:
            text = re.sub(rf"\b{word}\b", random.choice(alts), text, count=1)
    return text

# ================= TYPOGRAPHY =================
def typography(text):
    return f"<code>{text}</code>"

# ================= GENERATOR =================
def generate(uid, cat, mood):
    p = prefs(uid)
    r = p["randomness"]

    o = random.choice(OPENINGS[cat])
    m = random.choice(MOODS[mood]["middles"])
    e = random.choice(MOODS[mood]["endings"])
    emoji = random.choice(EMOJIS)

    text = f"{o},\n{m},\n{e}. {emoji}\n\n{HASHTAGS[cat]}"
    text = apply_synonyms(text, r)

    sig = hashlib.sha1(text.encode()).hexdigest()

    if safe(text) and semantic_safe(text) and not seen(uid, sig):
        remember(uid, sig)
        return typography(text)

    # fallback: forced mutate
    text += f" {random.choice(['',' '])}{emoji}"
    sig = hashlib.sha1(text.encode()).hexdigest()
    remember(uid, sig)
    return typography(text)

# ================= UI =================
CATEGORIES = {
    "palestine": "🇵🇸 فلسطين",
    "gaza": "🔥 غزة",
    "maps": "🗺️ خرائط فلسطين",
    "memory": "📜 الذاكرة الفلسطينية",
    "nakba": "🕊️ النكبة"
}

def cat_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    for k,v in CATEGORIES.items():
        kb.add(InlineKeyboardButton(v, callback_data=f"cat|{k}"))
    return kb

def mood_kb(cat):
    kb = InlineKeyboardMarkup()
    for m in MOODS:
        kb.add(InlineKeyboardButton(m, callback_data=f"mood|{cat}|{m}"))
    return kb

def again_kb(cat, mood):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{cat}|{mood}"),
        InlineKeyboardButton("📋 Copy", callback_data=f"copy")
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, "🇵🇸 اختار القسم:", reply_markup=cat_kb())

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    data = c.data.split("|")
    uid = c.from_user.id

    if data[0] == "cat":
        bot.send_message(c.message.chat.id, "🎭 اختار النبرة:", reply_markup=mood_kb(data[1]))

    elif data[0] == "mood":
        _, cat, mood = data
        txt = generate(uid, cat, mood)
        bot.send_message(c.message.chat.id, txt, reply_markup=again_kb(cat, mood))

    elif data[0] == "again":
        _, cat, mood = data
        prefs(uid)["randomness"] = min(0.9, prefs(uid)["randomness"] + 0.07)
        txt = generate(uid, cat, mood)
        bot.send_message(c.message.chat.id, txt, reply_markup=again_kb(cat, mood))

    elif data[0] == "copy":
        bot.answer_callback_query(c.id, "Copied ✔️")

# ================= RUN =================
print("🇵🇸 Stable Palestinian Hook Engine running...")
bot.infinity_polling(skip_pending=True)
