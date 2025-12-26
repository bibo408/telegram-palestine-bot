# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

TOKEN = os.getenv("BOT_TOKEN")
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

# ================= SEMANTIC AVOIDANCE ENGINE =================
SEMANTIC_BLACKLIST = {
    "war": ["battle","fight","combat","clash"],
    "military": ["armed","forces","troops"],
    "destruction": ["ruin","devastation","wreckage"],
}

def semantic_safe(text):
    t = text.lower()
    for root, variants in SEMANTIC_BLACKLIST.items():
        if root in t:
            return False
        for v in variants:
            if v in t:
                return False
    return True

# ================= USER VARIATION LOCK =================
USER_HISTORY = {}

def seen_before(uid, key):
    if uid not in USER_HISTORY:
        USER_HISTORY[uid] = set()
    return key in USER_HISTORY[uid]

def remember(uid, key):
    USER_HISTORY[uid].add(key)

# ================= USER PREFERENCES =================
USER_PREFS = {}

def get_prefs(uid):
    if uid not in USER_PREFS:
        USER_PREFS[uid] = {
            "typography": "mono",
            "randomness": "balanced"
        }
    return USER_PREFS[uid]

# ================= EMOJIS =================
EMOJIS = ["🇵🇸","🕊️","📜","⏳","🗺️","✨"]

# ================= CATEGORIES =================
CATEGORIES = {
    "palestine": "🇵🇸 فلسطين",
    "gaza": "🔥 غزة",
    "maps": "🗺️ خرائط فلسطين",
    "memory": "📜 الذاكرة الفلسطينية",
    "nakba": "🕊️ النكبة وأحداثها"
}

