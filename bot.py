# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import re

# ================= BOT =================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= BLOCKED ROOTS =================
BLOCKED_PATTERNS = [
    r"viol", r"conflict", r"resist", r"occup",
    r"zion", r"israel", r"jew",
    r"kill", r"bomb", r"attack",
    r"destroy", r"missil", r"rocket",
    r"fraud", r"scam"
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

# ================= HOOK ENGINE WITH TONES =================
HOOK_ENGINE = {
    "palestine": {
        "neutral": {
            "l1": ["Palestine exists beyond headlines"],
            "l2": ["it represents continuity, memory, and identity"],
            "l3": ["and its presence remains undeniable"]
        },
        "emotional": {
            "l1": ["Palestine was never easy to forget"],
            "l2": ["it lives quietly inside memory and belonging"],
            "l3": ["and that feeling refuses to disappear"]
        },
        "documentary": {
            "l1": ["Palestine is documented across history"],
            "l2": ["through records, culture, and lived experience"],
            "l3": ["forming an uninterrupted narrative"]
        },
        "viral": {
            "l1": ["Palestine was never a trend"],
            "l2": ["it was always a reality ignored too often"],
            "l3": ["and that truth still stands"]
        }
    },

    "gaza": {
        "neutral": {
            "l1": ["Gaza exists beyond daily headlines"],
            "l2": ["it reflects ordinary life under constant pressure"],
            "l3": ["where meaning continues quietly"]
        },
        "emotional": {
            "l1": ["Gaza carries stories few hear"],
            "l2": ["where endurance becomes a language"],
            "l3": ["and humanity stays visible"]
        },
        "documentary": {
            "l1": ["Gaza represents lived human reality"],
            "l2": ["documented through daily survival and resilience"],
            "l3": ["forming a continuous human record"]
        },
        "viral": {
            "l1": ["Gaza was never what screens showed"],
            "l2": ["it was always what cameras avoided"],
            "l3": ["and that silence speaks loudly"]
        }
    },

    "maps": {
        "neutral": {
            "l1": ["This historical map of Palestine records geography"],
            "l2": ["drawn long before modern narratives"],
            "l3": ["preserving memory through lines"]
        },
        "emotional": {
            "l1": ["This historical map carries memory"],
            "l2": ["where every line reflects belonging"],
            "l3": ["and history breathes quietly"]
        },
        "documentary": {
            "l1": ["This historical map of Palestine documents land"],
            "l2": ["through verified names and locations"],
            "l3": ["forming visual historical evidence"]
        },
        "viral": {
            "l1": ["This historical map shows what time couldn't erase"],
            "l2": ["a land drawn before reinterpretation"],
            "l3": ["and truth preserved on paper"]
        }
    },

    "nakba": {
        "neutral": {
            "l1": ["The Nakba remains a defining historical moment"],
            "l2": ["that reshaped lives and everyday reality"],
            "l3": ["with lasting consequences"]
        },
        "emotional": {
            "l1": ["The Nakba lives quietly in memory"],
            "l2": ["carried across generations"],
            "l3": ["where loss became shared experience"]
        },
        "documentary": {
            "l1": ["The Nakba is recorded through testimonies"],
            "l2": ["documenting widespread displacement"],
            "l3": ["as a lasting historical reference"]
        },
        "viral": {
            "l1": ["The Nakba was never just a date"],
            "l2": ["it marked a shift in lived reality"],
            "l3": ["and its meaning still unfolds"]
        }
    }
}

TONES = ["neutral", "emotional", "documentary", "viral"]

# ================= SAFETY =================
def is_safe(text):
    t = text.lower()
    return not any(re.search(p, t) for p in BLOCKED_PATTERNS)

# ================= GENERATOR =================
def generate_hook(category, tone):
    data = HOOK_ENGINE[category][tone]

    for _ in range(10):
        l1 = random.choice(data["l1"])
        l2 = random.choice(data["l2"])
        l3 = random.choice(data["l3"])

        text = f"{l1}\n{l2}\n{l3}"

        if is_safe(text):
            emoji = random.choice(EMOJIS)
            tags = " ".join(random.sample(HASHTAGS[category], 2))
            return f"{text}\n{tags} #Hatshepsut {emoji}"

    return "Content could not be generated safely."

# ================= TRANSLATION (FULL & CLEAN) =================
AR_TRANSLATIONS = {
    "Palestine exists beyond headlines": "فلسطين تتجاوز العناوين",
    "Palestine was never a trend": "فلسطين لم تكن يومًا ترند",
    "Gaza exists beyond daily headlines": "غزة تتجاوز العناوين اليومية",
    "This historical map of Palestine": "هذه خريطة تاريخية لفلسطين",
    "The Nakba": "النكبة"
}

def translate_full(text):
    lines = text.split("\n")
    translated = []

    for line in lines:
        for en, ar in AR_TRANSLATIONS.items():
            if line.startswith(en):
                line = line.replace(en, ar)
        translated.append(line)

    return "\n".join(translated)

# ================= KEYBOARDS =================
def tone_menu(lang, category):
    kb = InlineKeyboardMarkup(row_width=2)
    for t in TONES:
        kb.add(InlineKeyboardButton(t.capitalize(), callback_data=f"gen|{lang}|{category}|{t}"))
    return kb

def action_menu(lang, category, tone, text):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{lang}|{category}|{tone}"),
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
        lang = data[1]
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("🇵🇸 Palestine", callback_data=f"cat|{lang}|palestine"),
            InlineKeyboardButton("🔥 Gaza", callback_data=f"cat|{lang}|gaza"),
            InlineKeyboardButton("🗺️ Maps", callback_data=f"cat|{lang}|maps"),
            InlineKeyboardButton("🕊️ Nakba", callback_data=f"cat|{lang}|nakba")
        )
        bot.send_message(call.message.chat.id, "Choose category:", reply_markup=kb)

    elif data[0] == "cat":
        _, lang, category = data
        bot.send_message(call.message.chat.id, "Choose tone:", reply_markup=tone_menu(lang, category))

    elif data[0] in ["gen", "again"]:
        _, lang, category, tone = data
        text = generate_hook(category, tone)
        if lang == "ar":
            text = translate_full(text)
        bot.send_message(call.message.chat.id, text, reply_markup=action_menu(lang, category, tone, text))

# ================= RUN =================
print("Bot is running clean and stable...")
bot.infinity_polling(skip_pending=True)
