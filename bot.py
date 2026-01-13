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
        "This map presents Palestine as it was recorded before 1948",
    "This cartographic record shows Palestine prior to the year 1948",
    "This map documents the geography of Palestine before its alteration in 1948",
    "This historical map illustrates Palestine as it existed before 1948",
    "This map captures Palestine in its documented form before 1948",
    "This archival map reflects Palestine’s geographic reality prior to 1948",
    "This map preserves the recorded boundaries of Palestine before 1948",
    "This cartographic reference outlines Palestine as mapped before 1948",
    "This map represents Palestine according to pre-1948 documentation",
    "This recorded map presents Palestine as charted before 1948",

    "This map reflects Palestine based on geographic records before 1948",
    "This cartographic illustration shows Palestine prior to 1948 changes",
    "This map displays Palestine as recognized in maps before 1948",
    "This documented map outlines Palestine’s geography before 1948",
    "This map reconstructs Palestine according to pre-1948 cartography",
    "This archival cartographic source depicts Palestine before 1948",
    "This map illustrates Palestine using documented borders before 1948",
    "This geographic record presents Palestine prior to its redefinition in 1948",
    "This cartographic rendering shows Palestine as defined before 1948",
    "This map records Palestine’s geographic form prior to 1948",

    "This historical cartographic source presents Palestine before 1948",
    "This map displays the documented landscape of Palestine before 1948",
    "This map outlines Palestine according to archival maps before 1948",
    "This cartographic depiction presents Palestine as mapped prior to 1948",
    "This map captures the recognized geography of Palestine before 1948",
    "This documented cartographic map shows Palestine prior to 1948",
    "This map illustrates Palestine’s geographic structure before 1948",
    "This archival geographic record shows Palestine as mapped before 1948",
    "This cartographic presentation reflects Palestine before 1948",
    "This map documents Palestine’s borders as recorded before 1948",

    "This map presents Palestine’s geography according to records before 1948",
    "This historical map records Palestine as it appeared before 1948",
    "This cartographic reference documents Palestine prior to 1948",
    "This map shows Palestine based on documented geography before 1948",
    "This geographic map outlines Palestine as recorded prior to 1948",
    "This map reflects Palestine’s documented landscape before 1948",
    "This archival map shows Palestine in its geographic form before 1948",
    "This cartographic documentation presents Palestine before 1948",
    "This map captures Palestine’s documented borders prior to 1948",
    "This geographic record illustrates Palestine as mapped before 1948"
        "This map states Palestine as a recorded geographic fact before 1948",
    "This cartographic record confirms Palestine’s presence prior to 1948",
    "This map asserts Palestine as a documented land before 1948",
    "This map establishes Palestine as a mapped reality before 1948",
    "This geographic record fixes Palestine in place before 1948",

    "This map affirms Palestine as a documented geography before 1948",
    "This cartographic source anchors Palestine prior to 1948",
    "This map confirms Palestine as a mapped territory before 1948",
    "This documented map leaves no ambiguity about Palestine before 1948",
    "This geographic record secures Palestine’s presence before 1948",

    "This map defines Palestine through recorded geography before 1948",
    "This cartographic evidence places Palestine clearly before 1948",
    "This map asserts Palestine through documented borders before 1948",
    "This geographic documentation establishes Palestine prior to 1948",
    "This map confirms Palestine as geographic reality before 1948",

    "This cartographic record leaves Palestine fixed before 1948",
    "This map positions Palestine as a recorded fact before 1948",
    "This geographic source affirms Palestine’s mapped existence before 1948",
    "This map documents Palestine as an established land before 1948",
    "This cartographic map asserts Palestine before 1948",

    "This map reinforces Palestine as documented geography before 1948",
    "This geographic record confirms Palestine’s territorial presence before 1948",
    "This map establishes Palestine through recorded boundaries before 1948",
    "This cartographic evidence affirms Palestine’s existence before 1948",
    "This map documents Palestine as a geographic certainty before 1948",

    "This geographic map fixes Palestine as a recorded land before 1948",
    "This cartographic record validates Palestine prior to 1948",
    "This map affirms Palestine’s documented territory before 1948",
    "This geographic source confirms Palestine as mapped before 1948",
    "This map asserts Palestine as an established geography before 1948",

    "This cartographic documentation leaves no doubt about Palestine before 1948",
    "This map records Palestine as an indisputable geography before 1948",
    "This geographic record anchors Palestine firmly before 1948",
    "This map establishes Palestine as a territorial fact before 1948",
    "This cartographic source confirms Palestine’s place before 1948",

    "This map fixes Palestine within recorded geography before 1948",
    "This geographic documentation confirms Palestine’s existence before 1948",
    "This cartographic record asserts Palestine without ambiguity before 1948",
    "This map establishes Palestine as mapped land before 1948",
    "This geographic source reinforces Palestine before 1948",

    "This map affirms Palestine as a documented territorial reality before 1948",
    "This cartographic record positions Palestine decisively before 1948",
    "This geographic map confirms Palestine as recorded land before 1948",
    "This map establishes Palestine through documented geography before 1948",
    "This cartographic evidence fixes Palestine prior to 1948"
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

