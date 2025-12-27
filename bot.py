# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import re
import time

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
USER_PRESS = {}

def seen_before(uid, key):
    if uid not in USER_HISTORY:
        USER_HISTORY[uid] = []
    return key in USER_HISTORY[uid]

def remember(uid, key):
    USER_HISTORY.setdefault(uid, []).append(key)
    if len(USER_HISTORY[uid]) > 200:
        USER_HISTORY[uid] = USER_HISTORY[uid][-200:]

# ================= USER PREFERENCES =================
USER_PREFS = {}

def get_prefs(uid):
    if uid not in USER_PREFS:
        USER_PREFS[uid] = {
            "typography": "mono",
            "randomness": 0.4
        }
    return USER_PREFS[uid]

# ================= SYNONYMS ENGINE =================
SYNONYMS = {
    "historical": ["documented", "archival", "recorded"],
    "map": ["representation", "cartographic record"],
    "exists": ["persists", "remains"],
    "identity": ["presence", "essence"],
    "memory": ["remembrance", "collective memory"],
    "records": ["documents", "preserves"],
    "lives": ["endures", "continues"],
    "remains": ["stays", "persists"]
}

def smart_synonym_replace(text, loops=2):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if line.strip().startswith("#"):
            new_lines.append(line)
            continue
        words = re.findall(r"\b\w+\b", line)
        for _ in range(loops):
            for w in words:
                lw = w.lower()
                if lw in SYNONYMS and random.random() < 0.35:
                    rep = random.choice(SYNONYMS[lw])
                    line = re.sub(rf"\b{w}\b", rep, line, count=1)
        new_lines.append(line)
    return "\n".join(new_lines)

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
        "This historical map records Palestine as it existed before 1948"
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
        "Palestine remains present through memory and place"
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
        "Gaza reflects lived Palestinian reality"
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
        "This memory carries Palestine forward"
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
        "That moment in history altered Palestinian lives"
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
            "preserved without noise or exaggeration"
            "documented carefully without commentary",
