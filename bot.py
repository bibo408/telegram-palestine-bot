# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import time
import hashlib

TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN)

# ================= EMOJIS =================
EMOJIS = {
    "palestine": ["🇵🇸", "🌿", "🕊️", "✨"],
    "gaza": ["🔥", "🕯️", "🩸", "✊"],
    "maps": ["🗺️", "📜", "🧭", "🕰️"],
    "nakba": ["🕊️", "🖤", "🕯️", "⏳"]
}

# ================= TEXT BUILDERS =================
def unique_seed():
    return hashlib.md5(str(time.time()).encode()).hexdigest()[:6]

def generate_hook(category):
    emoji = random.choice(EMOJIS[category])
    seed = unique_seed()

    if category == "palestine":
        lines = [
            f"Palestine is not a headline, it is a living truth {emoji}",
            f"Palestine carries history in every stone and breath",
            f"Palestine remains, no matter how long the road feels"
        ]

    elif category == "gaza":
        lines = [
            f"Gaza speaks through resilience, not ruins {emoji}",
            f"Gaza turns pain into endurance, every single day",
            f"Gaza stands, even when the world looks away"
        ]

    elif category == "maps":
        lines = [
            f"This is a historical map of Palestine, not a forgotten sketch {emoji}",
            f"Old maps preserve names erased by modern borders",
            f"History survives wherever Palestine is remembered"
        ]

    elif category == "nakba":
        lines = [
            f"The Nakba was not a moment, it was a lasting wound {emoji}",
            f"The Nakba reshaped lives without erasing identity",
            f"The Nakba remains a testimony written in memory"
        ]

    random.shuffle(lines)

    text = "\n".join(lines)
    text += "\n\n#Hatshepsut #Palestine"

    return text

# ================= KEYBOARDS =================
def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🇵🇸 Palestine", callback_data="palestine"),
        InlineKeyboardButton("🔥 Gaza", callback_data="gaza"),
        InlineKeyboardButton("🗺️ Historical Maps", callback_data="maps"),
        InlineKeyboardButton("🕊️ Nakba", callback_data="nakba"),
    )
    return kb

def action_buttons(category):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{category}"),
        InlineKeyboardButton("📋 Copy Text", callback_data="copy")
    )
    return kb

# ================= BOT HANDLERS =================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Choose a category to generate a powerful hook 🇵🇸",
        reply_markup=main_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data in ["palestine", "gaza", "maps", "nakba"]:
        text = generate_hook(call.data)
        bot.send_message(call.message.chat.id, text, reply_markup=action_buttons(call.data))
        bot.send_message(
            call.message.chat.id,
            "مع تحيات بشمهندس بيبو\nوشريكه محمد مختار"
        )

    elif call.data.startswith("again"):
        category = call.data.split("|")[1]
        text = generate_hook(category)
        bot.send_message(call.message.chat.id, text, reply_markup=action_buttons(category))
        bot.send_message(
            call.message.chat.id,
            "مع تحيات بشمهندس بيبو\nوشريكه محمد مختار"
        )

    elif call.data == "copy":
        bot.send_message(
            call.message.chat.id,
            "📋 You can now copy the previous text easily."
        )

# ================= RUN =================
print("Bot is running...")
bot.infinity_polling()
