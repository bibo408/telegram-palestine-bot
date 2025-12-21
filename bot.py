# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= DATA =================
DATA = {
    "palestine": {
        "start": "Palestine",
        "emoji": ["🇵🇸", "🌿", "🕊️", "✨"],
        "lines1": [
            "is not a trending topic, it is a living truth",
            "is more than a place, it is an identity",
            "exists beyond headlines and timelines",
            "remains present in every generation"
        ],
        "lines2": [
            "carried through memory, land, and belonging",
            "protected by history and human will",
            "written into culture and consciousness",
            "preserved through resilience and time"
        ],
        "lines3": [
            "and its story continues, uninterrupted",
            "despite everything meant to erase it",
            "as a constant, not a question",
            "as a reality that endures"
        ]
    },

    "gaza": {
        "start": "Gaza",
        "emoji": ["🔥", "🕯️", "✊", "🩸"],
        "lines1": [
            "speaks through resilience, not destruction",
            "is defined by strength, not statistics",
            "stands through hardship and silence",
            "continues despite relentless pressure"
        ],
        "lines2": [
            "where humanity persists under strain",
            "where endurance becomes a language",
            "where life insists on existing",
            "where dignity refuses to collapse"
        ],
        "lines3": [
            "and its people remain unbroken",
            "without surrendering identity",
            "without losing their voice",
            "without fading into numbers"
        ]
    },

    "maps": {
        "start": "This historical map of Palestine",
        "emoji": ["🗺️", "📜", "🧭", "🕰️"],
        "lines1": [
            "documents a reality long before modern borders",
            "preserves names that time could not erase",
            "reveals a geography rooted in history",
            "records identity beyond political shifts"
        ],
        "lines2": [
            "where memory is drawn into every line",
            "where heritage exists beyond rebranding",
            "where place and people remain connected",
            "where truth is quietly preserved"
        ],
        "lines3": [
            "as evidence that history remembers",
            "as proof that maps can carry truth",
            "as a witness, not an opinion",
            "as a reminder of what existed"
        ]
    },

    "nakba": {
        "start": "The Nakba",
        "emoji": ["🕊️", "🖤", "🕯️", "⏳"],
        "lines1": [
            "marked a profound human displacement",
            "was a turning point in countless lives",
            "left an enduring impact on identity",
            "reshaped existence for generations"
        ],
        "lines2": [
            "without erasing memory or belonging",
            "while leaving scars carried through time",
            "yet failing to erase cultural roots",
            "but never eliminating identity"
        ],
        "lines3": [
            "and its story continues to be told",
            "as a lesson recorded in history",
            "as a memory preserved with dignity",
            "as a reality remembered, not repeated"
        ]
    }
}

# ================= FUNCTIONS =================
def generate_text(category):
    data = DATA[category]
    emoji = random.choice(data["emoji"])

    text = (
        f"{data['start']} {random.choice(data['lines1'])} {emoji}\n"
        f"{random.choice(data['lines2'])}\n"
        f"{random.choice(data['lines3'])}\n\n"
        "#Hatshepsut #Palestine"
    )
    return text

def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🇵🇸 Palestine", callback_data="palestine"),
        InlineKeyboardButton("🔥 Gaza", callback_data="gaza"),
        InlineKeyboardButton("🗺️ Historical Maps", callback_data="maps"),
        InlineKeyboardButton("🕊️ Nakba", callback_data="nakba")
    )
    return kb

def again_menu(category):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again:{category}")
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Choose a category to generate a powerful hook 🇵🇸",
        reply_markup=main_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        if call.data in DATA:
            category = call.data

        elif call.data.startswith("again:"):
            category = call.data.split(":")[1]
            if category not in DATA:
                return
        else:
            return

        text = generate_text(category)

        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=again_menu(category)
        )

        bot.send_message(
            call.message.chat.id,
            "مع تحيات بشمهندس بيبو\nوشريكه محمد مختار"
        )

    except Exception as e:
        # حماية أخيرة ضد أي كراش
        print("ERROR:", e)

# ================= RUN =================
print("Bot is running safely...")
bot.infinity_polling(skip_pending=True)
