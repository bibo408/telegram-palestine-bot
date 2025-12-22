# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import re

# ================= BOT =================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= BLOCKED WORDS (regex roots) =================
BLOCKED_PATTERNS = [
    r"viol", r"conflict", r"resist", r"occup",
    r"zion", r"israel", r"jew",
    r"kill", r"bomb", r"attack", r"fight",
    r"destroy", r"missil", r"rocket",
    r"fraud", r"scam", r"catastroph"
]

# ================= EMOJIS =================
EMOJIS = ["🇵🇸", "🕊️", "🌿", "📜", "🗺️", "⏳", "✨"]

# ================= HASHTAGS =================
HASHTAGS = {
    "palestine": ["#Palestine", "#PalestinianIdentity", "#FreePalestine"],
    "gaza": ["#Gaza", "#HumanStories", "#LifeBeyondHeadlines"],
    "maps": ["#HistoricalMaps", "#PalestineMaps", "#Cartography"],
    "nakba": ["#Nakba", "#HistoricalMemory", "#CollectiveMemory"]
}

# ================= HOOK ENGINE =================
HOOK_ENGINE = {
    "palestine": {
        "openers": [
            "was never just a place,",
            "has always been more than borders,",
            "exists far beyond headlines,",
            "was never defined by narratives,"
        ],
        "cores": [
            "it is a truth many learned to overlook,",
            "it carries meaning deeper than geography,",
            "it lives where memory refuses silence,",
            "it stands where identity remains rooted,"
        ],
        "impacts": [
            "and that is why it still matters.",
            "and that reality continues unchanged.",
            "and that memory refuses to fade.",
            "and its presence remains undeniable."
        ]
    },

    "gaza": {
        "openers": [
            "was never what the screen reduced it to,",
            "exists beyond breaking news,",
            "was never a moment in time,",
            "has always been more than numbers,"
        ],
        "cores": [
            "it is a human story unfolding daily,",
            "it reflects life lived under pressure,",
            "it carries voices rarely heard,",
            "it reveals strength through endurance,"
        ],
        "impacts": [
            "and dignity remains present.",
            "and life continues quietly.",
            "and humanity stays visible.",
            "and meaning survives repetition."
        ]
    },

    "maps": {
        "openers": [
            "This historical map of Palestine reveals,",
            "This map quietly documents,",
            "This preserved cartography shows,",
            "This historical record reminds us,"
        ],
        "cores": [
            "a land drawn long before modern narratives,",
            "names and places recorded in time,",
            "geography untouched by reinterpretation,",
            "history measured in ink and memory,"
        ],
        "impacts": [
            "and maps speak without commentary.",
            "and the past remains visible.",
            "and truth stays documented.",
            "and memory resists erasure."
        ]
    },

    "nakba": {
        "openers": [
            "The Nakba was never a single event,",
            "The Nakba marked more than displacement,",
            "The Nakba reshaped countless lives,",
            "The Nakba remains a lasting memory,"
        ],
        "cores": [
            "it altered everyday life permanently,",
            "it left traces across generations,",
            "it redefined belonging and loss,",
            "it became a shared human experience,"
        ],
        "impacts": [
            "and its memory continues today.",
            "and its meaning remains present.",
            "and its impact is still felt.",
            "and its story asks to be remembered."
        ]
    }
}

TONES = ["neutral", "emotional", "documentary", "viral"]

# ================= SAFETY =================
def is_safe(text):
    lower = text.lower()
    return not any(re.search(p, lower) for p in BLOCKED_PATTERNS)

# ================= GENERATOR =================
def build_hook(category):
    engine = HOOK_ENGINE[category]
    opener = random.choice(engine["openers"])
    core = random.choice(engine["cores"])
    impact = random.choice(engine["impacts"])

    lines = random.choice([
        [opener, core + " " + impact],
        [opener, core, impact]
    ])

    text = "\n".join(lines)
    return text

def generate_hook(category):
    for _ in range(15):
        text = build_hook(category)
        if is_safe(text):
            emoji = random.choice(EMOJIS)
            tags = " ".join(random.sample(HASHTAGS[category], 2))
            return f"{text}\n{tags} #Hatshepsut {emoji}"
    return "Content could not be generated safely."

# ================= TRANSLATION (FULL TEXT) =================
TRANSLATION_MAP = {
    "Palestine": "فلسطين",
    "This historical map of Palestine": "هذه خريطة تاريخية لفلسطين",
    "The Nakba": "النكبة",
    "was never": "لم تكن يومًا",
    "exists beyond": "تتجاوز",
    "it is": "إنها",
    "and": "و",
    "memory": "الذاكرة",
    "history": "التاريخ",
    "truth": "الحقيقة",
    "life": "الحياة"
}

def translate_full(text):
    translated = text
    for en, ar in TRANSLATION_MAP.items():
        translated = translated.replace(en, ar)
    return translated

# ================= KEYBOARDS =================
def main_menu(lang):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🇵🇸 Palestine", callback_data=f"gen|{lang}|palestine"),
        InlineKeyboardButton("🔥 Gaza", callback_data=f"gen|{lang}|gaza"),
        InlineKeyboardButton("🗺️ Historical Maps", callback_data=f"gen|{lang}|maps"),
        InlineKeyboardButton("🕊️ Nakba", callback_data=f"gen|{lang}|nakba"),
        InlineKeyboardButton("🎲 Surprise Me", callback_data=f"surprise|{lang}")
    )
    return kb

def action_menu(lang, category, text):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{lang}|{category}"),
        InlineKeyboardButton("📋 Copy", switch_inline_query_current_chat=text)
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(message):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🌍 English", callback_data="lang|en"),
        InlineKeyboardButton("🌍 عربي", callback_data="lang|ar")
    )
    bot.send_message(message.chat.id, "Choose language / اختر اللغة:", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    data = call.data.split("|")

    if data[0] == "lang":
        bot.send_message(call.message.chat.id, "Choose category:", reply_markup=main_menu(data[1]))

    elif data[0] == "gen":
        lang, category = data[1], data[2]
        text = generate_hook(category)
        if lang == "ar":
            text = translate_full(text)
        bot.send_message(call.message.chat.id, text, reply_markup=action_menu(lang, category, text))

    elif data[0] == "again":
        lang, category = data[1], data[2]
        text = generate_hook(category)
        if lang == "ar":
            text = translate_full(text)
        bot.send_message(call.message.chat.id, text, reply_markup=action_menu(lang, category, text))

    elif data[0] == "surprise":
        lang = data[1]
        category = random.choice(list(HOOK_ENGINE.keys()))
        text = generate_hook(category)
        if lang == "ar":
            text = translate_full(text)
        bot.send_message(call.message.chat.id, text, reply_markup=action_menu(lang, category, text))

# ================= RUN =================
print("Bot is running smoothly...")
bot.infinity_polling(skip_pending=True)
