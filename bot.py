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
    "conflict", "violence", "violent", "resistance", "occupation",
    "zion", "zionist", "jewish", "israel", "israeli",
    "attack", "kill", "bomb", "fight", "destroy",
    "missile", "rocket", "fraud", "scam", "steadfastness"
]

# ================= EMOJIS =================
EMOJIS = ["🇵🇸", "🕊️", "🌿", "📜", "🗺️", "⏳", "✨"]

# ================= HASHTAGS =================
HASHTAGS = {
    "palestine": ["#Palestine", "#PalestinianIdentity", "#FreePalestine"],
    "gaza": ["#Gaza", "#GazaStories", "#HumanStories"],
    "maps": ["#HistoricalMaps", "#PalestineMaps", "#Cartography"],
    "nakba": ["#Nakba", "#HistoricalMemory", "#CollectiveMemory"]
}

# ================= HOOKS =================
HOOKS = {
    "en": {
        "palestine": {
            "start": "Palestine",
            "neutral": ["exists beyond headlines and narratives", "remains a reality preserved through time"],
            "emotional": ["lives deeply in memory and belonging", "breathes through identity and remembrance"],
            "documentary": ["is recorded through culture and history", "is documented across generations"],
            "viral": ["is not a trend, it is a truth", "is a story the world keeps missing"]
        },
        "gaza": {
            "start": "Gaza",
            "neutral": ["continues through patience and endurance", "exists beyond daily headlines"],
            "emotional": ["holds stories written in endurance", "carries strength through hardship"],
            "documentary": ["reflects human persistence under pressure", "records daily life beyond statistics"],
            "viral": ["is more than what you are told", "is not what headlines reduce it to"]
        },
        "maps": {
            "start": "This historical map of Palestine",
            "neutral": ["preserves geography drawn long ago", "documents land before modern narratives"],
            "emotional": ["carries memory in every line", "holds stories beyond ink and paper"],
            "documentary": ["records places as they once existed", "stands as visual historical evidence"],
            "viral": ["reveals what time could not erase", "shows history without commentary"]
        },
        "nakba": {
            "start": "The Nakba",
            "neutral": ["remains a defining historical moment", "left an enduring impact on identity"],
            "emotional": ["lives quietly within collective memory", "left echoes carried across generations"],
            "documentary": ["is documented through testimonies and history", "marks a turning point in lived experience"],
            "viral": ["was not just a date in history", "is more than a chapter in books"]
        }
    },
    "ar": {
        "palestine": {
            "start": "فلسطين",
            "neutral": ["حقيقة قائمة تتجاوز العناوين", "واقع محفوظ عبر الزمن"],
            "emotional": ["تعيش في الذاكرة والانتماء", "تتنفس عبر الهوية والتاريخ"],
            "documentary": ["موثقة في الثقافة والذاكرة", "مسجلة عبر الأجيال"],
            "viral": ["ليست ترندًا بل حقيقة", "قصة يحاول العالم تجاهلها"]
        },
        "gaza": {
            "start": "غزة",
            "neutral": ["تستمر بالصبر والتحمل", "وجودها يتجاوز العناوين اليومية"],
            "emotional": ["تحمل قصصاً مكتوبة بالصبر", "تنقل القوة رغم الصعاب"],
            "documentary": ["تعكس صمود البشر تحت الضغط", "توثق الحياة اليومية بعيدًا عن الإحصاءات"],
            "viral": ["أكثر مما يُقال عنها", "ليست مجرد ما تظهره الأخبار"]
        },
        "maps": {
            "start": "خريطة تاريخية لفلسطين",
            "neutral": ["تحفظ الجغرافيا المرسومة منذ زمن", "توثق الأرض قبل الروايات الحديثة"],
            "emotional": ["تحمل الذاكرة في كل خط", "تحوي قصصاً تتجاوز الحبر والورق"],
            "documentary": ["توثق الأماكن كما كانت", "تُعد دليلًا مرئيًا للتاريخ"],
            "viral": ["تكشف ما لم يمحُه الزمن", "تظهر التاريخ بلا تعليق"]
        },
        "nakba": {
            "start": "النكبة",
            "neutral": ["تظل لحظة تاريخية محددة", "ترك تأثيرًا دائمًا على الهوية"],
            "emotional": ["تعيش بهدوء في الذاكرة الجمعية", "تترك أصداءً عبر الأجيال"],
            "documentary": ["موثقة بالشهادات والتاريخ", "تشير إلى نقطة تحول في التجربة الحياتية"],
            "viral": ["ليست مجرد تاريخ", "أكثر من فصل في الكتب"]
        }
    }
}

