# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")  # -100xxxxxxxxxx

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ================= MEMORY =================
LAST_HOOK = {}

# ================= BLOCKED WORDS =================
BLOCKED = [
    "conflict","violence","violent","resistance","occupation",
    "zion","zionist","jew","jewish","israel","israeli",
    "attack","kill","bomb","fight","destroy",
    "missile","rocket","fraud","scam","steadfast"
]

# ================= EMOJIS =================
EMOJIS = ["🇵🇸","🕊️","🌿","📜","🗺️","✨","⏳"]

# ================= HOOK ENGINE =================
HOOK_ENGINE = {
    "palestine": {
        "start": [
            "Palestine was never just a place",
            "Palestine has always been more than a name",
            "Palestine exists beyond every narrative",
        ],
        "core": [
            "it is an identity carried through memory",
            "it is a story written by presence not headlines",
            "it is a truth preserved by generations",
        ],
        "impact": [
            "and that is why it still lives",
            "and that is why it cannot disappear",
            "and that is why it remains undeniable",
        ]
    },
    "gaza": {
        "start": [
            "Gaza was never defined by silence",
            "Gaza has always spoken through endurance",
            "Gaza exists beyond what screens show",
        ],
        "core": [
            "it carries Palestinian identity in every detail",
            "it reflects a people rooted in presence",
            "it holds stories shaped by patience and memory",
        ],
        "impact": [
            "and its voice continues",
            "and its meaning remains",
            "and its presence cannot fade",
        ]
    },
    "maps": {
        "start": [
            "This historical map of Palestine proves one thing",
            "This map records Palestine as it always was",
            "This historical map speaks without commentary",
        ],
        "core": [
            "Palestinian cities and names drawn in history",
            "a Palestinian geography preserved on paper",
            "a land marked long before modern narratives",
        ],
        "impact": [
            "and maps remember what words deny",
            "and history remains visible",
            "and truth stays documented",
        ]
    },
    "nakba": {
        "start": [
            "The Nakba was not a single moment",
            "The Nakba reshaped Palestinian identity forever",
            "The Nakba lives beyond dates and timelines",
        ],
        "core": [
            "it altered Palestinian lives across generations",
            "it left memories carried quietly through time",
            "it changed homes but not belonging",
        ],
        "impact": [
            "and its memory still speaks",
            "and its weight is still felt",
            "and its story remains unfinished",
        ]
    }
}

# ================= HASHTAGS =================
HASHTAGS = {
    "palestine": ["#Palestine","#PalestinianIdentity","#Hatshepsut"],
    "gaza": ["#Gaza","#Palestine","#Hatshepsut"],
    "maps": ["#HistoricalPalestine","#Maps","#Hatshepsut"],
    "nakba": ["#Nakba","#PalestinianMemory","#Hatshepsut"]
}

# ================= UTIL =================
def blocked(text):
    t = text.lower()
    return any(w in t for w in BLOCKED)

def generate_hook(category):
    for _ in range(15):
        s = random.choice(HOOK_ENGINE[category]["start"])
        c = random.choice(HOOK_ENGINE[category]["core"])
        i = random.choice(HOOK_ENGINE[category]["impact"])
        emoji = random.choice(EMOJIS)

        hook = f"{s},\n{c},\n{i} {emoji}"

        if not blocked(hook):
            tags = " ".join(random.sample(HASHTAGS[category], 2))
            return f"<code>{hook}\n{tags}</code>"

    return "<code>Unable to generate safe content.</code>"

# ================= LOG =================
def send_log(user, hook, category, rating="Not rated"):
    if not LOG_CHANNEL_ID:
        return

    log = f"""
🇵🇸 <b>New Hook</b>

👤 <b>User:</b> {user.first_name}
🔗 <b>Username:</b> @{user.username if user.username else 'N/A'}
🆔 <b>ID:</b> {user.id}

📂 <b>Category:</b> {category}
⭐ <b>Rating:</b> {rating}

📝 <b>Hook:</b>
{hook}
"""
    bot.send_message(LOG_CHANNEL_ID, log)

# ================= KEYBOARDS =================
def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🇵🇸 فلسطين", callback_data="cat|palestine"),
        InlineKeyboardButton("🔥 غزة", callback_data="cat|gaza"),
        InlineKeyboardButton("🗺️ خرائط تاريخية", callback_data="cat|maps"),
        InlineKeyboardButton("🕊️ النكبة", callback_data="cat|nakba"),
    )
    return kb

def action_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data="again"),
        InlineKeyboardButton("👍", callback_data="rate|up"),
        InlineKeyboardButton("👎", callback_data="rate|down"),
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id, "اختر القسم ✨", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    user = call.from_user
    data = call.data.split("|")

    if data[0] == "cat":
        category = data[1]
        hook = generate_hook(category)

        LAST_HOOK[user.id] = {"hook": hook, "category": category}

        bot.send_message(call.message.chat.id, hook, reply_markup=action_menu())
        send_log(user, hook, category)

    elif data[0] == "again":
        last = LAST_HOOK.get(user.id)
        if last:
            hook = generate_hook(last["category"])
            LAST_HOOK[user.id]["hook"] = hook
            bot.send_message(call.message.chat.id, hook, reply_markup=action_menu())
            send_log(user, hook, last["category"])

    elif data[0] == "rate":
        last = LAST_HOOK.get(user.id)
        if last:
            rating = "👍 Strong" if data[1] == "up" else "👎 Weak"
            send_log(user, last["hook"], last["category"], rating)
            bot.answer_callback_query(call.id, "تم تسجيل التقييم ✔️")

# ================= RUN =================
print("Bot running...")
bot.infinity_polling(skip_pending=True)