"recorded through names, places, and memory",
"preserved without noise or exaggeration",
"noted with attention to historical detail",
"captured methodically and calmly",
"observed quietly through time",
"archived with meticulous care",
"traced through historical records",
"presented with factual accuracy",
"recorded without personal bias",
"kept as part of Palestinian heritage",
"documented with scholarly attention",
"transcribed from original sources",
"collected through oral histories",
"recorded in chronological order",
"compiled with historical context",
"noted objectively without interpretation",
"documented preserving authenticity",
"traced carefully through evidence",
"recorded through family stories",
"noted without embellishment",
"documented for archival purposes",
"kept in historical archives",
"observed through photographs and records",
"compiled with care and precision",
"presented in factual terms",
"recorded for educational purposes",
"archived for future generations",
"documented without external influence",
"traced through local testimonies",
"kept true to historical events",
"noted for historical accuracy",
"recorded through documents and letters",
"preserved in written accounts",
"documented with careful observation",
"traced through maps and archives",
"collected from eyewitnesses",
"documented without assumptions",
"preserved through careful transcription",
"recorded with authenticity",
"archived carefully for study",
"kept without modification",
"documented with historical rigor",
"traced through official documents",
"noted with accuracy and clarity",
"recorded without judgment",
"preserved with attention to detail",
"observed and noted systematically",
"documented quietly and accurately",
"traced through reliable sources",
"kept faithfully to original accounts",
"recorded with contextual awareness",
"collected methodically from sources",
"preserved in scholarly records",
"documented to maintain historical integrity",
"traced and verified through research",
"recorded through verified accounts",
"archived systematically",
"kept with utmost accuracy",
"noted in historical journals",
"documented through careful research",
"traced with attention to detail",
"recorded through trusted sources",
"preserved with factual emphasis",
"observed systematically over time",
"documented to reflect true events",
"collected with careful observation",
"recorded with academic precision",
"archived with reliability in mind",
"kept carefully through generations",
"traced through verified evidence",
"documented without embellishment",
"preserved for posterity",
"recorded with factual integrity",
"noted with clear historical context",
"documented through archives and reports",
"traced through recorded testimonies",
"collected accurately from witnesses",
"recorded without distortion",
"preserved in official records",
"documented to ensure accuracy",
"traced through authentic sources",
"kept true to historical facts",
"noted systematically",
"documented in detail",
"recorded for historical preservation",
"archived for future reference",
"traced with precision and care",
"preserved through official documentation",
"documented carefully for research",
"kept authentic through records",
"recorded methodically over time",
"traced with verification",
"documented without external bias",
"preserved through careful writing",
"observed and recorded faithfully",
"kept as true historical evidence",
"documented with meticulous attention",
"recorded to maintain truthfulness",
"traced systematically for accuracy",
"collected without alteration",
"preserved with focus on authenticity",
"documented carefully for education",
"kept with historical fidelity",
"recorded through detailed examination",
"traced and verified methodically",
"archived with attention to fact",
"documented to protect historical accuracy",
"recorded faithfully from reliable sources",
"kept systematically for study purposes",
"traced and documented thoroughly"

        ],
        "endings": [
            "as part of Palestinian historical continuity",
            "within Palestinian collective memory",
            "as a documented Palestinian reality"
            "as part of Palestinian historical continuity",
"within Palestinian collective memory",
"as a documented Palestinian reality",
"preserved in historical records",
"kept authentic through generations",
"maintained within local heritage",
"recorded for future reference",
"archived for educational purposes",
"retained in historical archives",
"kept true to documented events",
"ensuring historical accuracy",
"preserved with factual integrity",
"maintained through reliable sources",
"kept as true historical evidence",
"retained with careful documentation",
"archived with precision",
"documented with attention to detail",
"recorded faithfully over time",
"kept intact in memory and records",
"ensuring preservation of facts",
"maintained as verified history",
"kept for scholarly reference",
"preserved through careful writing",
"archived to reflect authenticity",
"maintained without distortion",
"recorded with utmost care",
"retained as part of collective memory",
"ensuring fidelity to history",
"preserved in official records",
"kept to honor historical truth",
"documented without external influence",
"maintained for educational study",
"retained as part of cultural heritage",
"kept for historical continuity",
"archived for future generations",
"preserved with scholarly attention",
"documented systematically",
"retained as authentic evidence",
"maintained through careful research",
"kept in chronological order",
"archived for verification",
"preserved to maintain truthfulness",
"retained as part of historical narrative",
"maintained without alteration",
"kept authentic through careful recording",
"documented for archival purposes",
"archived with attention to fact",
"preserved through verified sources",
"retained in historical manuscripts",
"maintained for posterity",
"kept as part of documented history",
"documented in detail",
"archived with integrity",
"preserved to ensure accuracy",
"retained with fidelity",
"maintained systematically",
"kept with historical rigor",
"documented for study purposes",
"archived to reflect verified events",
"preserved in original records",
"retained with scholarly precision",
"maintained without bias",
"kept true to original accounts",
"documented for historical fidelity",
"archived for careful research",
"preserved as verified fact",
"retained systematically for study",
"maintained as part of heritage",
"kept to uphold truth",
"documented with meticulous attention",
"archived with reliability",
"preserved through accurate recording",
"retained for scholarly study",
"maintained as factual record",
"kept authentic through careful documentation",
"documented for future generations",
"archived with precise attention",
"preserved to protect authenticity",
"retained as trusted evidence",
"maintained with historical context",
"kept in documented form",
"documented accurately for reference",
"archived for historical review",
"preserved through careful transcription",
"retained to maintain integrity",
"maintained for educational purposes",
"kept with utmost accuracy",
"documented systematically and faithfully",
"archived with careful observation",
"preserved as part of collective history",
"retained as authentic record",
"maintained to ensure historical truth",
"kept in factual form",
"documented with verification",
"archived for posterity",
"preserved in scholarly records",
"retained for authentic reference",
"maintained as part of Palestinian memory",
"kept accurately over time",
"documented with attention to authenticity",
"archived with factual emphasis",
"preserved through detailed examination",
"retained systematically and faithfully",
"maintained to reflect true events",
"kept in historical records",
"documented with verified sources",
"archived to maintain fidelity"

        ]
    },
    "⚡ مكثف عميق": {
        "middles": [
            "beyond headlines and explanations",
            "without needing validation",
            "outside imposed narratives"
            "beyond headlines and explanations",
"without needing validation",
"outside imposed narratives",
"challenging dominant perspectives",
"deeper than surface impressions",
"beyond conventional interpretations",
"without external justification",
"transcending superficial accounts",
"beyond immediate comprehension",
"without succumbing to bias",
"outside conventional storytelling",
"pushing past standard viewpoints",
"without reliance on mainstream narratives",
"beyond simplified explanations",
"challenging simplified interpretations",
"without external influence",
"deeper than common understanding",
"beyond superficial coverage",
"without needing external approval",
"transcending ordinary narratives",
"outside predictable frameworks",
"beyond typical interpretations",
"without relying on clichés",
"deeper than casual observation",
"beyond standard assumptions",
"without outside interference",
"transcending popular narratives",
"outside surface-level judgments",
"beyond mainstream simplifications",
"without depending on validation",
"challenging shallow interpretations",
"beyond traditional perspectives",
"without yielding to consensus",
"deeper than ordinary insights",
"beyond obvious explanations",
"without influence from others",
"transcending conventional wisdom",
"outside the expected narrative",
"beyond simplified storytelling",
"without external corroboration",
"challenging typical assumptions",
"beyond surface-level analysis",
"without needing reinforcement",
"deeper than superficial thought",
"beyond typical perspectives",
"without reliance on approval",
"transcending usual interpretations",
"outside mainstream viewpoints",
"beyond accepted narratives",
"without requiring validation",
"challenging ordinary assumptions",
"beyond typical reasoning",
"without influence from majority opinion",
"deeper than ordinary analysis",
"beyond general understanding",
"without depending on consensus",
"transcending conventional thinking",
"outside traditional assumptions",
"beyond common perception",
"without external confirmation",
"challenging standard viewpoints",
"beyond mainstream simplifications",
"without needing external agreement",
"deeper than typical insights",
"beyond obvious perceptions",
"without yielding to popular opinion",
"transcending accepted explanations",
"outside simplified frameworks",
"beyond conventional assumptions",
"without reliance on general opinion",
"challenging surface-level interpretations",
"beyond typical simplifications",
"without influence from mass consensus",
"deeper than standard reasoning",
"beyond general simplifications",
"without external validation",
"transcending ordinary viewpoints",
"outside conventional thinking",
"beyond superficial narratives",
"without depending on external proof",
"challenging typical perspectives",
"beyond everyday assumptions",
"without influence from mainstream sources",
"deeper than surface understanding",
"beyond ordinary interpretations",
"without yielding to standard explanations",
"transcending typical narratives",
"outside common frameworks",
"beyond simplified reasoning",
"without needing outside corroboration",
"challenging mainstream assumptions",
"beyond standard simplifications",
"without reliance on mass opinion",
"deeper than conventional thought",
"beyond typical observations",
"without external influence",
"transcending ordinary analysis",
"outside conventional simplifications",
"beyond popular assumptions",
"without needing outside approval",
"challenging surface-level reasoning",
"beyond ordinary perceptions",
"without dependence on validation",
"deeper than conventional analysis",
"beyond standard narratives",
"without influence from mainstream interpretations",
"transcending common assumptions",
"outside typical frameworks",
"beyond ordinary simplifications",
"without external confirmation"

        ],
        "endings": [
            "remaining undeniably Palestinian",
            "rooted deeply in Palestinian identity",
            "connected permanently to Palestine"
            "remaining undeniably Palestinian",
"rooted deeply in Palestinian identity",
"connected permanently to Palestine",
"preserved as an unbroken heritage",
"anchored in historical continuity",
"ensuring Palestinian memory endures",
"upholding collective identity",
"resilient through generations",
"standing firm in historical truth",
"maintaining unshakable identity",
"preserved beyond all adversity",
"anchored in unchanging roots",
"kept alive across generations",
"continuing the historical narrative",
"protected as a cultural legacy",
"unwavering in Palestinian reality",
"affirming historical presence",
"enduring despite challenges",
"rooted in ancestral memory",
"preserved against erasure",
"held firm through time",
"standing as historical truth",
"unbroken in identity and memory",
"maintained across generations",
"resisting dilution of history",
"embedded in Palestinian consciousness",
"secured in cultural memory",
"remaining a testament to heritage",
"anchored in unbroken lineage",
"preserved across centuries",
"unchanged in historical essence",
"upholding ancestral narratives",
"resilient to external pressures",
"affirming historical continuity",
"carried forward through generations",
"rooted in collective memory",
"maintained as historical truth",
"standing strong against erasure",
"upholding identity without compromise",
"preserved in lived experience",
"secured as a national reality",
"remaining a symbol of heritage",
"resisting historical manipulation",
"embedded in the social fabric",
"maintaining unbroken lineage",
"protected through collective memory",
"upholding cultural identity",
"continuing the ancestral legacy",
"unchanged in its essence",
"affirming resilience through time",
"remaining a beacon of heritage",
"anchored in enduring truth",
"preserved in the hearts of people",
"secured across history",
"maintaining cultural continuity",
"resilient in face of adversity",
"standing as a symbol of identity",
"upholding tradition and memory",
"preserved in collective consciousness",
"secured in historical narrative",
"remaining faithful to heritage",
"rooted in cultural foundations",
"maintained as an enduring reality",
"resisting historical erasure",
"affirming ancestral presence",
"carried through communal memory",
"standing unyielding through time",
"upholding the spirit of identity",
"preserved against cultural loss",
"secured in generational memory",
"remaining a testament to history",
"anchored in enduring values",
"maintained as a living legacy",
"resilient through changing times",
"continuing ancestral traditions",
"unchanged in its cultural significance",
"affirming the historical essence",
"remaining grounded in identity",
"upholding unbroken narratives",
"preserved across societal memory",
"secured as a lasting reality",
"maintaining the essence of heritage",
"resisting cultural dilution",
"embedded in national consciousness",
"standing firm through adversity",
"upholding ancestral truth",
"preserved in enduring memory",
"secured in historical fidelity",
"remaining a cornerstone of identity",
"rooted in continuous tradition",
"maintained as a cultural beacon",
"resilient to historical revisionism",
"affirming collective memory",
"carried forward without compromise",
"standing as a symbol of continuity",
"upholding legacy and tradition",
"preserved as unbroken heritage",
"secured in Palestinian reality",
"remaining faithful to memory",
"anchored in enduring identity",
"maintained through time",
"resilient across generations",
"continuing cultural legacy",
"unchanged in its historical essence",
"affirming identity and heritage",
"remaining a testament to continuity"

        ]
    },
    "✨ تأملي إنساني": {
        "middles": [
            "through quiet remembrance",
            "through lived experience",
            "through memory carried forward"
            "through quiet remembrance",
"through lived experience",
"through memory carried forward",
"with reflection on past events",
"guided by ancestral stories",
"through moments of contemplation",
"observing life’s quiet passages",
"through mindful awareness",
"absorbing lessons from history",
"through silent reflection",
"with gentle introspection",
"through personal recollection",
"embracing shared memories",
"through attentive observation",
"through mindful remembrance",
"guided by cultural insights",
"through subtle reflection",
"observing collective life",
"through patient contemplation",
"through heartfelt recollection",
"with thoughtful awareness",
"through experiential understanding",
"through reflective memory",
"through quiet observation",
"absorbing cultural wisdom",
"through introspective thought",
"through the lens of experience",
"guided by human stories",
"through thoughtful contemplation",
"through mindful attention",
"through reflective insight",
"through shared remembrance",
"through personal introspection",
"observing life with care",
"through attentive remembrance",
"through gentle reflection",
"through experiential insight",
"through patient memory",
"through mindful engagement",
"through heartfelt reflection",
"through cultural observation",
"guided by collective memory",
"through silent contemplation",
"through reflective observation",
"through empathetic understanding",
"through thoughtful recollection",
"through mindful perception",
"through quiet engagement",
"through attentive thought",
"through reflective awareness",
"through shared understanding",
"through personal reflection",
"through introspective observation",
"observing history with care",
"through mindful recollection",
"through gentle awareness",
"through experiential reflection",
"through thoughtful mindfulness",
"through patient observation",
"through reflective insightfulness",
"through empathetic reflection",
"through quiet introspection",
"through cultural mindfulness",
"through shared contemplation",
"through mindful empathy",
"through attentive insight",
"through heartfelt observation",
"through reflective mindfulness",
"through personal understanding",
"through introspective contemplation",
"observing life thoughtfully",
"through empathetic awareness",
"through gentle observation",
"through mindful introspection",
"through cultural reflection",
"through shared mindfulness",
"through thoughtful observation",
"through reflective perception",
"through quiet mindfulness",
"through experiential awareness",
"through patient reflection",
"through attentive mindfulness",
"through heartfelt introspection",
"through reflective engagement",
"through cultural observation",
"through mindful perception",
"through personal contemplation",
"through empathetic mindfulness",
"through gentle reflection",
"through reflective understanding",
"through shared reflection",
"through attentive engagement",
"through quiet contemplation",
"through introspective mindfulness",
"through thoughtful engagement",
"through mindful reflection",
"through reflective empathy",
"through heartfelt mindfulness",
"through experiential reflection",
"through patient introspection",
"through cultural engagement",
"through reflective contemplation",
"through shared understanding",
"through quiet engagement",
"through attentive reflection",
"through mindful understanding",
"through empathetic contemplation",
"through gentle mindfulness",
"through reflective thought",
"through personal mindfulness"

        ],
        "endings": [
            "held gently within Palestinian memory",
            "remembered without permission",
            "kept alive through identity"
            "held gently within Palestinian memory",
"remembered without permission",
"kept alive through identity",
"cherished quietly across generations",
"preserved in collective consciousness",
"held softly within shared memory",
"remained in hearts and minds",
"passed down through stories",
"engraved in cultural remembrance",
"nurtured through reflection",
"kept tenderly in awareness",
"honored through thoughtful recollection",
"maintained in quiet reverence",
"upheld through shared experience",
"cherished within daily life",
"safeguarded through memory",
"respected in ongoing tradition",
"kept gently in personal reflection",
"remembered with care",
"held in contemplative thought",
"preserved in cultural mindfulness",
"kept subtly alive",
"nurtured through empathy",
"honored within collective memory",
"carried forward with respect",
"observed through quiet reflection",
"maintained in human consciousness",
"preserved softly through stories",
"held tenderly in remembrance",
"remembered through heartfelt awareness",
"kept carefully in daily thought",
"cherished through introspection",
"nurtured within cultural identity",
"maintained with quiet attention",
"held delicately through time",
"remembered across lifetimes",
"upheld in mindful reflection",
"kept alive through shared experience",
"preserved thoughtfully in memory",
"observed with gentle care",
"held in reflective consciousness",
"cherished in the hearts of many",
"maintained subtly through life",
"kept gently in collective thought",
"nurtured through mindful awareness",
"honored softly in memory",
"remembered with quiet dignity",
"held through reflective understanding",
"preserved in human experience",
"kept thoughtfully alive",
"cherished quietly within culture",
"maintained in ongoing remembrance",
"held softly through generations",
"remembered with empathy",
"kept alive in shared stories",
"preserved with reflective care",
"nurtured through collective thought",
"held gently in mindful observation",
"remembered tenderly",
"cherished in quiet contemplation",
"maintained in reflective mindfulness",
"upheld with thoughtful care",
"kept alive across generations",
"preserved quietly in human consciousness",
"observed tenderly",
"held softly through cultural memory",
"remembered through mindful reflection",
"cherished thoughtfully",
"kept in heartfelt awareness",
"maintained with gentle mindfulness",
"held delicately in shared memory",
"remembered in quiet reflection",
"preserved through empathetic awareness",
"kept alive in thoughtful observation",
"cherished softly through generations",
"maintained subtly in human memory",
"held through mindful contemplation",
"remembered carefully",
"kept tenderly in cultural consciousness",
"preserved through reflective thought",
"nurtured gently in memory",
"held in quiet mindfulness",
"remembered with attentive care",
"cherished in reflective contemplation",
"maintained with empathy",
"kept alive in daily remembrance",
"preserved softly in shared awareness",
"observed carefully",
"held through introspective reflection",
"remembered in cultural mindfulness",
"cherished in mindful remembrance",
"maintained quietly in memory",
"kept thoughtfully through time",
"preserved with gentle care",
"nurtured in reflective consciousness",
"held tenderly in human memory",
"remembered with reflective attention",
"cherished through contemplative mindfulness",
"kept alive in cultural reflection",
"maintained softly in shared memory",
"held gently in ongoing remembrance"

        ]
    }
}

