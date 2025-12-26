# -*- coding: utf-8 -*-

import os
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import openai

# ================= SETUP =================
TOKEN = os.getenv("BOT_TOKEN")  # Telegram Bot Token
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

openai.api_key = os.getenv("OPENAI_API_KEY")  # OpenAI GPT-5 API Key

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

# ================= SEMANTIC AVOIDANCE =================
SEMANTIC_BLACKLIST = {
    "war": ["battle","fight","combat","clash"],
    "military": ["armed","forces","troops"],
    "destruction": ["ruin","devastation","wreckage"],
}

def semantic_safe(text):
    t = text.lower()
    for root, variants in SEMANTIC_BLACKLIST.items():
        if root in t: return False
        for v in variants:
            if v in t: return False
    return True

# ================= USER VARIATION LOCK =================
USER_HISTORY = {}

def seen_before(uid, key):
    if uid not in USER_HISTORY:
        USER_HISTORY[uid] = set()
    return key in USER_HISTORY[uid]

def remember(uid, key):
    USER_HISTORY[uid].add(key)

# ================= USER PREFERENCES =================
USER_PREFS = {}

def get_prefs(uid):
    if uid not in USER_PREFS:
        USER_PREFS[uid] = {
            "typography": "mono",
            "randomness": "balanced"
        }
    return USER_PREFS[uid]

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

# ================= ANTI-FLATNESS DETECTOR =================
def anti_flatness(opening, middle, ending):
    lens = [len(opening.split()), len(middle.split()), len(ending.split())]
    mean = sum(lens) / 3.0
    variance = sum((l - mean) ** 2 for l in lens) / 3.0
    if variance < 2.0: return False
    if opening.split()[0].lower() in middle.lower(): return False
    if ending.split()[0].lower() in middle.lower(): return False
    return True

# ================= TYPOGRAPHY MODES =================
TYPOGRAPHY_MODES = {
    "mono": lambda t: f"<code>{t}</code>",
    "boxed": lambda t: f"<pre>{t}</pre>",
    "clean": lambda t: t
}

def apply_typography(text, mode):
    return TYPOGRAPHY_MODES.get(mode, TYPOGRAPHY_MODES["mono"])(text)

# ================= CONTROLLED RANDOMNESS =================
RANDOMNESS_LEVELS = {
    "low": 0.2,
    "balanced": 0.5,
    "high": 0.8
}

def controlled_choice(items, level):
    r = RANDOMNESS_LEVELS.get(level, 0.5)
    if random.random() > r:
        return items[0]
    return random.choice(items)

# ================= GPT-5 TEXT EXPANSION =================
def expand_with_gpt5(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error generating content: {e}"

# ================= HOOK ENGINE =================
def generate_hook(uid, category, mood):
    prefs = get_prefs(uid)
    for _ in range(80):
        opening = controlled_choice(OPENINGS[category], prefs["randomness"])
        middle = controlled_choice(MOODS[mood]["middles"], prefs["randomness"])
        ending = controlled_choice(MOODS[mood]["endings"], prefs["randomness"])
        emoji = random.choice(EMOJIS)

        if not anti_flatness(opening, middle, ending):
            continue

        key = f"{category}|{mood}|{opening}|{middle}|{ending}"
        if seen_before(uid, key):
            continue

        raw = (
            f"{opening},\n"
            f"{middle},\n"
            f"{ending}. {emoji}\n\n"
