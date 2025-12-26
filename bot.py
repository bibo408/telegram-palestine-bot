# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import openai

# ================= CONFIG =================
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
openai.api_key = OPENAI_KEY

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

# ================= CATEGORIES =================
CATEGORIES = {
    "palestine": "🇵🇸 فلسطين",
    "gaza": "🔥 غزة",
    "maps": "🗺️ خرائط فلسطين",
    "memory": "📜 الذاكرة الفلسطينية",
    "nakba": "🕊️ النكبة وأحداثها"
}

# ================= MOODS =================
MOODS = ["🧠 هادئ توثيقي", "⚡ مكثف عميق", "✨ تأملي إنساني"]

# ================= USER HISTORY =================
USER_HISTORY = {}

def seen_before(uid, text):
    if uid not in USER_HISTORY:
        USER_HISTORY[uid] = set()
    return text in USER_HISTORY[uid]

def remember(uid, text):
    USER_HISTORY[uid].add(text)

# ================= GPT-5 HOOK GENERATOR =================
def generate_hook_gpt(uid, category, mood):
    prompt = f"""
Generate a unique Palestinian hook sentence in English for social media.
Requirements:
1. Must reflect Palestinian identity clearly (mention Palestine, Gaza, Nakba, or related themes).
2. Mood: {mood}.
3. Keep it in 2-3 lines max.
4. Add 1-2 relevant emojis subtly.
5. Avoid any violent or forbidden words.
6. Make it original and not repetitive.
7. End with appropriate hashtags (#Palestine #PalestinianIdentity #Memory).

Output only the text, do not add extra instructions.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-5-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.7,
            max_tokens=150
        )
        text = response['choices'][0]['message']['content'].strip()
        if safe(text) and not seen_before(uid, text):
            remember(uid, text)
            return f"<code>{text}</code>"
        else:
            return "<code>Could not generate a safe unique hook.</code>"
    except Exception as e:
        return f"<code>Error generating hook: {e}</code>"

# ================= KEYBOARDS =================
def categories_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    for k, v in CATEGORIES.items():
        kb.add(InlineKeyboardButton(v, callback_data=f"cat|{k}"))
    return kb

def mood_kb(category):
    kb = InlineKeyboardMarkup(row_width=1)
    for m in MOODS:
        kb.add(InlineKeyboardButton(m, callback_data=f"mood|{category}|{m}"))
    return kb

def again_kb(category, mood):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{category}|{mood}"),
        InlineKeyboardButton("📋 Copy", callback_data=f"copy|{category}|{mood}")
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

    elif data[0] == "copy":
        bot.answer_callback_query(c.id, "Copied ✔️", show_alert=True)

# ================= RUN =================
print("🇵🇸 GPT-5 Palestinian Hook Engine running...")
bot.infinity_polling(skip_pending=True)
