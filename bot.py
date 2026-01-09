```python
# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import re

# ================= BOT =================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= SAFETY =================
BLOCKED = [
    "conflict","violence","violent","attack","kill","bomb",
    "rocket","missile","fraud","scam"
]

def safe(text):
    t = text.lower()
    return not any(w in t for w in BLOCKED)

# ================= USER MEMORY =================
USER_HISTORY = {}

def seen_before(uid, key):
    USER_HISTORY.setdefault(uid, [])
    return key in USER_HISTORY[uid]

def remember(uid, key):
    USER_HISTORY.setdefault(uid, []).append(key)
    if len(USER_HISTORY[uid]) > 300:
        USER_HISTORY[uid] = USER_HISTORY[uid][-300:]

# ================= SYNONYMS =================
SYNONYMS = {
    "historical": ["documented", "archival", "recorded"],
    "map": ["cartographic record", "geographical document"],
    "exists": ["persists", "remains"],
    "identity": ["presence", "historical reality"],
    "memory": ["documented memory", "collective record"],
    "land": ["territory", "geography"],
    "recorded": ["documented", "preserved"],
}

def smart_synonym_replace(text, loops=2):
    for _ in range(loops):
        for k, vals in SYNONYMS.items():
            if re.search(rf"\b{k}\b", text, re.IGNORECASE) and random.random() < 0.35:
                text = re.sub(rf"\b{k}\b", random.choice(vals), text, count=1, flags=re.IGNORECASE)
    return text

# ================= EMOJIS =================
EMOJIS = ["🗺️","📜","⏳","🧭"]

# ================= CATEGORIES =================
CATEGORIES = {
    "maps": "🗺️ خرائط فلسطين (تثبيت تاريخي)"
}

# ================= OPENINGS =================
OPENINGS = {
    "maps": [
        "This historical map of Palestine establishes a documented geographical reality",
        "A verified historical map confirming Palestine as a defined land",
        "This cartographic record fixes Palestine within historical geography",
        "An archival map presenting Palestine as a recorded historical territory",
        "This documented map confirms Palestine’s presence before modern alterations",
        "A preserved historical map identifying Palestine by name and borders",
        "This geographical document records Palestine as an established land",
        "A historical cartographic source defining Palestine with precision",
        "This map stands as evidence of Palestine’s historical geography",
        "An official-style historical map documenting Palestine clearly",
        "This archival cartography anchors Palestine within recorded history",
        "A historical map fixing Palestine as a recognized geographical entity",
        "This documented map records Palestine as a continuous land",
        "An authentic historical map confirming Palestine’s territorial reality",
        "This cartographic evidence places Palestine firmly in history",
    ]
}

# ================= SINGLE STRONG MOOD =================
MOOD = {
    "middles": [
        "based on verified historical sources and cartographic records",
        "derived from documented geographical surveys",
        "supported by archival references and historical documentation",
        "grounded in recorded maps and preserved sources",
        "compiled from established historical cartography",
        "confirmed through multiple documented records",
        "supported by consistent historical mapping",
        "validated by archival geographical evidence",
        "anchored in preserved historical documentation",
        "based on recognized cartographic standards",
        "derived from authenticated historical sources",
        "supported by documented geographical continuity",
    ],
    "endings": [
        "leaving no ambiguity about Palestine’s historical existence",
        "establishing Palestine as a fixed historical reality",
        "confirming Palestine as a documented geographical truth",
        "fixing Palestine permanently within historical record",
        "affirming Palestine as an undeniable historical land",
        "cementing Palestine’s place in documented history",
        "leaving no room for reinterpretation or denial",
        "standing as factual historical evidence",
        "preserving Palestine as a recorded geographical reality",
        "confirming Palestine through documented historical proof",
        "establishing historical certainty beyond narrative dispute",
        "anchoring Palestine as a verifiable historical entity",
    ]
}

# ================= HASHTAGS =================
HASHTAGS = {
    "maps": "#HistoricalMaps #Palestine #DocumentedHistory #Hatshepsut"
}

# ================= TYPOGRAPHY =================
def apply_typography(text):
    return f"<code>{text}</code>"

# ================= GENERATOR =================
def generate_hook(uid):
    for _ in range(80):
        o = random.choice(OPENINGS["maps"])
        m = random.choice(MOOD["middles"])
        e = random.choice(MOOD["endings"])
        emoji = random.choice(EMOJIS)

        key = f"{o}|{m}|{e}"
        if seen_before(uid, key):
            continue

        text = f"{o},\n{m},\n{e}. {emoji}\n\n{HASHTAGS['maps']}"
        text = smart_synonym_replace(text)

        if safe(text):
            remember(uid, key)
            return apply_typography(text)

    return apply_typography("No new documented formulation available.")

# ================= KEYBOARDS =================
def main_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🗺️ Generate Historical Map Statement", callback_data="gen"))
    return kb

def again_kb(copied=False):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("🔄 Generate Again", callback_data="again"))
    if not copied:
        kb.add(InlineKeyboardButton("📋 Copy", callback_data="copy"))
    else:
        kb.add(InlineKeyboardButton("✅ Copied", callback_data="noop"))
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, "🗺️ Historical Fixation Engine:", reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: True)
def handle(c):
    uid = c.from_user.id

    if c.data == "gen":
        text = generate_hook(uid)
        bot.send_message(c.message.chat.id, text, reply_markup=again_kb())

    elif c.data == "again":
        text = generate_hook(uid)
        bot.send_message(c.message.chat.id, text, reply_markup=again_kb())

    elif c.data == "copy":
        bot.edit_message_reply_markup(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            reply_markup=again_kb(copied=True)
        )
        bot.answer_callback_query(c.id, "Copied ✔️")

    else:
        bot.answer_callback_query(c.id)

# ================= RUN =================
print("🗺️ Historical Fixation Engine running...")
bot.infinity_polling(skip_pending=True)
```