# ================= OPENING WORD CONTROL =================
OPENINGS = {
    "maps": [
        "This is a historical map of Palestine before 1948",
        "A documented historical map of Palestine prior to 1948",
        "This historical map records Palestine as it existed before 1948",
        "Explore the Palestinian landscape as it was pre-1948",
        "Palestine before 1948, captured in this historical map",
        "This map showcases Palestine in its historical borders",
        "A visual record of Palestinian territory before 1948",
        "Mapping Palestine's historical geography prior to 1948",
        "The pre-1948 borders of Palestine displayed here",
        "This archival map preserves Palestine's past",
        "Palestine depicted historically before 1948",
        "A visual documentation of Palestine pre-1948",
        "Historical cartography of Palestine before 1948",
        "Palestine’s geography prior to 1948 in detail",
        "Detailed map illustrating Palestine before 1948"
        "Maps showing Palestine before 1948",
"A historical cartography of Palestine pre-1948",
"Archival map of Palestinian lands prior to 1948",
"Detailed depiction of Palestine before 1948",
"Palestinian geography as it existed before 1948",
"Visual record of Palestine’s borders pre-1948",
"Palestinian territories mapped historically",
"Historic map illustrating Palestine before 1948",
"Cartographic documentation of Palestine pre-1948",
"Palestine’s land divisions before 1948",
"Archival cartography depicting Palestine",
"Palestinian map from historical records",
"Mapped geography of Palestine before 1948",
"Visualizing Palestine historically before 1948",
"Palestine represented on pre-1948 maps",
"Historical depiction of Palestinian regions",
"Documented map showing Palestine boundaries",
"Palestinian territories in historical context",
"Old map of Palestine for archival study",
"Palestine before 1948 shown cartographically",
"Historical mapping of Palestinian lands",
"Pre-1948 map illustrating Palestinian towns",
"Archival depiction of Palestinian cities",
"Detailed geography of Palestine before 1948",
"Historical overview of Palestinian boundaries",
"Mapping Palestinian territories historically",
"Palestine captured in old maps",
"Documented territorial layout of Palestine",
"Historic map marking Palestinian towns",
"Palestine illustrated through cartography",
"Archival study of Palestine maps",
"Historic overview of Palestinian regions",
"Palestinian land divisions on historical maps",
"Old cartography of Palestinian areas",
"Palestinian borders documented pre-1948",
"Detailed archival maps of Palestine",
"Palestine mapped according to historical records",
"Historic territorial mapping of Palestine",
"Palestinian cities and towns mapped historically",
"Visual historical record of Palestine",
"Mapping Palestine before the year 1948",
"Archival mapping of Palestinian regions",
"Historical cartography showing Palestine",
"Palestine captured in pre-1948 geography",
"Documented boundaries of Palestine historically",
"Old maps depicting Palestinian towns",
"Palestinian landscapes recorded historically",
"Palestine illustrated on old cartographic maps",
"Historic mapping of Palestinian territories",
"Archival documentation of Palestine maps",
"Palestinian historical regions shown on maps",
"Mapping the lands of Palestine before 1948"

    ],
    "palestine": [
        "Palestine exists as a continuous identity",
        "Palestine lives beyond time and narration",
        "Palestine remains present through memory and place",
        "Palestinian identity persists throughout history",
        "Palestine endures through culture and memory",
        "Palestinian heritage remains alive today",
        "Palestine’s story continues through generations",
        "Palestine stands as a living history",
        "Palestinian land holds an eternal identity",
        "Palestine maintains its presence despite challenges",
        "Palestinian culture and identity persist",
        "Palestine’s existence transcends time",
        "Palestine lives in memory and spirit",
        "Palestine remains a core identity",
        "Palestine is eternal through history and people"
        "Palestine exists as a continuous identity",
        "Palestine lives beyond time and narration",
        "Palestine remains present through memory and place",
        "Palestine has always been a land of culture and history",
        "The spirit of Palestine endures across generations",
        "Palestinian identity is rooted in its lands",
        "Palestine thrives in memory and stories",
        "Palestinian presence persists through time",
        "Palestine remains alive in hearts and minds",
        "The essence of Palestine transcends borders",
        "Palestine has been a beacon of heritage",
        "Palestinian identity flows through history",
        "Palestine survives through remembrance",
        "The legacy of Palestine is eternal",
        "Palestinian culture continues to flourish",
        "Palestine’s story is told through its people",
        "Palestinian history remains vivid and alive",
        "Palestine embodies resilience and identity",
        "Palestinian lands hold centuries of memory",
        "Palestine persists despite challenges",
        "The soul of Palestine is indestructible",
"Palestinian identity is carried through generations",
"Palestine remains a homeland in spirit",
"Palestinian traditions thrive despite adversity",
"Palestine stands as a symbol of heritage",
"Palestinian memory shapes the present",
"Palestine continues to inspire its people",
"Palestinian roots run deep through history",
"The heart of Palestine beats through its stories",
"Palestine’s identity is timeless and enduring",
"Palestinian presence endures in every village",
"Palestine reflects culture, history, and memory",
"Palestinian lands tell stories of resilience",
"Palestine’s spirit is preserved in memory",
"Palestinian heritage remains alive today",
"Palestine carries its identity forward",
"Palestinian lands have been home for generations",
"Palestine stands as a testament to culture",
"Palestinian people embody the land’s history",
"The memory of Palestine lives through its people",
"Palestinian identity is woven into the land",
"Palestine’s story is written across generations",
"Palestinian culture survives through memory",
"Palestine exists beyond political maps",
"Palestinian heritage is a continuous legacy",
"The spirit of Palestine flows through time",
"Palestinian identity remains steadfast",
"Palestine continues to exist in every heart",
"Palestinian memory keeps the land alive",
"Palestine’s presence is eternal in spirit",
"The story of Palestine is never forgotten"

    ],
    "gaza": [
        "Gaza represents daily Palestinian presence",
        "Gaza carries Palestinian identity forward",
        "Gaza reflects lived Palestinian reality",
        "Life in Gaza embodies Palestinian continuity",
        "Gaza holds centuries of history and memory",
        "The streets of Gaza tell Palestinian stories",
        "Gaza preserves Palestinian culture and life",
        "Every corner of Gaza reflects history",
        "Gaza's people maintain enduring heritage",
        "Daily life in Gaza sustains identity",
        "Gaza remains a symbol of Palestinian resilience",
        "Gaza mirrors Palestinian tradition and life",
        "Gaza is a living witness to history",
        "Palestinian presence thrives in Gaza",
        "Gaza’s daily rhythm preserves identity"
        "Gaza represents daily Palestinian presence",
"Gaza carries Palestinian identity forward",
"Gaza reflects lived Palestinian reality",
"The spirit of Gaza endures through its people",
"Gaza continues to tell its story",
"Palestinian life thrives in Gaza",
"Gaza embodies resilience and culture",
"Gaza preserves history through memory",
"The essence of Gaza remains strong",
"Gaza’s heritage lives through generations",
"Gaza reflects the soul of Palestine",
"Palestinian traditions flourish in Gaza",
"Gaza stands as a symbol of perseverance",
"Gaza holds centuries of Palestinian memory",
"The heart of Gaza beats with life",
"Gaza’s people embody its history",
"Palestinian identity thrives in Gaza",
"Gaza remains a land of stories and memories",
"The spirit of Gaza is indestructible",
"Gaza carries its legacy forward",
"Gaza preserves Palestinian roots",
"Palestinian culture continues in Gaza",
"Gaza reflects resilience and identity",
"The soul of Gaza shines through challenges",
"Gaza’s history is alive in its people",
"Palestinian memory is preserved in Gaza",
"Gaza stands strong across generations",
"Gaza represents Palestinian continuity",
"The essence of Gaza flows through time",
"Gaza’s people keep the land’s spirit alive",
"Palestinian identity persists in Gaza",
"Gaza thrives through culture and heritage",
"The heart of Gaza tells its story",
"Gaza embodies Palestinian resilience",
"Gaza remains a beacon of identity",
"The legacy of Gaza lives on",
"Gaza reflects Palestinian struggle and hope",
"Palestinian traditions endure in Gaza",
"Gaza carries its culture forward",
"Gaza survives through memory and stories",
"The spirit of Gaza is eternal",
"Gaza’s people preserve its identity",
"Gaza stands as a testament to heritage",
"Palestinian life continues in Gaza",
"Gaza embodies history and perseverance",
"The soul of Gaza survives through generations",
"Gaza remains alive in stories and memory",
"Palestinian identity flows in Gaza",
"Gaza’s spirit inspires its people",
"Gaza keeps Palestinian memory alive"

    ],
    "memory": [
        "Palestinian memory moves quietly through generations",
        "Memory preserves Palestinian identity without interruption",
        "This memory carries Palestine forward",
        "Heritage keeps the Palestinian story alive",
        "Memory ensures identity continuity",
        "Collective remembrance sustains culture",
        "Memory of Palestine persists through time",
        "Palestinian history is carried in memory",
        "Past generations’ memory informs today",
        "Memory anchors Palestinian identity",
        "Stories and recollections preserve heritage",
        "Historical memory maintains culture",
        "Memory of Palestine shapes the present",
        "Heritage remembered across generations",
        "Palestinian memory is ever-living"
        "Palestinian memory moves quietly through generations",
"Memory preserves Palestinian identity without interruption",
"This memory carries Palestine forward",
"Palestinian history lives in memory",
"Memory holds the essence of Palestine",
"Generations pass on Palestinian memory",
"Memory keeps Palestinian stories alive",
"Palestinian memory shapes identity",
"Memory reflects Palestinian resilience",
"Memory preserves the past for the future",
"Palestinian heritage thrives through memory",
"Memory records Palestine's living history",
"Memory maintains the spirit of the people",
"Palestinian culture continues in memory",
"Memory safeguards Palestinian traditions",
"Palestinian identity persists through memory",
"Memory tells the story of Palestine",
"Memory is a bridge between generations",
"Memory embodies Palestinian continuity",
"Memory carries the essence of the homeland",
"Palestinian experiences are held in memory",
"Memory nurtures collective identity",
"Memory immortalizes Palestinian life",
"Memory shapes the future through the past",
"Palestinian memory lives in hearts",
"Memory safeguards history from being lost",
"Memory preserves everyday Palestinian life",
"Memory transmits stories of resilience",
"Memory reflects Palestinian struggles and triumphs",
"Memory honors ancestors and heritage",
"Memory keeps Palestinian roots alive",
"Memory tells of life before displacement",
"Memory preserves moments of Palestinian culture",
"Memory connects generations and places",
"Memory upholds the spirit of Palestine",
"Palestinian memory is a treasure",
"Memory protects identity across time",
"Memory carries voices of the past",
"Memory is the soul of Palestinian continuity",
"Memory immortalizes traditions and customs",
"Memory keeps the homeland alive in hearts",
"Memory strengthens Palestinian belonging",
"Memory embodies stories of survival",
"Memory reflects enduring heritage",
"Memory honors resilience and culture",
"Memory keeps history vivid and present",
"Memory preserves values and identity",
"Memory holds the narratives of Palestine",
"Memory passes wisdom from elders to youth",
"Memory ensures Palestine is never forgotten",
"Memory sustains identity through generations"

    ],
    "nakba": [
        "The Nakba reshaped Palestinian daily life",
        "The Nakba marked a historical turning point",
        "That moment in history altered Palestinian lives",
        "The Nakba changed the course of history",
        "Lives were transformed during the Nakba",
        "Nakba represents a critical historical moment",
        "Palestinian life was forever changed by the Nakba",
        "The Nakba reshaped communities and culture",
        "History remembers the Nakba vividly",
        "Nakba’s impact echoes through generations",
        "The Nakba is a pivotal historical event",
        "Palestinian identity was challenged during Nakba",
        "Nakba left lasting historical footprints",
        "Lives and memory were altered by Nakba",
        "The Nakba defined a new era for Palestine"
        "The Nakba reshaped Palestinian daily life",
"The Nakba marked a historical turning point",
"That moment in history altered Palestinian lives",
"The Nakba changed generations forever",
"The Nakba left a lasting mark on Palestine",
"The Nakba displaced countless families",
"Stories of the Nakba live in memory",
"The Nakba reminds us of resilience",
"The Nakba is remembered through generations",
"The Nakba echoes in Palestinian identity",
"The Nakba shaped the homeland's history",
"The Nakba altered the map of Palestine",
"The Nakba continues to affect lives today",
"The Nakba carries lessons of perseverance",
"The Nakba is part of collective memory",
"Through the Nakba, history is never forgotten",
"The Nakba inspires remembrance and action",
"The Nakba holds countless untold stories",
"Memory of the Nakba preserves identity",
"The Nakba changed the course of lives",
"The Nakba represents loss and endurance",
"The Nakba connects past and present",
"The Nakba is a chapter of history",
"The Nakba transformed communities",
"The Nakba teaches resilience and strength",
"The Nakba is etched in Palestinian hearts",
"The Nakba reminds us of homeland's value",
"The Nakba embodies struggle and hope",
"The Nakba impacts identity and culture",
"The Nakba lives in stories and memory",
"The Nakba left generations uprooted",
"The Nakba is never forgotten by history",
"The Nakba carries lessons for the future",
"The Nakba shapes collective consciousness",
"The Nakba changed landscapes and lives",
"The Nakba is memorialized through generations",
"The Nakba is part of the national narrative",
"The Nakba teaches the cost of displacement",
"The Nakba preserves historical truth",
"The Nakba guides remembrance today",
"The Nakba reflects endurance and memory",
"The Nakba binds generations together",
"The Nakba inspires continuity of identity",
"The Nakba left a permanent legacy",
"The Nakba reminds of struggle and survival",
"The Nakba shaped Palestinian resilience",
"The Nakba remains central in memory",
"The Nakba tells the story of loss",
"The Nakba connects families across time",
"The Nakba is remembered with solemnity",
"The Nakba defines historical consciousness",
"The Nakba underscores the importance of home",
"The Nakba continues to shape narratives"

    ]
}