# ================= HASHTAGS =================
HASHTAGS = {
    "palestine": "#Palestine #PalestinianIdentity #Hatshepsut",
    "gaza": "#Gaza #PalestinianMemory #Hatshepsut",
    "maps": "#HistoricalMap #Palestine #Hatshepsut",
    "memory": "#PalestinianMemory #History #Hatshepsut",
    "nakba": "#Nakba #PalestinianMemory #Hatshepsut"
}

# ================= ANTI-FLATNESS DETECTOR =================
def anti_flatness(o, m, e):
    lens = [len(o.split()), len(m.split()), len(e.split())]
    if max(lens) - min(lens) < 2:
        return False
    return True

# ================= TYPOGRAPHY =================
def apply_typography(text):
    return f"<code>{text}</code>"

# ================= HOOK ENGINE =================
def generate_hook(uid, category, mood):
    prefs = get_prefs(uid)
    for _ in range(60):
        o = random.choice(OPENINGS[category])
        m = random.choice(MOODS[mood]["middles"])
        e = random.choice(MOODS[mood]["endings"])
        emoji = random.choice(EMOJIS)

        if not anti_flatness(o, m, e):
            continue

        key = f"{o}|{m}|{e}"
        if seen_before(uid, key):
            continue

        text = f"{o},\n{m},\n{e}. {emoji}\n\n{HASHTAGS[category]}"
        text = smart_synonym_replace(text)

        if safe(text) and semantic_safe(text):
            remember(uid, key)
            return apply_typography(text)

    return apply_typography("No new safe formulation could be generated.")

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

