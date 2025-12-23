# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

# ================= BOT =================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= BLOCKED WORDS =================
BLOCKED_WORDS = [
    "conflict","violence","violent","resistance","occupation",
    "zion","zionist","jewish","israel","israeli",
    "attack","kill","bomb","fight","destroy",
    "missile","rocket","fraud","scam","steadfastness"
]

# ================= EMOJIS =================
EMOJIS = ["🇵🇸","🕊️","🌿","⏳","📜","✨","🗺️"]

# ================= OPENING CONTROL =================
OPENINGS = {
    "palestine": ["Palestine", "This land", "This place"],
    "gaza": ["Gaza", "This place", "This land"],
    "maps": ["This historical map", "This map", "This record"],
    "memory": ["This memory", "This history", "This moment"],
    "nakba": ["The Nakba", "That year", "That moment"]
}

# ================= CATEGORIES =================
CATEGORIES = {
    "palestine": "🇵🇸 فلسطين",
    "gaza": "🔥 غزة",
    "maps": "🗺️ خرائط فلسطين",
    "memory": "📜 الذاكرة الفلسطينية",
    "nakba": "🕊️ النكبة وأحداثها"
}

# ================= CORE IDEAS =================
CORE_IDEAS = {
    "palestine": [
        "carries Palestinian identity beyond time",
        "exists through memory, not permission",
        "remains present through generations"
    ],
    "gaza": [
        "reflects Palestinian presence in daily life",
        "holds stories shaped by patience",
        "remains part of Palestinian identity"
    ],
    "maps": [
        "documents Palestinian geography clearly",
        "preserves names drawn long ago",
        "records land before narratives changed"
    ],
    "memory": [
        "passes quietly between generations",
        "lives without needing explanation",
        "remains intact through remembrance"
    ],
    "nakba": [
        "changed lives without erasing identity",
        "left memories carried through generations",
        "reshaped daily life without ending belonging"
    ]
}

# ================= CONTRAST BUILDER =================
CONTRASTS = [
    "yet it remains undeniable",
    "even when ignored",
    "while time continues",
    ""
]

# ================= EMOTION LAYERS =================
EMOTIONS = {
    "🌿 هادئ": ["without noise", "without display"],
    "🕊️ تأملي": ["carried quietly", "remembered softly"],
    "🔥 مؤثر": ["deeply felt", "clearly present"],
    "⏳ خارج الزمن": ["beyond time", "outside timelines"]
}

# ================= HASHTAG ROLES =================
HASHTAGS = {
    "identity": ["#Palestine", "#PalestinianIdentity"],
    "memory": ["#Memory", "#PalestinianMemory"],
    "history": ["#History", "#HistoricalRecord"],
    "culture": ["#Heritage", "#Culture"],
    "brand": ["#Hatshepsut"]
}

CATEGORY_TAG_MAP = {
    "palestine": ["identity","culture","brand"],
    "gaza": ["identity","memory","brand"],
    "maps": ["history","memory","brand"],
    "memory": ["memory","culture","brand"],
    "nakba": ["memory","history","brand"]
}

# ================= UTIL =================
def contains_blocked(text):
    t = text.lower()
    return any(w in t for w in BLOCKED_WORDS)

def mix_hashtags(category):
    roles = CATEGORY_TAG_MAP[category]
    tags = []
    for r in roles:
        tags.append(random.choice(HASHTAGS[r]))
    return " ".join(tags)

# ================= HOOK ENGINE =================
def generate_hook(category, emotion):
    for _ in range(15):
        opening = random.choice(OPENINGS[category])
        core = random.choice(CORE_IDEAS[category])
        contrast = random.choice(CONTRASTS)
        emotion_line = random.choice(EMOTIONS[emotion])
        emoji = random.choice(EMOJIS)

        line1 = f"{opening} {core}"
        line2 = contrast if contrast else emotion_line
        line3 = f"remembered as Palestinian identity"

        text = f"{line1},\n{line2},\n{line3}. {emoji}"

        if not contains_blocked(text):
            return f"<code>{text}\n\n{mix_hashtags(category)}</code>"

    return "<code>Content could not be generated safely.</code>"

# ================= KEYBOARDS =================
def category_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    for k,v in CATEGORIES.items():
        kb.add(InlineKeyboardButton(v, callback_data=f"cat|{k}"))
    return kb

def emotion_menu(category):
    kb = InlineKeyboardMarkup(row_width=2)
    for e in EMOTIONS.keys():
        kb.add(InlineKeyboardButton(e, callback_data=f"emo|{category}|{e}"))
    return kb

def action_menu(category, emotion):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 توليد مرة تانية", callback_data=f"again|{category}|{emotion}"),
        InlineKeyboardButton("👍 قوي", callback_data="rate|up"),
        InlineKeyboardButton("👎 ضعيف", callback_data="rate|down")
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🇵🇸 اختار القسم:",
        reply_markup=category_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    data = call.data.split("|")

    if data[0] == "cat":
        bot.edit_message_text(
            "🎭 اختار الإحساس:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=emotion_menu(data[1])
        )

    elif data[0] == "emo":
        _, category, emotion = data
        text = generate_hook(category, emotion)
        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=action_menu(category, emotion)
        )

    elif data[0] == "again":
        _, category, emotion = data
        text = generate_hook(category, emotion)
        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=action_menu(category, emotion)
        )

    elif data[0] == "rate":
        bot.answer_callback_query(call.id, "✔️ تم تسجيل رأيك")

# ================= RUN =================
print("🇵🇸 Palestinian Hook Engine running...")
bot.infinity_polling(skip_pending=True)
