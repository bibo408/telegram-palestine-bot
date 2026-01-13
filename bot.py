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

# ================= USER MEMORY =================
USER_HISTORY = {}
MEMORY_LIMIT = 300
MEMORY_TTL = 3600 * 6  # 6 hours

def now():
    return int(time.time())

def seen(uid, sig):
    USER_HISTORY.setdefault(uid, {})
    if sig in USER_HISTORY[uid]:
        return now() - USER_HISTORY[uid][sig] < MEMORY_TTL
    return False

def remember(uid, sig):
    USER_HISTORY.setdefault(uid, {})
    USER_HISTORY[uid][sig] = now()
    if len(USER_HISTORY[uid]) > MEMORY_LIMIT:
        USER_HISTORY[uid] = dict(
            sorted(USER_HISTORY[uid].items(), key=lambda x: x[1])[-MEMORY_LIMIT:]
        )

# ================= USER PREFS =================
USER_PREFS = {}

def prefs(uid):
    USER_PREFS.setdefault(uid, {
        "randomness": 0.5
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
        "Palestine exists as a continuous historical identity",
        "Palestine remains present through land, memory, and people",
        "Palestine persists beyond time and imposed narratives",
    ],
    "gaza": [
        "Gaza reflects lived Palestinian reality",
        "Gaza carries Palestinian presence forward",
        "Gaza stands as daily evidence of Palestinian life",
    ],
    "memory": [
        "Palestinian memory moves steadily through generations",
        "Memory preserves Palestinian presence without interruption",
        "Palestinian memory records what history cannot erase",
    ],
    "nakba": [
        "The Nakba marked a decisive historical rupture",
        "The Nakba reshaped Palestinian life permanently",
        "The Nakba altered the geography of Palestinian existence",
    ]
}

MIDDLES = [
    "documented carefully through records, names, and places",
    "preserved with historical accuracy and restraint",
    "recorded without exaggeration or distortion",
    "maintained through continuous human presence",
    "carried forward through lived experience",
    "preserved through memory rather than narration",
    "recorded quietly but without interruption",
    "maintained as part of an unbroken historical record"
]

ENDINGS = [
    "as part of Palestinian historical continuity",
    "within Palestinian collective memory",
    "as a documented Palestinian reality",
    "rooted firmly in historical presence",
    "preserved beyond erasure",
    "remaining inseparable from Palestinian identity",
    "connected permanently to place and memory",
    "held intact across generations"
]

# ================= QUESTIONS (NEW) =================
QUESTIONS = {
    "palestine": [
        "If this identity never disappeared, why is it still questioned?",
        "What does denial look like when history remains visible?",
        "How much evidence is required before reality is accepted?"
    ],
    "gaza": [
        "If daily life continues, what exactly is claimed to be absent?",
        "Why is lived reality still treated as a debate?",
        "At what point does existence stop needing justification?"
    ],
    "maps": [
        "If maps record reality, why are these ones ignored?",
        "When geography is documented, what remains to dispute?",
        "How can erased borders still appear so clearly?"
    ],
    "memory": [
        "If memory is continuous, who decides when it ends?",
        "Why is remembrance feared when it stays consistent?",
        "What threatens power more than uninterrupted memory?"
    ],
    "nakba": [
        "If displacement reshaped everything, why is its cause denied?",
        "How does a rupture vanish if its impact never did?",
        "Who benefits from redefining historical breaks?"
    ]
}

EMOJIS = ["🇵🇸","📜","🕊️","⏳","🗺️"]

HASHTAGS = {
    "palestine": "#Palestine #PalestinianIdentity #Hatshepsut",
    "gaza": "#Gaza #PalestinianMemory #Hatshepsut",
    "maps": "#HistoricalMap #Palestine #Hatshepsut",
    "memory": "#PalestinianMemory #History #Hatshepsut",
    "nakba": "#Nakba #PalestinianMemory #Hatshepsut"
}

# ================= SYNONYMS =================
SYNONYMS = {
    "historical": ["documented","archival","recorded"],
    "preserved": ["maintained","kept","retained"],
    "memory": ["remembrance","collective memory"],
    "exists": ["persists","remains","endures"]
}

def apply_synonyms(text, intensity):
    for w, alts in SYNONYMS.items():
        if random.random() < intensity:
            text = re.sub(rf"\b{w}\b", random.choice(alts), text, count=1)
    return text

# ================= TYPOGRAPHY =================
def typography(text):
    return f"<code>{text}</code>"

# ================= GENERATOR =================
def generate(uid, cat):
    r = prefs(uid)["randomness"]

    o = random.choice(OPENINGS[cat])
    m = random.choice(MIDDLES)
    e = random.choice(ENDINGS)
    q = random.choice(QUESTIONS[cat])
    emoji = random.choice(EMOJIS)

    main_text = f"{o},\n{m},\n{e}. {emoji}"
    main_text = apply_synonyms(main_text, r)

    full_text = (
        f"{main_text}\n\n"
        f"<b>{q}</b>\n\n"
        f"{HASHTAGS[cat]}"
    )

    sig = hashlib.sha1(main_text.encode()).hexdigest()

    if safe(full_text) and semantic_safe(full_text) and not seen(uid, sig):
        remember(uid, sig)
        return typography(full_text)

    remember(uid, sig)
    return typography(full_text)

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

def again_kb(cat):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{cat}"),
        InlineKeyboardButton("📋 Copy", callback_data="copy")
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
        cat = data[1]
        txt = generate(uid, cat)
        bot.send_message(c.message.chat.id, txt, reply_markup=again_kb(cat))

    elif data[0] == "again":
        cat = data[1]
        prefs(uid)["randomness"] = min(0.9, prefs(uid)["randomness"] + 0.07)
        txt = generate(uid, cat)
        bot.send_message(c.message.chat.id, txt, reply_markup=again_kb(cat))

    elif data[0] == "copy":
        bot.answer_callback_query(c.id, "Copied ✔️")

# ================= RUN =================
print("🇵🇸 Strong Tone + Question Engine running...")
bot.infinity_polling(skip_pending=True)