# ================= MOOD PRESETS =================
MOODS = {
    "🧠 هادئ توثيقي": {
        "middles": [
            "documented carefully without commentary",
            "recorded through names, places, and memory",
            "preserved without noise or exaggeration",
            "carefully noted through historical references",
            "recorded from oral histories",
            "documented with attention to every detail",
            "observed and chronicled with precision",
            "noted faithfully through evidence"
        ],
        "endings": [
            "as part of Palestinian historical continuity",
            "within Palestinian collective memory",
            "as a documented Palestinian reality",
            "as part of the enduring Palestinian narrative",
            "ensuring memory remains intact for generations",
            "recorded for historical accuracy",
            "maintaining authentic Palestinian heritage",
            "preserved for future generations"
        ]
    },
    "⚡ مكثف عميق": {
        "middles": [
            "beyond headlines and explanations",
            "without needing validation",
            "outside imposed narratives",
            "beyond public perception",
            "through deep analysis",
            "without external commentary",
            "beyond superficial accounts",
            "through concentrated focus"
        ],
        "endings": [
            "remaining undeniably Palestinian",
            "rooted deeply in Palestinian identity",
            "connected permanently to Palestine",
            "standing firmly as Palestinian",
            "deeply embedded in identity",
            "held strongly through culture",
            "unshaken in heritage",
            "anchored in Palestinian reality"
        ]
    },
    "✨ تأملي إنساني": {
        "middles": [
            "through quiet remembrance",
            "through lived experience",
            "through memory carried forward",
            "in silent reflection",
            "through personal connection",
            "through empathetic understanding",
            "with mindful observation",
            "reflecting human experience"
        ],
        "endings": [
            "held gently within Palestinian memory",
            "remembered without permission",
            "kept alive through identity",
            "nurtured in cultural consciousness",
            "preserved in hearts and minds",
            "honored through collective remembrance",
            "maintained with care",
            "safeguarded in human memory"
        ]
    }
}