TONES = ["neutral", "emotional", "documentary", "viral"]

# ================= UTIL =================
def contains_blocked(text):
    t = text.lower()
    return any(w in t for w in BLOCKED_WORDS)

def generate_hook(lang, category, tone):
    data = HOOKS[lang][category]
    emoji = random.choice(EMOJIS)

    for _ in range(10):
        text = (
            f"{data['start']} {random.choice(data[tone])}\n"
            f"A story shaped by memory\n"
            f"A presence that continues"
        )

        if not contains_blocked(text):
            tags = " ".join(random.sample(HASHTAGS[category], 2))
            return f"{text}\n{tags} #Hatshepsut {emoji}"

    return "Content could not be generated safely."

# ================= KEYBOARDS =================
def language_menu():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🌍 English", callback_data="lang|en"),
        InlineKeyboardButton("🌍 عربي", callback_data="lang|ar")
    )
    return kb

def category_menu(lang):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🇵🇸 Palestine", callback_data=f"cat|{lang}|palestine"),
        InlineKeyboardButton("🔥 Gaza", callback_data=f"cat|{lang}|gaza"),
        InlineKeyboardButton("🗺️ Historical Maps", callback_data=f"cat|{lang}|maps"),
        InlineKeyboardButton("🕊️ Nakba", callback_data=f"cat|{lang}|nakba"),
        InlineKeyboardButton("🎲 Surprise Me", callback_data="surprise")
    )
    return kb

def tone_menu(lang, category):
    kb = InlineKeyboardMarkup(row_width=2)
    for tone in TONES:
        kb.add(
            InlineKeyboardButton(
                tone.capitalize(),
                callback_data=f"tone|{lang}|{category}|{tone}"
            )
        )
    return kb

def action_menu(lang, category, tone, text):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(
            "🔄 Generate Again",
            callback_data=f"again|{lang}|{category}|{tone}"
        ),
        InlineKeyboardButton(
            "📋 Copy",
            switch_inline_query_current_chat=text
        ),
        InlineKeyboardButton(
            "🌐 Translate",
            callback_data=f"translate|{lang}|{category}|{tone}|{text}"
        ),
        InlineKeyboardButton(
            "👍",
            callback_data=f"rate|up|{text}"
        ),
        InlineKeyboardButton(
            "👎",
            callback_data=f"rate|down|{text}"
        )
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Choose language / اختر اللغة:",
        reply_markup=language_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    try:
        data = call.data.split("|")

        if data[0] == "lang":
            bot.send_message(
                call.message.chat.id,
                "Choose category:",
                reply_markup=category_menu(data[1])
            )

        elif data[0] == "cat":
            bot.send_message(
                call.message.chat.id,
                "Choose tone:",
                reply_markup=tone_menu(data[1], data[2])
            )

        elif data[0] == "tone":
            _, lang, category, tone = data
            text = generate_hook(lang, category, tone)
            if text:
                bot.send_message(
                    call.message.chat.id,
                    text,
                    reply_markup=action_menu(lang, category, tone, text)
                )

        elif data[0] == "again":
            _, lang, category, tone = data
            text = generate_hook(lang, category, tone)
            if text:
                bot.send_message(
                    call.message.chat.id,
                    text,
                    reply_markup=action_menu(lang, category, tone, text)
                )

        elif data[0] == "surprise":
            lang = random.choice(["en","ar"])
            category = random.choice(list(HOOKS[lang].keys()))
            tone = random.choice(TONES)
            text = generate_hook(lang, category, tone)
            if text:
                bot.send_message(
                    call.message.chat.id,
                    text,
                    reply_markup=action_menu(lang, category, tone, text)
                )

        elif data[0] == "translate":
            # ترجمة بسيطة: تغيير اللغة (toggle)
            _, lang, category, tone, text = data
            new_lang = "ar" if lang == "en" else "en"
            new_text = generate_hook(new_lang, category, tone)
            bot.send_message(
                call.message.chat.id,
                new_text,
                reply_markup=action_menu(new_lang, category, tone, new_text)
            )

        elif data[0] == "rate":
            _, direction, text = data
            bot.answer_callback_query(call.id, f"Thanks for rating {direction}!")

    except Exception as e:
        print("ERROR:", e)

# ================= RUN =================
print("Bot is running safely...")
bot.infinity_polling(skip_pending=True)
