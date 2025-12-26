# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import re

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= HARD BLOCKED WORDS =================
BLOCKED = [
    "conflict","violence","violent","resistance","occupation",
    "zion","zionist","jewish","israel","israeli",
    "attack","kill","bomb","destroy","rocket","missile",
    "fraud","scam"
]

# ================= SEMANTIC AVOIDANCE ENGINE =================
SEMANTIC_BLOCKS = [
    ["force","forced","forcibly","imposed"],
    ["erased","erase","erasing","wipe"],
    ["removed","removal","displaced"],
    ["military","armed","weapon"],
    ["dominated","control","seized"],
    ["suffer","pain","tragedy","catastrophe"]
]

def semantic_safe(text):
    t = text.lower()
    for cluster in SEMANTIC_BLOCKS:
        for word in cluster:
            if word in t:
                return False
    return True

# ================= USER VARIATION MEMORY =================
USER_HISTORY = {}

def seen_before(user_id, key):
    if user_id not in USER_HISTORY:
        USER_HISTORY[user_id] = set()
    return key in USER_HISTORY[user_id]

def remember(user_id, key):
    USER_HISTORY[user_id].add(key)

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

# ================= OPENINGS =================
OPENINGS = {
    "maps": [
        "This is a historical map of Palestine before 1948",
        "This historical map documents Palestine prior to 1948",
        "A historical map showing Palestine before 1948"
    ],
    "palestine": [
        "Palestine exists as a living identity",
        "Palestine remains present through memory",
        "Palestine lives beyond time and headlines"
    ],
    "gaza": [
        "Gaza represents continuous Palestinian presence",
        "Gaza reflects daily Palestinian life",
        "Gaza carries Palestinian memory forward"
    ],
    "memory": [
        "Palestinian memory carries identity forward",
        "This memory moves quietly through generations",
        "History lives without asking permission"
    ],
    "nakba": [
        "The Nakba reshaped Palestinian daily life",
        "The Nakba marked a turning point in history",
        "That historical moment altered lives forever"
    ]
}

# ================= DEVELOPMENT LAYERS =================
MIDDLES = [
    "not as a claim, but as a recorded reality",
    "through names, places, and remembrance",
    "without explanation or justification",
    "beyond timelines and political framing"
]

ENDINGS = [
    "remaining undeniably Palestinian",
    "rooted deeply in Palestinian identity",
    "connected to Palestine without interruption",
    "preserved as Palestinian historical memory"
]

# ================= HASHTAGS =================
HASHTAGS = {
    "palestine": "#Palestine #PalestinianIdentity #Hatshepsut",
    "gaza": "#Gaza #PalestinianMemory #Hatshepsut",
    "maps": "#HistoricalMap #Palestine #Hatshepsut",
    "memory": "#PalestinianMemory #History #Hatshepsut",
    "nakba": "#Nakba #PalestinianMemory #Hatshepsut"
}

# ================= ANTI-FLATNESS DETECTOR =================
def is_flat(text):
    words = re.findall(r"\w+", text.lower())

    if len(words) < 12:
        return True

    identity_terms = ["palestine","palestinian","gaza","nakba"]
    if not any(w in words for w in identity_terms):
        return True

    depth_terms = ["memory","identity","history","map","historical"]
    if not any(w in words for w in depth_terms):
        return True

    return False

# ================= HOOK ENGINE =================
def generate_hook(user_id, category):
    for _ in range(60):
        o = random.choice(OPENINGS[category])
        m = random.choice(MIDDLES)
        e = random.choice(ENDINGS)
        emoji = random.choice(EMOJIS)

        variation_key = f"{category}|{o}|{m}|{e}"
        if seen_before(user_id, variation_key):
            continue

        text_body = (
            f"{o},\n"
            f"{m},\n"
            f"{e}. {emoji}"
        )

        full_text = f"{text_body}\n\n{HASHTAGS[category]}"

        if not semantic_safe(full_text):
            continue
        if not all(w not in full_text.lower() for w in BLOCKED):
            continue
        if is_flat(full_text):
            continue

        remember(user_id, variation_key)
        return f"<code>{full_text}</code>"

    return "<code>No new high-quality formulation could be generated.</code>"

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
    user_id = c.from_user.id

    if data[0] == "cat":
        category = data[1]
        text = generate_hook(user_id, category)
        bot.send_message(
            c.message.chat.id,
            text,
            reply_markup=again_kb(category)
        )

    elif data[0] == "again":
        category = data[1]
        text = generate_hook(user_id, category)
        bot.send_message(
            c.message.chat.id,
            text,
            reply_markup=again_kb(category)
        )

# ================= RUN =================
print("🇵🇸 Advanced Semantic Hook Engine running...")
bot.infinity_polling(skip_pending=True)