# ================= SYNONYMS =================
SYNONYMS = {
    "historical": ["documented", "archival", "recorded"],
    "Palestine": ["Palestinian land", "the land of Palestine", "Palestinian homeland"],
    "memory": ["heritage", "legacy", "recollection"],
    "identity": ["being", "essence", "character"],
    "life": ["existence", "daily life", "lifestyle"]
}

def apply_synonyms(text):
    for word, options in SYNONYMS.items():
        text = text.replace(word, random.choice(options))
    return text

# ================= HASHTAGS =================
HASHTAGS = {
    "palestine": "#Palestine #PalestinianIdentity #Hatshepsut",
    "gaza": "#Gaza #PalestinianMemory #Hatshepsut",
    "maps": "#HistoricalMap #Palestine #Hatshepsut",
    "memory": "#PalestinianMemory #History #Hatshepsut",
    "nakba": "#Nakba #PalestinianMemory #Hatshepsut"
}

# ================= ANTI-FLATNESS DETECTOR =================
def anti_flatness(opening, middle, ending):
    lens = [len(opening.split()), len(middle.split()), len(ending.split())]
    mean = sum(lens) / 3.0
    variance = sum((l - mean) ** 2 for l in lens) / 3.0
    if variance < 2.0:
        return False
    if opening.split()[0].lower() in middle.lower():
        return False
    if ending.split()[0].lower() in middle.lower():
        return False
    return True

