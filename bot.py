# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

# ================= BOT INIT =================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= SAFETY FILTER =================
BLOCKED = [
    "violence","violent","attack","kill","bomb","destroy",
    "weapon","missile","rocket","war","fight","combat"
]

def safe(text):
    t = text.lower()
    return not any(w in t for w in BLOCKED)

# ================= USER MEMORY =================
USER_HISTORY = {}

def remember(uid, key):
    USER_HISTORY.setdefault(uid, []).append(key)
    USER_HISTORY[uid] = USER_HISTORY[uid][-300:]

def seen(uid, key):
    return key in USER_HISTORY.get(uid, [])

# ================= UI CATEGORIES (AR ONLY) =================
CATEGORIES = {
    "maps": "🗺️ الخرائط التاريخية",
    "palestine": "🇵🇸 فلسطين",
    "gaza": "🏙️ غزة",
    "nakba": "📜 النكبة"
}

# ================= ASSERTIVE LONG STATEMENTS =================
STATEMENTS = {

    "maps": [
        (
            "This is the original historical map of Palestine before 1948 as officially recorded",
            "It documents Palestine clearly as a recognized geographical entity without alteration",
            "It remains a verified and consistent cartographic reference"
        ),
        (
            "This map represents Palestine exactly as identified in historical records prior to 1948",
            "It reflects formal geographic documentation used during that historical period",
            "It stands as a stable and unquestioned historical source"
        ),
        (
            "This is an authentic cartographic record identifying Palestine before 1948",
            "It presents Palestine as a defined and named geographical location",
            "It remains consistent across historical documentation"
        ),
        (
            "This historical map shows Palestine as clearly defined before any later changes",
            "It records Palestine using established cartographic standards of its time",
            "It remains preserved as verified historical evidence"
        ),
        (
            "This map documents Palestine as officially recognized prior to 1948",
            "It confirms the presence of Palestine within historical geographic records",
            "It remains fixed within documented cartography"
        ),
        (
            "This is a verified historical map clearly identifying Palestine before 1948",
            "It reflects how Palestine was formally documented and referenced",
            "It remains an authoritative geographic source"
        ),
        (
            "This map presents Palestine as consistently recorded in historical cartography",
            "It confirms Palestine’s presence without ambiguity or reinterpretation",
            "It stands as reliable historical documentation"
        ),
        (
            "This is a preserved map documenting Palestine as known before 1948",
            "It reflects established geographic knowledge of that period",
            "It remains unchanged within historical archives"
        ),
        (
            "This historical cartographic record clearly identifies Palestine before 1948",
            "It documents Palestine using standardized geographic references",
            "It remains validated across historical sources"
        ),
        (
            "This map records Palestine as a defined geographic entity prior to 1948",
            "It confirms consistent historical identification of Palestine",
            "It stands as enduring historical evidence"
        )
    ],

    "palestine": [
        (
            "Palestine is a historical fact established through continuous documentation",
            "It exists across geography, records, and formally preserved history",
            "It remains a confirmed and enduring reality"
        ),
        (
            "Palestine exists as an established and recognized historical reality",
            "It is consistently documented across maps and historical records",
            "It stands as a continuous historical presence"
        ),
        (
            "Palestine is recorded as a defined geographical and historical entity",
            "It appears consistently across documented sources and references",
            "It remains fixed and identifiable through time"
        ),
        (
            "Palestine is not an interpretation but a documented historical fact",
            "It is supported by extensive geographic and historical records",
            "It remains a stable and confirmed reality"
        ),
        (
            "Palestine exists as a continuous historical presence",
            "It has been identified and recorded across generations",
            "It remains firmly established in history"
        ),
        (
            "Palestine is historically documented across official geographic records",
            "It appears clearly within preserved historical sources",
            "It remains an established historical reality"
        ),
        (
            "Palestine stands as a recognized historical and geographic entity",
            "It is documented without interruption across time",
            "It remains consistently identifiable"
        ),
        (
            "Palestine exists through recorded geography and preserved history",
            "It has been consistently named and documented",
            "It remains historically established"
        ),
        (
            "Palestine is a confirmed historical fact supported by documentation",
            "It appears across multiple historical and geographic records",
            "It remains an enduring reality"
        ),
        (
            "Palestine exists as a clearly defined historical entity",
            "It is documented through consistent geographic references",
            "It remains fixed within recorded history"
        )
    ],

    "gaza": [
        (
            "Gaza is an integral part of the Palestinian geographic landscape",
            "It exists as a documented Palestinian city throughout history",
            "It remains a confirmed and continuous reality"
        ),
        (
            "Gaza is historically identified as a Palestinian city",
            "It appears consistently within geographic and historical records",
            "It remains firmly established"
        ),
        (
            "Gaza exists as a documented Palestinian presence",
            "It has been recorded across historical sources and references",
            "It remains a stable geographic reality"
        ),
        (
            "Gaza stands as part of Palestinian geography and history",
            "It is consistently identified within documented records",
            "It remains an established reality"
        ),
        (
            "Gaza is recorded as a Palestinian city across historical documentation",
            "It appears clearly within preserved geographic records",
            "It remains historically confirmed"
        ),
        (
            "Gaza exists within Palestinian geographic identification",
            "It has been documented consistently across time",
            "It remains a recognized historical reality"
        ),
        (
            "Gaza represents a continuous Palestinian geographic presence",
            "It is documented without interruption in historical sources",
            "It remains fixed in geography"
        ),
        (
            "Gaza is historically recorded as part of Palestine",
            "It appears across consistent geographic documentation",
            "It remains an established reality"
        ),
        (
            "Gaza stands as a documented Palestinian city",
            "It is identified through preserved historical records",
            "It remains geographically and historically consistent"
        ),
        (
            "Gaza exists as a confirmed Palestinian geographic location",
            "It has been recorded across historical references",
            "It remains firmly established"
        )
    ],

    "nakba": [
        (
            "The Nakba is a documented historical event",
            "It marked a recorded turning point in Palestinian history",
            "It remains preserved within historical records"
        ),
        (
            "The Nakba represents a confirmed historical moment",
            "It is documented across multiple historical sources",
            "It remains an established historical fact"
        ),
        (
            "The Nakba is recorded as a significant historical event",
            "It appears consistently within historical documentation",
            "It remains preserved through time"
        ),
        (
            "The Nakba stands as a documented moment in history",
            "It is supported by extensive historical records",
            "It remains historically confirmed"
        ),
        (
            "The Nakba exists as a recorded historical event",
            "It has been documented across preserved sources",
            "It remains fixed within history"
        ),
        (
            "The Nakba is recognized through documented historical evidence",
            "It is recorded across multiple historical references",
            "It remains established in historical memory"
        ),
        (
            "The Nakba represents a documented historical reality",
            "It is preserved through consistent historical records",
            "It remains an enduring historical fact"
        ),
        (
            "The Nakba is identified as a recorded historical event",
            "It appears within preserved historical documentation",
            "It remains historically established"
        ),
        (
            "The Nakba exists as a confirmed historical occurrence",
            "It is documented without contradiction across sources",
            "It remains fixed in history"
        ),
        (
            "The Nakba stands as a preserved historical event",
            "It is supported by recorded historical documentation",
            "It remains an established historical fact"
        )
    ]
}

