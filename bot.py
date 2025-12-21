# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

# ================= BOT =================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ================= BLOCKED WORDS =================
BLOCKED_WORDS = [
    "conflict", "violence", "resistance", "occupation",
    "zion", "zionist", "jewish", "israel", "israeli",
    "catastrophe", "attack", "kill", "killing", "bomb",
    "fight", "fighting", "seizure", "displacement",
    "destruction", "destroy", "missile", "rocket",
    "fraud", "scam", "steadfastness"
]

# ================= EMOJIS =================
EMOJIS = ["🇵🇸", "🕊️", "🌿", "📜", "🗺️", "⏳", "✨"]

# ================= HASHTAGS =================
HASHTAGS = {
    "palestine": ["#Palestine", "#FreePalestine", "#PalestinianIdentity"],
    "gaza": ["#Gaza", "#HumanStories", "#VoicesFromGaza"],
    "maps": ["#HistoricalMaps", "#PalestineHistory", "#Cartography"],
    "nakba": ["#Nakba", "#HistoricalMemory", "#CollectiveMemory"]
}

# ================= HOOKS =================
HOOKS = {
    "palestine": {
        "start": "Palestine",
        "neutral": [
            "exists beyond headlines and narratives",
            "remains a reality preserved through time"
        ],
        "emotional": [
            "lives deeply in memory and belonging",
            "breathes through identity and remembrance"
        ],
        "documentary": [
            "is recorded through culture and history",
            "is documented across generations"
        ],
        "viral": [
            "is not a trend, it is a truth",
            "is a story the world keeps missing"
        ]
    },

    "gaza": {
        "start": "Gaza",
        "neutral": [
            "continues through resilience and patience",
            "exists beyond daily headlines"
        ],
        "emotional": [
            "holds stories written in endurance",
            "carries strength through hardship"
        ],
        "documentary": [
            "reflects human persistence under pressure",
            "records daily life beyond statistics"
        ],
        "viral": [
            "is more than what you are told",
            "is not what headlines reduce it to"
        ]
    },

    "maps": {
        "start": "This historical map of Palestine",
        "neutral": [
            "preserves geography drawn long ago",
            "documents land before modern narratives"
        ],
        "emotional": [
            "carries memory in every line",
            "holds stories beyond ink and paper"
        ],
        "documentary": [
            "records places as they once existed",
            "stands as visual historical evidence"
        ],
        "viral": [
            "reveals what time could not erase",
            "shows history without commentary"
        ]
    },

    "nakba": {
        "start": "The Nakba",
        "neutral": [
            "remains a defining historical moment",
            "left an enduring impact on identity"
        ],
        "emotional": [
            "lives quietly within collective memory",
            "left echoes carried across generations"
        ],
        "documentary": [
            "is documented through testimonies and history",
            "marks a turning point in lived experience"
        ],
        "viral": [
            "was not just a date in history",
            "is more than a chapter in books"
        ]
    }
}

TONES = ["neutral", "emotional", "documentary", "viral"]

# ================= UTILITIES =================
def contains_blocked(text):
    lower = text.lower()
    return any(word in lower for word in BLOCKED_WORDS)

def generate_hook(category, tone):
    data = HOOKS[category]
    emoji = random.choice(EMOJIS)

    for _ in range(10):  # retries to avoid blocked words
        line1 = f"{data['start']} {random.choice(data[tone])}"
        line2 = "A perspective shaped by memory and continuity"
        line3 = "A story that remains present through time"

        text = f"{emoji} {line1}\n{line2}\n{line3}"
        if not contains_blocked(text):
            tags = " ".join(random.sample(HASHTAGS[category], 2))
            return f"{text}\n{tags} #Hatshepsut"

    return "Content could not be generated safely."

# ================= KEYBOARDS =================
def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🇵🇸 Palestine", callback_data="palestine"),
        InlineKeyboardButton("🔥 Gaza", callback_data="gaza"),
        InlineKeyboardButton("🗺️ Historical Maps", callback_data="maps"),
        InlineKeyboardButton("🕊️ Nakba", callback_data="nakba"),
        InlineKeyboardButton("🎲 Surprise Me", callback_data="surprise")
    )
    return kb

def tone_menu(category):
    kb = InlineKeyboardMarkup(row_width=2)
    for tone in TONES:
        kb.add(
            InlineKeyboardButton(
                tone.capitalize(),
                callback_data=f"tone|{category}|{tone}"
            )
        )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Choose a category:",
        reply_markup=main_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    try:
        if call.data == "surprise":
            category = random.choice(list(HOOKS.keys()))
            tone = random.choice(TONES)
            text = generate_hook(category, tone)
            bot.send_message(call.message.chat.id, text)
            return

        if call.data in HOOKS:
            bot.send_message(
                call.message.chat.id,
                "Choose a tone:",
                reply_markup=tone_menu(call.data)
            )
            return

        if call.data.startswith("tone|"):
            _, category, tone = call.data.split("|")
            text = generate_hook(category, tone)
            bot.send_message(call.message.chat.id, text)
            return

    except Exception as e:
        print("ERROR:", e)

# ================= RUN =================
print("Bot is running safely...")
bot.infinity_polling(skip_pending=True)
