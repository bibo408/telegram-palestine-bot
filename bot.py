# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import openai

# ================= TELEGRAM & OPENAI KEYS =================
TOKEN = os.getenv("BOT_TOKEN")        # تيليجرام
OPENAI_KEY = os.getenv("OPENAI_KEY")  # OpenAI GPT-5
openai.api_key = OPENAI_KEY

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= BLOCKED WORDS =================
BLOCKED = [
    "conflict","violence","violent","resistance","occupation",
    "zion","zionist","jewish","israel","israeli",
    "attack","kill","bomb","destroy","rocket","missile",
    "fraud","scam"
]

def safe(text):
    t = text.lower()
    return not any(w in t for w in BLOCKED)

# ================= USER HISTORY =================
USER_HISTORY = {}

def seen_before(uid, key):
    if uid not in USER_HISTORY:
        USER_HISTORY[uid] = set()
    return key in USER_HISTORY[uid]

def remember(uid, key):
    USER_HISTORY[uid].add(key)

# ================= CATEGORIES =================
CATEGORIES = {
    "palestine": "🇵🇸 فلسطين",
    "gaza": "🔥 غزة",
    "maps": "🗺️ خرائط فلسطين",
    "memory": "📜 الذاكرة الفلسطينية",
    "nakba": "🕊️ النكبة وأحداثها"
}

# ================= MOODS =================
MOODS = {
    "🧠 هادئ توثيقي": "calm",
    "⚡ مكثف عميق": "intense",
    "✨ تأملي إنساني": "reflective"
}

# ================= GPT-5 HOOK GENERATOR =================
def generate_hook_gpt(uid, category, mood):
    prompt = f"""
Write a short social media post in English (2-3 lines) about {category}.
Mood: {mood}.
Include Palestinian identity, emojis, and hashtags.
Avoid any mention of violence, military, or sensitive words.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-5-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.7,
            max_tokens=150
        )
        text = response['choices'][0]['message']['content'].strip()
        key = f"{uid}|{category}|{mood}|{text}"
        if seen_before(uid, key) or not safe(text):
            return "Could not generate safe content."
        remember(uid, key)
        return f"<code>{text}</code>"
    except Exception as e:
        print("GPT Error:", e)
        return "<code>Error generating content</code>"

# ================= KEYBOARDS =================
def categories_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    for k,v in CATEGORIES.items():
        kb.add(InlineKeyboardButton(v, callback_data=f"cat|{k}"))
    return kb

def mood_kb(category):
    kb = InlineKeyboardMarkup(row_width=1)
    for m in MOODS.keys():
        kb.add(InlineKeyboardButton(m, callback_data=f"mood|{category}|{m}"))
    return kb

def again_kb(category, mood):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{category}|{mood}")
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(
        m.chat.id,
        "🇵🇸 اختار القسم:",
        reply_markup=categories_kb()
    )

@bot.callback_query_handler(func=lambda c: True)
def handle(c):
    data = c.data.split("|")
    uid = c.from_user.id

    if data[0] == "cat":
        bot.send_message(
            c.message.chat.id,
            "🎭 اختار النبرة:",
            reply_markup=mood_kb(data[1])
        )

    elif data[0] == "mood":
        _, category, mood = data
        text = generate_hook_gpt(uid, category, mood)
        bot.send_message(
            c.message.chat.id,
            text,
            reply_markup=again_kb(category, mood)
        )

    elif data[0] == "again":
        _, category, mood = data
        text = generate_hook_gpt(uid, category, mood)
        bot.send_message(
            c.message.chat.id,
            text,
            reply_markup=again_kb(category, mood)
        )

# ================= RUN =================
print("🇵🇸 GPT-5 Palestinian Hook Engine running...")
bot.infinity_polling(skip_pending=True)
