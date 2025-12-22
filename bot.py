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

# ================= CATEGORIES =================
CATEGORIES = {
    "palestine": "🇵🇸 فلسطين",
    "gaza": "🔥 غزة",
    "maps": "🗺️ خرائط فلسطين",
    "memory": "📜 الذاكرة الفلسطينية"
}

# ================= PALESTINIAN IDENTITY ANCHORS =================
IDENTITY_LINES = [
    "Palestine lives beyond borders and headlines.",
    "Palestinian identity is not a narrative — it is a reality.",
    "This is Palestine, remembered without permission.",
    "Gaza remains Palestinian in memory and presence.",
    "Palestine exists wherever its memory is carried."
]

# ================= HOOK STYLES =================
HOOK_STYLES = {
    "🎯 تصريح قوي": [
        "Some identities cannot be erased by time.",
        "Truth does not disappear when ignored."
    ],
    "❓ سؤال ذكي": [
        "What does history try — and fail — to silence?",
        "What remains when memory refuses to fade?"
    ],
    "🧠 توثيقي هادئ": [
        "Recorded quietly, preserved carefully.",
        "Archived without noise or commentary."
    ],
    "⚡ صدمة هادئة": [
        "No headline. No noise. Still remembered.",
        "Nothing dramatic — yet everything is permanent."
    ]
}

# ================= CORE MEANINGS =================
CORE_MEANINGS = {
    "palestine": [
        "A land carried through generations, not trends",
        "An identity preserved beyond time"
    ],
    "gaza": [
        "A Palestinian place defined by endurance",
        "Stories that exist beyond description"
    ],
    "maps": [
        "Palestinian geography drawn before narratives shifted",
        "Maps that remember Palestine clearly"
    ],
    "memory": [
        "A Palestinian memory passed without interruption",
        "History carried quietly across generations"
    ]
}

# ================= EMOTIONAL SLIDER =================
EMOTION_LEVELS = {
    "🌿 هادئ": {
        "suffix": ["Without noise.", "Without explanation."]
    },
    "🔥 متوسط": {
        "suffix": ["And it remains.", "And it continues."]
    },
    "⚡ عالي": {
        "suffix": ["Against time itself.", "Even now."]
    }
}

# ================= HASHTAG AI MIXER =================
HASHTAGS = {
    "palestine": ["#Palestine", "#PalestinianIdentity", "#Memory"],
    "gaza": ["#Gaza", "#PalestinianLife", "#Stories"],
    "maps": ["#PalestineMaps", "#HistoricalMemory", "#Cartography"],
    "memory": ["#PalestinianMemory", "#History", "#Identity"]
}

# ================= UTIL =================
def contains_blocked(text):
    t = text.lower()
    return any(w in t for w in BLOCKED_WORDS)

def mix_hashtags(category):
    base = HASHTAGS[category]
    return " ".join(random.sample(base, min(3, len(base))))

# ================= HOOK ENGINE =================
def generate_hook(category, style, emotion):
    for _ in range(10):
        identity = random.choice(IDENTITY_LINES)
        hook = random.choice(HOOK_STYLES[style])
        core = random.choice(CORE_MEANINGS[category])
        suffix = random.choice(EMOTION_LEVELS[emotion]["suffix"])
        emoji = random.choice(EMOJIS)

        text = f"{identity} {hook} {core}. {suffix} {emoji}"

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
    kb = InlineKeyboardMarkup(row_width=1)
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
        "🇵🇸 اختار القسم الفلسطيني:",
        reply_markup=category_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    data = call.data.split("|")

    if data[0] == "cat":
        bot.edit_message_text(
            "🎨 اختار أسلوب الجملة:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=style_menu(data[1])
        )

    elif data[0] == "style":
        bot.edit_message_text(
            "🎭 اختار مستوى الإحساس:",
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
        bot.answer_callback_query(call.id, "✔️ تم تسجيل رأيك")

# ================= RUN =================
print("🇵🇸 Palestinian Hook Engine is running...")
bot.infinity_polling(skip_pending=True)