def again_kb(category, mood, copied=False):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{category}|{mood}")
    )
    if not copied:
        kb.add(
            InlineKeyboardButton("📋 Copy", callback_data=f"copy|{category}|{mood}")
        )
    else:
        kb.add(
            InlineKeyboardButton("✅ Copied", callback_data="noop")
        )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, "🇵🇸 اختار القسم:", reply_markup=categories_kb())

@bot.callback_query_handler(func=lambda c: True)
def handle(c):
    data = c.data.split("|")
    uid = c.from_user.id
    USER_PRESS.setdefault(uid, 0)

    if data[0] == "cat":
        bot.send_message(c.message.chat.id, "🎭 اختار النبرة:", reply_markup=mood_kb(data[1]))

    elif data[0] == "mood":
        USER_PRESS[uid] = 0
        _, cat, mood = data
        text = generate_hook(uid, cat, mood)
        bot.send_message(c.message.chat.id, text, reply_markup=again_kb(cat, mood))

    elif data[0] == "again":
        USER_PRESS[uid] += 1
        prefs = get_prefs(uid)
        prefs["randomness"] = min(0.9, prefs["randomness"] + 0.05)
        _, cat, mood = data
        text = generate_hook(uid, cat, mood)
        bot.send_message(c.message.chat.id, text, reply_markup=again_kb(cat, mood))

    elif data[0] == "copy":
        bot.edit_message_reply_markup(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            reply_markup=again_kb(data[1], data[2], copied=True)
        )
        bot.answer_callback_query(c.id, "Copied ✔️")

    else:
        bot.answer_callback_query(c.id)

# ================= RUN =================
print("🇵🇸 Advanced Palestinian Hook Engine running...")
bot.infinity_polling(skip_pending=True)
