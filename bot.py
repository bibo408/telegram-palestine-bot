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
EMOJIS = ["✨","🌿","🕊️","⏳","📜","🌍"]

# ================= CATEGORIES =================
CATEGORIES = {
    "palestine": "فلسطين",
    "gaza": "غزة",
    "maps": "خرائط تاريخية",
    "nakba": "النكبة"
}

# ================= HOOK STYLES =================
HOOK_STYLES = {
    "سؤال": [
        "What remains when time refuses to erase the truth?",
        "Have you ever wondered what history chose to remember?"
    ],
    "تصريح قوي": [
        "This is not a story — it is a presence.",
        "Some truths do not fade with time."
    ],
    "مقارنة": [
        "What is written is not always what is remembered.",
        "Maps change, memory does not."
    ],
    "صدمة هادئة": [
        "No sound. No headline. Still remembered.",
        "Nothing dramatic — yet everything is permanent."
    ],
    "توثيقي": [
        "Recorded quietly. Preserved carefully.",
        "Archived beyond noise and commentary."
    ]
}

# ================= CORE MEANINGS =================
CORE_MEANINGS = {
    "palestine": [
        "A land carried through memory, not headlines",
        "An identity preserved beyond time"
    ],
    "gaza": [
        "A place defined by endurance, not description",
        "Stories that exist beyond what is shown"
    ],
    "maps": [
        "Lines that remember what time tried to change",
        "Geography drawn before narratives shifted"
    ],
    "nakba": [
        "A moment that reshaped memory forever",
        "History that continues without announcement"
    ]
}

# ================= EMOTIONAL SLIDER =================
EMOTION_LEVELS = {
    "هادئ": {
        "prefix": ["Quietly.", "Softly."],
        "suffix": ["Without noise.", "Without commentary."]
    },
    "متوسط": {
        "prefix": ["Still.", "Yet."],
        "suffix": ["And it remains.", "And it continues."]
    },
    "عالي": {
        "prefix": ["Unforgotten.", "Undeniable."],
        "suffix": ["Even now.", "Against time itself."]
    }
}

# ================= HASHTAG AI MIXER =================
HASHTAGS = {
    "palestine": {
        "safe": ["#Palestine", "#History", "#Identity"],
        "viral": ["#Truth", "#Memory", "#Land"],
        "niche": ["#CulturalMemory", "#RecordedHistory"]
    },
    "gaza": {
        "safe": ["#Gaza", "#HumanStories"],
        "viral": ["#Untold", "#BeyondHeadlines"],
        "niche": ["#DailyLife", "#SilentStories"]
    },
    "maps": {
        "safe": ["#HistoricalMaps", "#Cartography"],
        "viral": ["#VisualHistory"],
        "niche": ["#OldMaps", "#GeographicMemory"]
    },
    "nakba": {
        "safe": ["#Nakba", "#HistoricalMoment"],
        "viral": ["#CollectiveMemory"],
        "niche": ["#OralHistory"]
    }
}

# ================= UTIL =================
def contains_blocked(text):
    t = text.lower()
    return any(w in t for w in BLOCKED_WORDS)

def mix_hashtags(category):
    sets = HASHTAGS[category]
    result = []
    result += random.sample(sets["safe"], min(2, len(sets["safe"])))
    result += random.sample(sets["viral"], 1)
    result += random.sample(sets["niche"], 1)
    return " ".join(result)

# ================= HOOK ENGINE =================
def generate_hook(category, style, emotion):
    for _ in range(10):
        opening = random.choice(HOOK_STYLES[style])
        core = random.choice(CORE_MEANINGS[category])
        emo = EMOTION_LEVELS[emotion]
        prefix = random.choice(emo["prefix"])
        suffix = random.choice(emo["suffix"])
        emoji = random.choice(EMOJIS)

        text = f"{prefix} {opening} {core}. {suffix} {emoji}"

        if not contains_blocked(text):
            hashtags = mix_hashtags(category)
            return f"<code>{text}\n\n{hashtags}</code>"

    return "<code>Content could not be generated safely.</code>"

# ================= KEYBOARDS =================
def category_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    for k, v in CATEGORIES.items():
        kb.add(InlineKeyboardButton(v, callback_data=f"cat|{k}"))
    return kb

def style_menu(category):
    kb = InlineKeyboardMarkup(row_width=2)
    for s in HOOK_STYLES.keys():
        kb.add(InlineKeyboardButton(s, callback_data=f"style|{category}|{s}"))
    return kb

def emotion_menu(category, style):
    kb = InlineKeyboardMarkup(row_width=3)
    for e in EMOTION_LEVELS.keys():
        kb.add(InlineKeyboardButton(e, callback_data=f"emo|{category}|{style}|{e}"))
    return kb

def action_menu(category, style, emotion):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 توليد مرة تانية", callback_data=f"again|{category}|{style}|{emotion}"),
        InlineKeyboardButton("👍 قوي", callback_data="rate|up"),
        InlineKeyboardButton("👎 ضعيف", callback_data="rate|down")
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "اختار القسم:",
        reply_markup=category_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    data = call.data.split("|")

    if data[0] == "cat":
        bot.edit_message_text(
            "اختار نوع الهوك:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=style_menu(data[1])
        )

    elif data[0] == "style":
        bot.edit_message_text(
            "اختار مستوى الإحساس:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=emotion_menu(data[1], data[2])
        )

    elif data[0] == "emo":
        _, category, style, emotion = data
        text = generate_hook(category, style, emotion)
        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=action_menu(category, style, emotion)
        )

    elif data[0] == "again":
        _, category, style, emotion = data
        text = generate_hook(category, style, emotion)
        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=action_menu(category, style, emotion)
        )

    elif data[0] == "rate":
        bot.answer_callback_query(call.id, "تم تسجيل رأيك ✅")

# ================= RUN =================
print("Bot running with Intelligence Engine...")
bot.infinity_polling(skip_pending=True)
