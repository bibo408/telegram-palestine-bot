# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

# ================= BOT TOKEN =================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ================= DATA =================
DATA = {
    "nakba": {
        "emoji": "🕊️",
        "line1": [
            "A story shaped by memory and loss",
            "History carries voices from the past",
            "A moment that changed countless lives",
            "Memories that time could not erase"
        ],
        "line2": [
            "Identity remained stronger than displacement",
            "Roots stayed alive despite hardship",
            "Belonging was never erased",
            "Hope survived across generations"
        ]
    },

    "beauty": {
        "emoji": "🌿",
        "line1": [
            "Nature reflects deep cultural heritage",
            "Landscapes carry quiet beauty",
            "Every corner holds timeless charm",
            "The land speaks through its beauty"
        ],
        "line2": [
            "Hope grows through generations",
            "Beauty survives every challenge",
            "Life continues with grace",
            "Peace lives within the land"
        ]
    },

    "maps": {
        "emoji": "🗺️",
        "line1": [
            "Old maps reveal historical truth",
            "Cartography preserves forgotten names",
            "History speaks through preserved lines",
            "Maps tell stories beyond borders"
        ],
        "line2": [
            "Geography cannot erase identity",
            "Time cannot remove heritage",
            "Memory remains stronger than borders",
            "History remembers what maps show"
        ]
    },

    "gaza": {
        "emoji": "🔥",
        "line1": [
            "A place defined by resilience",
            "Strength rises through adversity",
            "Human spirit stands firm",
            "Courage lives in every heart"
        ],
        "line2": [
            "Hope survives difficult moments",
            "Dignity remains unbroken",
            "Life continues with courage",
            "Humanity shines through hardship"
        ]
    }
}

# ================= MEMORY =================
used_texts = set()

# ================= GENERATOR =================
def generate_text(category):
    d = DATA.get(category)

    if not d:
        return "❌ Invalid category"

    attempts = 0
    while attempts < 30:
        l1 = random.choice(d["line1"])
        l2 = random.choice(d["line2"])
        text = f"{d['emoji']} {l1}\n{l2}\nPalestine remains 🇵🇸"

        if text not in used_texts:
            used_texts.add(text)
            return text

        attempts += 1

    return "⚠️ All phrases for this category have been used."

# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton("🕊️ NAKBA 🇵🇸", callback_data="nakba"),
        InlineKeyboardButton("🌿 Beautiful Palestine 🇵🇸", callback_data="beauty"),
        InlineKeyboardButton("🗺️ Historical Maps 🇵🇸", callback_data="maps"),
        InlineKeyboardButton("🔥 GAZA 🇵🇸", callback_data="gaza")
    )

    bot.send_message(
        message.chat.id,
        "🇵🇸 Choose a category:",
        reply_markup=keyboard
    )

# ================= CALLBACK =================
@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    category = call.data
    text = generate_text(category)

    bot.send_message(call.message.chat.id, text)
    bot.answer_callback_query(call.id)

# ================= RUN =================
print("Bot is running...")
bot.infinity_polling()
