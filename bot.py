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
        "This historical map records Palestine as it existed before 1948",
        "Explore the Palestinian landscape as it was pre-1948",
        "Palestine before 1948, captured in this historical map",
        "This map showcases Palestine in its historical borders",
        "A visual record of Palestinian territory before 1948",
        "Mapping Palestine's historical geography prior to 1948",
        "The pre-1948 borders of Palestine displayed here",
        "This archival map preserves Palestine's past",
        "Palestine depicted historically before 1948",
        "A visual documentation of Palestine pre-1948",
        "Historical cartography of Palestine before 1948",
        "Palestine’s geography prior to 1948 in detail",
        "Detailed map illustrating Palestine before 1948"
    ],
    "palestine": [
        "Palestine exists as a continuous identity",
        "Palestine lives beyond time and narration",
        "Palestine remains present through memory and place",
        "Palestinian identity persists throughout history",
        "Palestine endures through culture and memory",
        "Palestinian heritage remains alive today",
        "Palestine’s story continues through generations",
        "Palestine stands as a living history",
        "Palestinian land holds an eternal identity",
        "Palestine maintains its presence despite challenges",
        "Palestinian culture and identity persist",
        "Palestine’s existence transcends time",
        "Palestine lives in memory and spirit",
        "Palestine remains a core identity",
        "Palestine is eternal through history and people"
    ],
    "gaza": [
        "Gaza represents daily Palestinian presence",
        "Gaza carries Palestinian identity forward",
        "Gaza reflects lived Palestinian reality",
        "Life in Gaza embodies Palestinian continuity",
        "Gaza holds centuries of history and memory",
        "The streets of Gaza tell Palestinian stories",
        "Gaza preserves Palestinian culture and life",
        "Every corner of Gaza reflects history",
        "Gaza's people maintain enduring heritage",
        "Daily life in Gaza sustains identity",
        "Gaza remains a symbol of Palestinian resilience",
        "Gaza mirrors Palestinian tradition and life",
        "Gaza is a living witness to history",
        "Palestinian presence thrives in Gaza",
        "Gaza’s daily rhythm preserves identity"
    ],
    "memory": [
        "Palestinian memory moves quietly through generations",
        "Memory preserves Palestinian identity without interruption",
        "This memory carries Palestine forward",
        "Heritage keeps the Palestinian story alive",
        "Memory ensures identity continuity",
        "Collective remembrance sustains culture",
        "Memory of Palestine persists through time",
        "Palestinian history is carried in memory",
        "Past generations’ memory informs today",
        "Memory anchors Palestinian identity",
        "Stories and recollections preserve heritage",
        "Historical memory maintains culture",
        "Memory of Palestine shapes the present",
        "Heritage remembered across generations",
        "Palestinian memory is ever-living"
    ],
    "nakba": [
        "The Nakba reshaped Palestinian daily life",
        "The Nakba marked a historical turning point",
        "That moment in history altered Palestinian lives",
        "The Nakba changed the course of history",
        "Lives were transformed during the Nakba",
        "Nakba represents a critical historical moment",
        "Palestinian life was forever changed by the Nakba",
        "The Nakba reshaped communities and culture",
        "History remembers the Nakba vividly",
        "Nakba’s impact echoes through generations",
        "The Nakba is a pivotal historical event",
        "Palestinian identity was challenged during Nakba",
        "Nakba left lasting historical footprints",
        "Lives and memory were altered by Nakba",
        "The Nakba defined a new era for Palestine"
    ]
}

# ================= MOOD PRESETS =================
MOODS = {
    "🧠 هادئ توثيقي": {
        "middles": [
            "documented carefully without commentary",
            "recorded through names, places, and memory",
            "preserved without noise or exaggeration",
            "carefully noted through historical references",
            "recorded from oral histories",
            "documented with attention to every detail",
            "observed and chronicled with precision",
            "noted faithfully through evidence"
        ],
        "endings": [
            "as part of Palestinian historical continuity",
            "within Palestinian collective memory",
            "as a documented Palestinian reality",
            "as part of the enduring Palestinian narrative",
            "ensuring memory remains intact for generations",
            "recorded for historical accuracy",
            "maintaining authentic Palestinian heritage",
            "preserved for future generations"
        ]
    },
    "⚡ مكثف عميق": {
        "middles": [
            "beyond headlines and explanations",
            "without needing validation",
            "outside imposed narratives",
            "beyond public perception",
            "through deep analysis",
            "without external commentary",
            "beyond superficial accounts",
            "through concentrated focus"
        ],
        "endings": [
            "remaining undeniably Palestinian",
            "rooted deeply in Palestinian identity",
            "connected permanently to Palestine",
            "standing firmly as Palestinian",
            "deeply embedded in identity",
            "held strongly through culture",
            "unshaken in heritage",
            "anchored in Palestinian reality"
        ]
    },
    "✨ تأملي إنساني": {
        "middles": [
            "through quiet remembrance",
            "through lived experience",
            "through memory carried forward",
            "in silent reflection",
            "through personal connection",
            "through empathetic understanding",
            "with mindful observation",
            "reflecting human experience"
        ],
        "endings": [
            "held gently within Palestinian memory",
            "remembered without permission",
            "kept alive through identity",
            "nurtured in cultural consciousness",
            "preserved in hearts and minds",
            "honored through collective remembrance",
            "maintained with care",
            "safeguarded in human memory"
        ]
    }
}

# ================= SYNONYMS =================
SYNONYMS = {
    "historical": ["documented", "archival", "recorded"],
    "Palestine": ["Palestinian land", "the land of Palestine", "Palestinian homeland"],
    "memory": ["heritage", "legacy", "recollection"],
    "identity": ["being", "essence", "character"],
    "life": ["existence", "daily life", "lifestyle"]
}

def apply_synonyms(text):
    for word, options in SYNONYMS.items():
        text = text.replace(word, random.choice(options))
    return text

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
    if variance < 2.0:
        return False
    if opening.split()[0].lower() in middle.lower():
        return False
    if ending.split()[0].lower() in middle.lower():
        return False
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
            f"{HASHTAGS[category]}"
        )

        raw = apply_synonyms(raw)

        if safe(raw) and semantic_safe(raw):
            remember(uid, key)
            return apply_typography(raw, prefs["typography"])

    return apply_typography("No new safe formulation could be generated.", prefs["typography"])

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
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{category}|{mood}"),
        InlineKeyboardButton("📋 Copy", callback_data=f"copy|{category}|{mood}")
    )
    kb.add(
        InlineKeyboardButton("🅣 Typography", callback_data=f"typography|{category}|{mood}")
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
    prefs = get_prefs(uid)

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

    elif data[0] == "typography":
        _, category, mood = data
        modes = list(TYPOGRAPHY_MODES.keys())
        prefs["typography"] = modes[(modes.index(prefs["typography"]) + 1) % len(modes)]
        bot.answer_callback_query(c.id, f"Typography: {prefs['typography']} ✔️")

    elif data[0] == "copy":
        bot.answer_callback_query(c.id, "Copied ✔️", show_alert=True)

# ================= RUN =================
print("🇵🇸 Advanced Palestinian Hook Engine running...")
bot.infinity_polling(skip_pending=True)