# ================= TYPOGRAPHY MODES =================
TYPOGRAPHY_MODES = {
    "mono": lambda t: f"<code>{t}</code>",
    "boxed": lambda t: f"<pre>{t}</pre>",
    "clean": lambda t: t
}

def apply_typography(text, mode):
    return TYPOGRAPHY_MODES.get(mode, TYPOGRAPHY_MODES["mono"])(text)

# ================= CONTROLLED RANDOMNESS =================
RANDOMNESS_LEVELS = {
    "low": 0.2,
    "balanced": 0.5,
    "high": 0.8
}

def controlled_choice(items, level):
    r = RANDOMNESS_LEVELS.get(level, 0.5)
    if random.random() > r:
        return items[0]
    return random.choice(items)

# ================= HOOK ENGINE =================
def generate_hook(uid, category, mood):
    prefs = get_prefs(uid)
    for _ in range(80):
        opening = controlled_choice(OPENINGS[category], prefs["randomness"])
        middle = controlled_choice(MOODS[mood]["middles"], prefs["randomness"])
        ending = controlled_choice(MOODS[mood]["endings"], prefs["randomness"])
        emoji = random.choice(EMOJIS)

        if not anti_flatness(opening, middle, ending):
            continue

        key = f"{category}|{mood}|{opening}|{middle}|{ending}"
        if seen_before(uid, key):
            continue

        raw = (
            f"{opening},\n"
            f"{middle},\n"
            f"{ending}. {emoji}\n\n"
            f"{HASHTAGS[category]}"
        )

        raw = apply_synonyms(raw)

        if safe(raw) and semantic_safe(raw):
            remember(uid, key)
            return apply_typography(raw, prefs["typography"])

    return apply_typography("No new safe formulation could be generated.", prefs["typography"])

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
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{category}|{mood}"),
        InlineKeyboardButton("📋 Copy", callback_data=f"copy|{category}|{mood}")
    )
    kb.add(
        InlineKeyboardButton("🅣 Typography", callback_data=f"typography|{category}|{mood}")
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
    prefs = get_prefs(uid)

    if data[0] == "cat":
        bot.send_message(
            c.message.chat.id,
            "🎭 اختار النبرة:",
            reply_markup=mood_kb(data[1])
        )

    elif data[0] == "mood":
        _, category, mood = data
        text = generate_hook(uid, category, mood)
        bot.send_message(
            c.message.chat.id,
            text,
            reply_markup=again_kb(category, mood)
        )

    elif data[0] == "again":
        _, category, mood = data
        text = generate_hook(uid, category, mood)
        bot.send_message(
            c.message.chat.id,
            text,
            reply_markup=again_kb(category, mood)
        )

    elif data[0] == "typography":
        _, category, mood = data
        modes = list(TYPOGRAPHY_MODES.keys())
        prefs["typography"] = modes[(modes.index(prefs["typography"]) + 1) % len(modes)]
        bot.answer_callback_query(c.id, f"Typography: {prefs['typography']} ✔️")

    elif data[0] == "copy":
        bot.answer_callback_query(c.id, "Copied ✔️", show_alert=True)

# ================= RUN =================
print("🇵🇸 Advanced Palestinian Hook Engine running...")
bot.infinity_polling(skip_pending=True)