# ================= EMOJIS =================
EMOJIS = {
    "maps": ["🗺️","🧭","📜","📐","🧾","📖","🪶"],
    "palestine": ["🌍","🧱","📜","⏳","🌿","✨","🕊️"],
    "gaza": ["🏙️","🌊","📍","🧱","🌅","⏳","🕊️"],
    "nakba": ["📜","⏳","🕯️","📖","🪶","🧠","🕊️"]
}

# ================= HASHTAGS =================
HASHTAGS = {
    "maps": "#Palestine #HistoricalMap #Pre1948 #Documented #Verified #Fact",
    "palestine": "#Palestine #HistoricalFact #RecordedHistory #Established",
    "gaza": "#Gaza #Palestine #HistoricalReality #Recorded",
    "nakba": "#Nakba #DocumentedHistory #HistoricalFact"
}

# ================= GENERATOR =================
def generate(uid, category):
    for _ in range(60):
        s1, s2, s3 = random.choice(STATEMENTS[category])
        emoji = random.choice(EMOJIS[category])

        body = f"{s1}.\n{s2}.\n{s3}."
        text = f"{body}\n\n🇵🇸 {emoji}\n\n{HASHTAGS[category]}"

        key = f"{category}|{body}"
        if seen(uid, key):
            continue
        if not safe(text):
            continue

        remember(uid, key)
        return f"<code>{text}</code>"

    return "<code>The historical record remains unchanged.</code>"

# ================= KEYBOARDS =================
def categories_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    for k, v in CATEGORIES.items():
        kb.add(InlineKeyboardButton(v, callback_data=f"cat|{k}"))
    return kb

def again_kb(category):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔁 تعزيز البيان", callback_data=f"again|{category}"))
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, "🔒 اختر القسم:", reply_markup=categories_kb())

@bot.callback_query_handler(func=lambda c: True)
def handle(c):
    uid = c.from_user.id
    data = c.data.split("|")

    if data[0] == "cat":
        txt = generate(uid, data[1])
        bot.send_message(c.message.chat.id, txt, reply_markup=again_kb(data[1]))
    elif data[0] == "again":
        txt = generate(uid, data[1])
        bot.send_message(c.message.chat.id, txt, reply_markup=again_kb(data[1]))
    else:
        bot.answer_callback_query(c.id)

# ================= RUN =================
print("🇵🇸 ASSERTIVE ENGLISH FACT ENGINE RUNNING")
bot.infinity_polling(skip_pending=True)
