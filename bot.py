# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

# ================= BOT =================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ================= EMOJIS =================
EMOJIS = ["🇵🇸", "🔥", "🕊️", "🗺️", "⏳", "📜", "💔", "🌿", "✊"]

# ================= HOOK PARTS =================
HOOKS = {
    "palestine": {
        "start": "Palestine",
        "line1": [
            "is not a headline, it is a reality the world keeps overlooking",
            "is more than a place, it is a story still being written",
            "exists beyond politics, borders, and narratives",
            "remains a truth no distortion can erase"
        ],
        "line2": [
            "where identity survives every attempt of erasure",
            "where history refuses to stay silent",
            "where memory outlives occupation",
            "where roots remain stronger than force"
        ],
        "line3": [
            "and the story continues despite everything",
            "and its name still echoes across generations",
            "and its existence remains undeniable",
            "and its people never disappeared"
        ]
    },

    "gaza": {
        "start": "Gaza",
        "line1": [
            "is not just a conflict zone, it is a human reality",
            "is not statistics, it is lives interrupted",
            "is not a breaking news alert, it is daily survival",
            "is not silence, even when the world looks away"
        ],
        "line2": [
            "where resilience is practiced, not preached",
            "where endurance becomes a way of life",
            "where strength is born from loss",
            "where humanity persists under pressure"
        ],
        "line3": [
            "and dignity remains unbroken",
            "and hope refuses to disappear",
            "and life continues against all odds",
            "and voices still rise from the ruins"
        ]
    },

    "maps": {
        "start": "This historical map of Palestine",
        "line1": [
            "reveals a geography that predates modern narratives",
            "documents names and borders that once existed",
            "stands as visual evidence of recorded history",
            "preserves a land long before political manipulation"
        ],
        "line2": [
            "where cities, villages, and identities are clearly marked",
            "where memory is drawn in ink, not erased by time",
            "where history is measured by truth, not power",
            "where the past refuses to be rewritten"
        ],
        "line3": [
            "and maps tell stories words cannot silence",
            "and cartography exposes forgotten realities",
            "and history remains visible for those who look",
            "and truth survives within preserved lines"
        ]
    },

    "nakba": {
        "start": "The Nakba",
        "line1": [
            "was not a single moment, but a lasting trauma",
            "marked the beginning of widespread displacement",
            "reshaped countless lives overnight",
            "left scars that time could not heal"
        ],
        "line2": [
            "where families were separated from their homes",
            "where loss became a shared memory",
            "where survival replaced normal life",
            "where identity was tested but not erased"
        ],
        "line3": [
            "and its impact continues across generations",
            "and its memory remains deeply rooted",
            "and its consequences are still felt today",
            "and its story demands to be remembered"
        ]
    }
}

# ================= GENERATOR =================
def generate_hook(category):
    data = HOOKS.get(category)
    emoji = random.choice(EMOJIS)

    line1 = f"{data['start']} {random.choice(data['line1'])}"
    line2 = random.choice(data['line2'])
    line3 = random.choice(data['line3'])

    hashtags = "#Hatshepsut #Palestine"

    return f"{emoji} {line1}\n{line2}\n{line3}\n{hashtags}"

# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🇵🇸 Palestine", callback_data="palestine"),
        InlineKeyboardButton("🔥 Gaza", callback_data="gaza"),
        InlineKeyboardButton("🗺️ Historical Maps", callback_data="maps"),
        InlineKeyboardButton("🕊️ Nakba", callback_data="nakba")
    )

    bot.send_message(
        message.chat.id,
        "Choose a category:",
        reply_markup=keyboard
    )

# ================= CALLBACK =================
@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    hook_text = generate_hook(call.data)

    # Send main hook
    bot.send_message(call.message.chat.id, hook_text)

    # Send signature message automatically after
    bot.send_message(
        call.message.chat.id,
        "مع تحيات بشمهندس بيبو\nوشريكه محمد مختار"
    )

    bot.answer_callback_query(call.id)

# ================= RUN =================
print("Bot is running...")
bot.infinity_polling()
