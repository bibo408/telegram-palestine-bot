# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
import re
import time
import hashlib

# ================= BOT INIT =================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= SAFE FILTER =================
BLOCKED = {
    "conflict","violence","violent","resistance","occupation",
    "zion","zionist","jewish","israel","israeli",
    "attack","kill","bomb","destroy","rocket","missile",
    "fraud","scam"
}

def safe(text):
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    return not any(w in BLOCKED for w in words)

SEMANTIC_BLACKLIST = {
    "war": ["battle","fight","combat","clash"],
    "military": ["armed","forces","troops"],
    "destruction": ["ruin","devastation","wreckage"],
}

def semantic_safe(text):
    t = text.lower()
    for root, variants in SEMANTIC_BLACKLIST.items():
        if re.search(rf"\b{root}\b", t):
            return False
        for v in variants:
            if re.search(rf"\b{v}\b", t):
                return False
    return True

# ================= USER MEMORY =================
USER_HISTORY = {}
MEMORY_LIMIT = 300
MEMORY_TTL = 3600 * 6  # 6 hours

def now():
    return int(time.time())

def seen(uid, sig):
    USER_HISTORY.setdefault(uid, {})
    if sig in USER_HISTORY[uid]:
        return now() - USER_HISTORY[uid][sig] < MEMORY_TTL
    return False

def remember(uid, sig):
    USER_HISTORY.setdefault(uid, {})
    USER_HISTORY[uid][sig] = now()
    if len(USER_HISTORY[uid]) > MEMORY_LIMIT:
        USER_HISTORY[uid] = dict(
            sorted(USER_HISTORY[uid].items(), key=lambda x: x[1])[-MEMORY_LIMIT:]
        )

# ================= USER PREFS =================
USER_PREFS = {}

def prefs(uid):
    USER_PREFS.setdefault(uid, {
        "randomness": 0.5
    })
    return USER_PREFS[uid]

# ================= TEXT BANK =================
OPENINGS = {
    "maps": [
        "This is a historical map of Palestine before 1948",
        "An archival cartographic record of Palestine prior to 1948",
        "A documented representation of Palestinian geography before 1948",
        "This map presents Palestine as it was recorded before 1948",
    "This cartographic record shows Palestine prior to the year 1948",
    "This map documents the geography of Palestine before its alteration in 1948",
    "This historical map illustrates Palestine as it existed before 1948",
    "This map captures Palestine in its documented form before 1948",
    "This archival map reflects Palestine’s geographic reality prior to 1948",
    "This map preserves the recorded boundaries of Palestine before 1948",
    "This cartographic reference outlines Palestine as mapped before 1948",
    "This map represents Palestine according to pre-1948 documentation",
    "This recorded map presents Palestine as charted before 1948",

    "This map reflects Palestine based on geographic records before 1948",
    "This cartographic illustration shows Palestine prior to 1948 changes",
    "This map displays Palestine as recognized in maps before 1948",
    "This documented map outlines Palestine’s geography before 1948",
    "This map reconstructs Palestine according to pre-1948 cartography",
    "This archival cartographic source depicts Palestine before 1948",
    "This map illustrates Palestine using documented borders before 1948",
    "This geographic record presents Palestine prior to its redefinition in 1948",
    "This cartographic rendering shows Palestine as defined before 1948",
    "This map records Palestine’s geographic form prior to 1948",

    "This historical cartographic source presents Palestine before 1948",
    "This map displays the documented landscape of Palestine before 1948",
    "This map outlines Palestine according to archival maps before 1948",
    "This cartographic depiction presents Palestine as mapped prior to 1948",
    "This map captures the recognized geography of Palestine before 1948",
    "This documented cartographic map shows Palestine prior to 1948",
    "This map illustrates Palestine’s geographic structure before 1948",
    "This archival geographic record shows Palestine as mapped before 1948",
    "This cartographic presentation reflects Palestine before 1948",
    "This map documents Palestine’s borders as recorded before 1948",

    "This map presents Palestine’s geography according to records before 1948",
    "This historical map records Palestine as it appeared before 1948",
    "This cartographic reference documents Palestine prior to 1948",
    "This map shows Palestine based on documented geography before 1948",
    "This geographic map outlines Palestine as recorded prior to 1948",
    "This map reflects Palestine’s documented landscape before 1948",
    "This archival map shows Palestine in its geographic form before 1948",
    "This cartographic documentation presents Palestine before 1948",
    "This map captures Palestine’s documented borders prior to 1948",
    "This geographic record illustrates Palestine as mapped before 1948"
        "This map states Palestine as a recorded geographic fact before 1948",
    "This cartographic record confirms Palestine’s presence prior to 1948",
    "This map asserts Palestine as a documented land before 1948",
    "This map establishes Palestine as a mapped reality before 1948",
    "This geographic record fixes Palestine in place before 1948",

    "This map affirms Palestine as a documented geography before 1948",
    "This cartographic source anchors Palestine prior to 1948",
    "This map confirms Palestine as a mapped territory before 1948",
    "This documented map leaves no ambiguity about Palestine before 1948",
    "This geographic record secures Palestine’s presence before 1948",

    "This map defines Palestine through recorded geography before 1948",
    "This cartographic evidence places Palestine clearly before 1948",
    "This map asserts Palestine through documented borders before 1948",
    "This geographic documentation establishes Palestine prior to 1948",
    "This map confirms Palestine as geographic reality before 1948",

    "This cartographic record leaves Palestine fixed before 1948",
    "This map positions Palestine as a recorded fact before 1948",
    "This geographic source affirms Palestine’s mapped existence before 1948",
    "This map documents Palestine as an established land before 1948",
    "This cartographic map asserts Palestine before 1948",

    "This map reinforces Palestine as documented geography before 1948",
    "This geographic record confirms Palestine’s territorial presence before 1948",
    "This map establishes Palestine through recorded boundaries before 1948",
    "This cartographic evidence affirms Palestine’s existence before 1948",
    "This map documents Palestine as a geographic certainty before 1948",

    "This geographic map fixes Palestine as a recorded land before 1948",
    "This cartographic record validates Palestine prior to 1948",
    "This map affirms Palestine’s documented territory before 1948",
    "This geographic source confirms Palestine as mapped before 1948",
    "This map asserts Palestine as an established geography before 1948",

    "This cartographic documentation leaves no doubt about Palestine before 1948",
    "This map records Palestine as an indisputable geography before 1948",
    "This geographic record anchors Palestine firmly before 1948",
    "This map establishes Palestine as a territorial fact before 1948",
    "This cartographic source confirms Palestine’s place before 1948",

    "This map fixes Palestine within recorded geography before 1948",
    "This geographic documentation confirms Palestine’s existence before 1948",
    "This cartographic record asserts Palestine without ambiguity before 1948",
    "This map establishes Palestine as mapped land before 1948",
    "This geographic source reinforces Palestine before 1948",

    "This map affirms Palestine as a documented territorial reality before 1948",
    "This cartographic record positions Palestine decisively before 1948",
    "This geographic map confirms Palestine as recorded land before 1948",
    "This map establishes Palestine through documented geography before 1948",
    "This cartographic evidence fixes Palestine prior to 1948"
    ],
    "palestine": [
        "Palestine exists as a continuous historical identity",
        "Palestine remains present through land, memory, and people",
        "Palestine persists beyond time and imposed narratives",
        "Palestine exists as a continuous historical and human reality",
    "Palestine remains present through land, people, and documented history",
    "Palestine stands as an established identity shaped over generations",
    "Palestine persists as a living historical presence without interruption",
    "Palestine continues as a recognized reality rooted in place and memory",

    "Palestine exists beyond narratives imposed upon its history",
    "Palestine remains grounded in geography, culture, and lived experience",
    "Palestine stands as a recorded identity shaped by continuity",
    "Palestine persists through time as a documented historical presence",
    "Palestine exists through an unbroken connection between people and land",

    "Palestine remains present as a historical fact rather than a claim",
    "Palestine stands defined by continuity rather than erasure",
    "Palestine exists as a lived reality sustained across generations",
    "Palestine persists as a recognized presence within recorded history",
    "Palestine remains rooted in place despite imposed disruption",

    "Palestine stands as an enduring historical and cultural entity",
    "Palestine exists through consistent human presence and memory",
    "Palestine remains present as part of documented regional history",
    "Palestine persists beyond attempts to redefine its existence",
    "Palestine stands anchored in geography and collective memory",

    "Palestine exists as a continuous historical landscape",
    "Palestine remains a stable identity shaped by lived experience",
    "Palestine stands as a historical presence maintained over time",
    "Palestine persists as an established reality rather than an idea",
    "Palestine exists through recorded history and ongoing presence",

    "Palestine remains present through generations without interruption",
    "Palestine stands as a documented identity formed through continuity",
    "Palestine exists beyond debate as a historical fact",
    "Palestine persists through land, memory, and human continuity",
    "Palestine remains an enduring presence rooted in lived reality",

    "Palestine stands as a continuous identity shaped by history",
    "Palestine exists as a recorded presence sustained over time",
    "Palestine remains present through geography and human attachment",
    "Palestine persists as a documented historical reality",
    "Palestine stands defined by continuity rather than narrative shifts",

    "Palestine exists as an enduring human and historical presence",
    "Palestine remains present as part of an unbroken historical record",
    "Palestine stands as a stable identity grounded in place",
    "Palestine persists as a lived reality shaped by time",
    "Palestine exists through continuity rather than interruption",

    "Palestine remains present as a historical and cultural fact",
    "Palestine stands as an established reality sustained across generations",
    "Palestine exists as a continuous presence tied to land and people",
    "Palestine persists as a documented identity beyond denial"
        "Palestine exists as a historical fact, not a disputed concept",
    "Palestine remains a documented reality regardless of denial",
    "Palestine stands as an established presence grounded in history",
    "Palestine persists as a fixed reality rather than a narrative",
    "Palestine exists through recorded continuity, not interpretation",

    "Palestine remains present as a matter of historical record",
    "Palestine stands defined by evidence rather than rhetoric",
    "Palestine exists as a confirmed reality rooted in place",
    "Palestine persists as an indisputable historical presence",
    "Palestine remains established beyond argument or revision",

    "Palestine stands as a recorded fact embedded in history",
    "Palestine exists independently of political framing",
    "Palestine remains a continuous presence despite distortion",
    "Palestine persists as a verified reality across generations",
    "Palestine stands fixed within documented historical context",

    "Palestine exists as a grounded reality rather than a claim",
    "Palestine remains present through evidence, not assertion",
    "Palestine stands as an established identity beyond dispute",
    "Palestine persists as a historical constant, not a position",
    "Palestine exists as a proven presence tied to land",

    "Palestine remains anchored in history regardless of denial",
    "Palestine stands as a documented entity beyond reinterpretation",
    "Palestine exists through continuity rather than concession",
    "Palestine persists as a historical certainty, not an opinion",
    "Palestine remains present as a recorded geographical and human reality",

    "Palestine stands established through documented human presence",
    "Palestine exists as an unbroken historical reality",
    "Palestine remains present through recorded continuity of life",
    "Palestine persists as a confirmed identity grounded in history",
    "Palestine stands as a fixed presence immune to erasure",

    "Palestine exists beyond narrative control or denial",
    "Palestine remains a factual presence anchored in documentation",
    "Palestine stands as an established reality within historical record",
    "Palestine persists as a verified presence rather than a debate",
    "Palestine exists as a historical constant rooted in place",

    "Palestine remains present as a matter of documented continuity",
    "Palestine stands as a recorded reality beyond revision",
    "Palestine exists through evidence that resists erasure",
    "Palestine persists as a confirmed historical identity",
    "Palestine remains fixed within the record of history",

    "Palestine stands as an established fact rather than a narrative",
    "Palestine exists as a documented presence beyond denial",
    "Palestine remains a continuous reality grounded in evidence",
    "Palestine persists as an indisputable historical presence",
    "Palestine stands anchored as a verified reality through time"
    ],
    "gaza": [
        "Gaza reflects lived Palestinian reality",
        "Gaza carries Palestinian presence forward",
        "Gaza stands as daily evidence of Palestinian life",
         "Gaza represents a daily reality shaped by resilience and struggle",
    "Gaza stands as a living testament to Palestinian endurance",
    "Gaza reflects the unbroken presence of its people through history",
    "Gaza persists as a continuous hub of Palestinian identity",
    "Gaza remains a documented reality of life and community",

    "Gaza exists as a territory defined by lived Palestinian experience",
    "Gaza embodies the ongoing story of survival and hope",
    "Gaza represents human presence despite persistent challenges",
    "Gaza stands grounded in history and collective memory",
    "Gaza continues to hold the essence of Palestinian culture",

    "Gaza remains present as a community enduring through generations",
    "Gaza reflects the spirit of its people in every street and home",
    "Gaza exists as a living record of continuity and identity",
    "Gaza stands as a witness to resilience against adversity",
    "Gaza persists as a historical and cultural reality",

    "Gaza represents the intersection of heritage and everyday life",
    "Gaza remains anchored in the memory of its inhabitants",
    "Gaza embodies the persistence of Palestinian culture and roots",
    "Gaza exists through human presence and shared experience",
    "Gaza stands as a recorded reality within historical continuity",

    "Gaza continues to thrive through community and collective memory",
    "Gaza reflects the unyielding presence of generations past and present",
    "Gaza exists as a living territory documented in history",
    "Gaza remains a hub of Palestinian life against all odds",
    "Gaza stands as a continuous record of cultural identity",

    "Gaza represents a documented reality shaped by endurance",
    "Gaza persists as a center of human activity and tradition",
    "Gaza remains present through generations of lived experience",
    "Gaza embodies resilience and the continuity of daily life",
    "Gaza exists as a living testament to heritage and memory",

    "Gaza stands as a territory defined by human presence and culture",
    "Gaza reflects the ongoing story of Palestinian perseverance",
    "Gaza continues to exist as a documented community reality",
    "Gaza remains anchored in the historical record of its people",
    "Gaza persists as a living hub of identity and memory",

    "Gaza represents the unbroken continuity of life and culture",
    "Gaza exists as a community that maintains historical presence",
    "Gaza stands as a witness to endurance through generations",
    "Gaza remains present in geography, culture, and lived experience",
    "Gaza embodies the persistence of memory and tradition",

    "Gaza continues as a living reality shaped by resilience and history",
    "Gaza reflects the ongoing presence of human activity and identity",
    "Gaza exists as a documented territory tied to its inhabitants",
    "Gaza remains a continuous center of life, culture, and memory",
    "Gaza stands as a testament to endurance and human spirit",

    "Gaza persists as a historical and cultural reality without interruption",
    "Gaza represents the lived presence of its people across generations",
    "Gaza remains grounded in both memory and everyday life",
    "Gaza embodies resilience, identity, and continuity",
    "Gaza exists as a recorded territory of Palestinian presence"
        "Gaza exists as a concrete reality that cannot be ignored",
    "Gaza stands as a documented hub of life under relentless challenges",
    "Gaza persists as a center of human presence against all adversity",
    "Gaza remains an undeniable territory of Palestinian endurance",
    "Gaza embodies survival as a fixed, historical reality",

    "Gaza is a living record of resilience documented across generations",
    "Gaza continues as a factual presence beyond political debate",
    "Gaza stands confirmed through the continuous life of its people",
    "Gaza exists as an indisputable reality grounded in history",
    "Gaza remains a territory defined by evidence, not opinion",

    "Gaza is present as a documented community, unyielding through time",
    "Gaza persists as an established reality despite all attempts to erase it",
    "Gaza stands as a verified hub of Palestinian culture and identity",
    "Gaza exists as a factual presence resistant to distortion",
    "Gaza remains anchored in lived reality rather than narrative",

    "Gaza embodies continuity through human presence and memory",
    "Gaza persists as an undeniable center of life and culture",
    "Gaza stands as a confirmed record of Palestinian existence",
    "Gaza exists as a fixed reality documented by generations",
    "Gaza remains present regardless of denial or political framing",

    "Gaza continues as a documented territory shaped by resilience",
    "Gaza stands unbroken as a center of daily human activity",
    "Gaza exists through evidence that resists erasure or manipulation",
    "Gaza persists as an established community rooted in history",
    "Gaza remains present as a confirmed reality of life and struggle",

    "Gaza embodies a factual, unalterable presence of its people",
    "Gaza exists as a verified hub of identity and culture",
    "Gaza stands as a recorded reality that cannot be disputed",
    "Gaza persists through generations as a fixed, living territory",
    "Gaza remains documented and anchored in historical evidence",

    "Gaza continues as a reality unshaken by denial or revisionism",
    "Gaza stands as a proven hub of human presence and resilience",
    "Gaza exists as a factual territory defined by lived experience",
    "Gaza persists as a confirmed record of identity and continuity",
    "Gaza remains unaltered in its historical and cultural reality",

    "Gaza embodies survival as a documented fact, not a claim",
    "Gaza exists through undeniable human presence and history",
    "Gaza stands confirmed as a continuous community reality",
    "Gaza persists as a verified center of life and culture",
    "Gaza remains grounded in recorded continuity, unyielding through time",

    "Gaza continues as a factual hub of Palestinian existence and memory",
    "Gaza stands as a fixed reality resistant to erasure or distortion",
    "Gaza exists as a documented center of resilience and culture",
    "Gaza persists as an established presence, beyond debate or interpretation",
    "Gaza remains a living record of human life and identity",

    "Gaza embodies documented continuity and unbroken presence",
    "Gaza exists as a verified territory where life and culture endure",
    "Gaza stands as an undeniable hub of historical and human reality",
    "Gaza persists as a factual record of survival and resistance",
    "Gaza remains present, anchored in generations of lived experience"
    ],
    "memory": [
        "Palestinian memory moves steadily through generations",
        "Memory preserves Palestinian presence without interruption",
        "Palestinian memory records what history cannot erase",
    ],
    "nakba": [
        "The Nakba marked a decisive historical rupture",
        "The Nakba reshaped Palestinian life permanently",
        "The Nakba altered the geography of Palestinian existence",
        "The Nakba reshaped Palestinian lives and communities forever",
    "The Nakba marked a historical turning point for Palestine",
    "The Nakba created a lasting impact on generations of Palestinians",
    "The Nakba altered the course of daily life across the homeland",
    "The Nakba displaced countless families and transformed society",

    "The Nakba remains a defining moment in Palestinian history",
    "The Nakba echoes through the memory of every Palestinian family",
    "The Nakba changed the physical and social landscape of Palestine",
    "The Nakba left permanent scars on communities and culture",
    "The Nakba represents a pivotal chapter in the Palestinian narrative",

    "The Nakba forced entire communities into exile and uncertainty",
    "The Nakba is remembered as a moment of loss and upheaval",
    "The Nakba reshaped cities, towns, and villages across Palestine",
    "The Nakba created enduring challenges for displaced populations",
    "The Nakba continues to influence Palestinian identity and memory",

    "The Nakba redefined borders, homes, and the sense of belonging",
    "The Nakba disrupted generations and altered historical trajectories",
    "The Nakba remains a central point in Palestinian collective memory",
    "The Nakba represents the struggle and resilience of its people",
    "The Nakba shaped the homeland and the lives of its residents",

    "The Nakba displaced communities while preserving cultural identity",
    "The Nakba is etched into the memory of Palestinian society",
    "The Nakba left an undeniable mark on the social fabric of Palestine",
    "The Nakba represents both tragedy and the persistence of life",
    "The Nakba changed the narrative of homeland and displacement",

    "The Nakba forced historical changes that resonate today",
    "The Nakba impacted generations and the continuity of heritage",
    "The Nakba is remembered through stories, memories, and survival",
    "The Nakba reshaped traditions and the structure of communities",
    "The Nakba continues to define the Palestinian experience",

    "The Nakba altered landscapes and lives in profound ways",
    "The Nakba is a historical reality that cannot be overlooked",
    "The Nakba represents displacement, endurance, and memory",
    "The Nakba changed the identity and composition of the homeland",
    "The Nakba remains a point of reflection and collective remembrance",

    "The Nakba disrupted daily life while preserving cultural essence",
    "The Nakba continues to influence families across generations",
    "The Nakba represents the resilience of a displaced population",
    "The Nakba altered both human and geographical landscapes",
    "The Nakba is a permanent chapter in Palestinian history",

    "The Nakba left enduring marks on identity, culture, and memory",
    "The Nakba is remembered through continuity and communal stories",
    "The Nakba reshaped life, society, and historical consciousness",
    "The Nakba continues to echo in Palestinian traditions and culture",
    "The Nakba represents struggle, endurance, and the will to survive",

    "The Nakba changed cities, villages, and the sense of homeland",
    "The Nakba remains a historical fact shaping present realities",
    "The Nakba displaced populations while preserving heritage",
    "The Nakba is documented through memory and collective narrative",
    "The Nakba continues to define Palestinian consciousness today"
        "The Nakba is a stark reality that reshaped Palestine permanently",
    "The Nakba forced entire communities into displacement and survival",
    "The Nakba left an undeniable mark on Palestinian identity",
    "The Nakba destroyed homes while forging resilient memory",
    "The Nakba altered generations with irreversible consequences",

    "The Nakba is documented as a pivotal moment of loss and exile",
    "The Nakba erased landscapes yet preserved human spirit",
    "The Nakba stands as an undeniable chapter of suffering and endurance",
    "The Nakba imposed displacement while strengthening communal bonds",
    "The Nakba reshaped territories and lives beyond reconciliation",

    "The Nakba continues to define the fate of Palestinians today",
    "The Nakba forced historical rupture across cities and villages",
    "The Nakba left families uprooted yet determined to survive",
    "The Nakba altered the homeland and the collective narrative",
    "The Nakba remains a fixed reality that cannot be denied",

    "The Nakba displaced populations while embedding lasting trauma",
    "The Nakba forced survival in the midst of destruction and chaos",
    "The Nakba shaped generations through loss and resistance",
    "The Nakba left scars that continue across the social fabric",
    "The Nakba is a historical truth unshakable by denial or revisionism",

    "The Nakba demolished communities yet preserved memory and identity",
    "The Nakba forced exile while igniting persistence and resilience",
    "The Nakba continues to echo through every Palestinian heart",
    "The Nakba altered borders, lives, and generational continuity",
    "The Nakba remains a central pillar of Palestinian consciousness",

    "The Nakba destroyed physical spaces yet solidified collective memory",
    "The Nakba forced abrupt change while sustaining cultural essence",
    "The Nakba remains an uncompromising historical fact",
    "The Nakba reshaped existence through loss, survival, and testimony",
    "The Nakba persists as an enduring reality of life and struggle",

    "The Nakba uprooted generations while shaping enduring identity",
    "The Nakba is a permanent marker of displacement and resilience",
    "The Nakba altered landscapes while defining memory and presence",
    "The Nakba is a factual record of suffering and perseverance",
    "The Nakba continues to determine the lived reality of Palestinians",

    "The Nakba destroyed neighborhoods while securing historical memory",
    "The Nakba remains an unalterable record of loss and endurance",
    "The Nakba forced survival amidst adversity and displacement",
    "The Nakba is a stark reminder of history that cannot be ignored",
    "The Nakba forged identity through trauma, resistance, and memory",

    "The Nakba left permanent gaps yet ensured communal continuity",
    "The Nakba is an undeniable chapter of suffering and endurance",
    "The Nakba uprooted people while solidifying collective consciousness",
    "The Nakba altered the homeland while embedding historical truth",
    "The Nakba remains a defining moment of struggle and persistence",

    "The Nakba forced change that resonates across generations",
    "The Nakba is a factual imprint on Palestinian land and memory",
    "The Nakba destroyed homes yet preserved the spirit of a nation",
    "The Nakba persists as a documented reality of loss and survival",
    "The Nakba continues to shape identity, culture, and collective life"
    ]
}

MIDDLES = [
    "documented carefully through records, names, and places",
    "preserved with historical accuracy and restraint",
    "recorded without exaggeration or distortion",
    "maintained through continuous human presence",
    "carried forward through lived experience",
    "preserved through memory rather than narration",
    "recorded quietly but without interruption",
    "maintained as part of an unbroken historical record"
    "documented carefully through names, places, and events",
    "recorded with attention to historical and cultural detail",
    "preserved meticulously without adding personal interpretation",
    "observed quietly to reflect accurate past realities",
    "noted systematically through testimonies and archives",

    "traced across historical maps and documented territories",
    "kept authentic through oral histories and written records",
    "archived with precision to maintain factual accuracy",
    "captured methodically from eyewitness accounts",
    "compiled carefully to respect historical integrity",

    "recorded through multiple verified sources and testimonies",
    "documented impartially to avoid distortion of facts",
    "preserved without embellishment or exaggerated claims",
    "observed objectively through photographs and manuscripts",
    "traced thoroughly across documents and family stories",

    "collected from historical texts and community narratives",
    "recorded with careful attention to continuity and context",
    "archived systematically to maintain chronological accuracy",
    "kept true to original sources without reinterpretation",
    "documented to reflect the cultural and social reality",

    "traced accurately across archives and preserved materials",
    "noted with focus on consistency and verified evidence",
    "recorded methodically to maintain historical coherence",
    "documented precisely to respect factual representation",
    "collected rigorously through primary and secondary sources",

    "preserved carefully to ensure generational memory persists",
    "observed without interference to maintain objectivity",
    "documented with scholarly attention and verification",
    "recorded across multiple accounts for reliability",
    "archived systematically for study and historical reference",

    "kept intact to reflect authentic cultural and historical essence",
    "traced meticulously to ensure complete factual coverage",
    "collected through observation and archival research",
    "recorded with academic precision and attention to detail",
    "documented thoroughly without external influence",

    "observed with care to maintain truthful historical depiction",
    "archived with attention to prevent alteration or loss",
    "recorded to reflect the lived experience of communities",
    "documented through careful examination of historical sources",
    "traced with attention to every verified detail",

    "preserved methodically for educational and scholarly purposes",
    "collected with diligence to maintain integrity of records",
    "recorded carefully to avoid misrepresentation of events",
    "archived systematically across verified historical documents",
    "noted objectively without assumptions or exaggerations",

    "documented to maintain continuity and cultural authenticity",
    "traced through reliable testimonies and factual sources",
    "observed systematically to capture accurate historical reality",
    "kept carefully to respect memory and generational knowledge",
    "recorded faithfully without bias or distortion"
    "recorded carefully to preserve the unaltered historical narrative",
    "documented with rigorous attention to every verified detail",
    "traced thoroughly across maps, letters, and archival materials",
    "observed meticulously to reflect the authentic lived experience",
    "kept precise to honor factual consistency and truthfulness",

    "compiled systematically from multiple trustworthy sources",
    "archived attentively to protect cultural and historical integrity",
    "documented methodically without adding subjective commentary",
    "recorded faithfully across eyewitness accounts and documents",
    "preserved accurately to reflect historical reality objectively",

    "traced comprehensively through written and oral testimonies",
    "collected carefully to maintain unbroken factual continuity",
    "observed systematically to capture context and chronology",
    "documented impartially to avoid distortion or bias",
    "archived methodically to ensure authenticity of records",

    "kept intact to respect the original sources and accounts",
    "recorded with careful attention to historical causality",
    "preserved methodically across verified archival evidence",
    "traced accurately to maintain consistency across documents",
    "documented rigorously to safeguard historical accuracy",

    "observed with diligence to reflect true cultural heritage",
    "compiled methodically from original manuscripts and maps",
    "archived with precision to prevent factual errors",
    "recorded carefully to honor the lived reality of communities",
    "traced meticulously to preserve chronological coherence",

    "collected systematically to ensure objective historical reporting",
    "documented thoroughly without interpretive distortion",
    "kept faithful to primary sources across generations",
    "observed methodically for clarity and factual integrity",
    "archived with attention to every verified occurrence",

    "recorded with scholarly rigor to uphold historical truth",
    "preserved carefully for educational and cultural purposes",
    "traced across multiple verified testimonies and documents",
    "documented methodically to retain chronological accuracy",
    "kept intact to safeguard authentic cultural narratives",

    "observed meticulously to capture both context and detail",
    "archived systematically for study and reference",
    "recorded rigorously to avoid exaggeration or omission",
    "preserved with care to maintain factual consistency",
    "traced accurately across historical and cultural records",

    "collected with diligence to maintain authenticity and truth",
    "documented faithfully through archival and oral evidence",
    "kept systematically to ensure reliable historical memory",
    "observed carefully to capture the essence of events",
    "archived meticulously to reflect authentic experiences",

    "recorded methodically across diverse trustworthy sources",
    "preserved attentively to prevent loss or misrepresentation",
    "traced comprehensively through documents and testimonies",
    "documented rigorously to reflect verified historical reality",
    "kept accurate to maintain factual and cultural fidelity",

    "observed carefully for precision and historical integrity",
    "archived systematically to retain verifiable evidence",
    "recorded with meticulous attention to context and detail",
    "preserved thoroughly to ensure objective historical reporting",
    "traced methodically through credible sources and archives",

    "collected attentively to protect continuity of memory",
    "documented with precision to reflect authentic cultural record",
    "kept systematically to ensure clarity and factual accuracy",
    "observed rigorously to capture events faithfully",
    "archived carefully to maintain unbroken historical lineage",

    "recorded thoroughly across multiple independent sources",
    "preserved with care to retain complete historical fidelity",
    "traced systematically through eyewitness accounts and texts",
    "documented meticulously to honor original context and facts",
    "kept accurately to reflect cultural and historical essence",

    "observed with exacting attention to detail and chronology",
    "archived methodically to preserve both record and meaning",
    "recorded with diligence to maintain factual integrity",
    "preserved attentively across multiple generations of records",
    "traced thoroughly to ensure reliable and verified documentation",

    "collected systematically to maintain accurate historical continuity",
    "documented rigorously to reflect authentic lived experience",
    "kept faithful to both oral histories and written evidence",
    "observed methodically to protect the truth of recorded events",
    "archived with precision to reflect authentic cultural heritage",

    "recorded carefully to retain factual accuracy across sources",
    "preserved meticulously for future scholarly reference",
    "traced systematically through credible and verified records",
    "documented attentively to honor original evidence and testimony",
    "kept intact to maintain historical and cultural authenticity",

    "observed rigorously to ensure fidelity of historical record",
    "archived methodically to protect both memory and context",
    "recorded thoroughly with careful attention to chronological order",
    "preserved accurately to reflect documented cultural history",
    "traced comprehensively across diverse reliable sources",

    "collected attentively to maintain precise factual representation",
    "documented with diligence to safeguard historical truth",
    "kept systematically to ensure unaltered cultural continuity",
    "observed carefully to capture verified accounts authentically",
    "archived meticulously to retain objective historical evidence"
    "capturing the harsh reality without sugarcoating or compromise",
    "reflecting undeniable truths despite discomfort or denial",
    "exposing the full impact with unflinching clarity",
    "documenting events as they occurred, harsh and unaltered",
    "revealing consequences that cannot be ignored or softened",

    "illustrating the stark facts with uncompromising honesty",
    "presenting reality without excuses or justification",
    "confronting historical truths with raw accuracy",
    "tracing events sharply to highlight the real consequences",
    "preserving testimony that refuses to be diluted or denied",

    "observing the events with brutal factual precision",
    "capturing the essence of struggle without mitigation",
    "documenting the truth that challenges convenient narratives",
    "exposing realities that demand awareness and action",
    "recording the past in its stark, uncompromised form",

    "highlighting truths that are often silenced or ignored",
    "tracing events rigorously to prevent historical distortion",
    "reflecting reality in all its intensity and consequence",
    "preserving accounts that confront denial and indifference",
    "presenting facts that insist on being acknowledged",

    "revealing the severity of events without softening language",
    "documenting consequences that are hard but unavoidable",
    "exposing the raw outcomes to ensure collective memory",
    "tracing history with uncompromising attention to impact",
    "capturing struggle and resilience in their harshest form",

    "observing events with unyielding factual scrutiny",
    "preserving testimony that resists simplification or erasure",
    "documenting the full gravity of circumstances without bias",
    "tracing consequences with relentless clarity and precision",
    "highlighting truths that challenge complacency and forgetfulness",

    "capturing history’s intensity without filter or compromise",
    "recording reality as a forceful reminder for future generations",
    "exposing facts that demand reflection and reckoning",
    "documenting consequences that cannot be ignored",
    "tracing events to ensure lessons are unmistakably clear",

    "preserving truths that resist erasure or misrepresentation",
    "reflecting the unvarnished impact of historical events",
    "observing events rigorously to confront false narratives",
    "capturing the severity of reality in sharp detail",
    "tracing accounts with relentless commitment to truth",

    "documenting harsh realities without easing discomfort",
    "exposing consequences that challenge mainstream denial",
    "preserving testimony that confronts selective memory",
    "reflecting events in their unfiltered intensity",
    "capturing struggles that demand acknowledgment",

    "observing facts with uncompromising rigor and honesty",
    "tracing history without softening its hard lessons",
    "documenting events that provoke thought and action",
    "highlighting truths that defy erasure and obfuscation",
    "recording realities that confront ignorance and denial",

    "preserving evidence that cannot be conveniently ignored",
    "exposing outcomes that demand collective awareness",
    "capturing struggles without compromise or distortion",
    "documenting history with sharp, unrelenting clarity",
    "tracing facts that resist simplification or omission",

    "reflecting events with uncompromising factual precision",
    "recording consequences that reveal uncomfortable truths",
    "observing history’s harsh realities for all to see",
    "preserving testimony that refuses to be sanitized",
    "tracing the full weight of events without dilution",

    "capturing the raw impact of struggle without distraction",
    "documenting reality that challenges selective memory",
    "exposing the severity of consequences that cannot be ignored",
    "highlighting truths that insist on acknowledgment",
    "preserving accounts that confront distortion or denial",

    "observing historical facts without compromise or bias",
    "tracing events with stark, unwavering clarity",
    "documenting the intensity of struggle and its outcomes",
    "capturing realities that demand recognition and action",
    "preserving evidence that resists obfuscation or erasure",

    "reflecting consequences with unflinching honesty",
    "recording struggles in their full and harsh context",
    "documenting truths that challenge comfortable narratives",
    "tracing events rigorously to ensure historical fidelity",
    "capturing reality with precision that cannot be disputed",

    "exposing outcomes that demand awareness and confrontation",
    "preserving accounts that resist revision and denial",
    "observing events without softening their harsh impact",
    "documenting the raw facts that shape collective memory",
    "tracing historical reality with uncompromising rigor",

    "capturing the severity of struggle with sharp accuracy",
    "reflecting unvarnished truths for present and future",
    "recording consequences that demand acknowledgment",
    "preserving testimony that challenges selective history",
    "documenting events in their full, uncompromised reality",

    "highlighting hard truths that confront denial and ignorance",
    "observing events with exacting, unyielding scrutiny",
    "tracing facts to ensure no distortion or erasure occurs",
    "recording realities that refuse simplification or softening",
    "preserving the stark impact of history for generations ahead"
]

ENDINGS = [
    "as part of Palestinian historical continuity",
    "within Palestinian collective memory",
    "as a documented Palestinian reality",
    "rooted firmly in historical presence",
    "preserved beyond erasure",
    "remaining inseparable from Palestinian identity",
    "connected permanently to place and memory",
    "held intact across generations"
    "remaining undeniably Palestinian in every memory and trace",
    "rooted deeply in Palestinian identity without compromise",
    "connected permanently to the lands and their history",
    "preserved as an unbroken heritage across generations",
    "anchored in historical continuity that resists erasure",

    "ensuring Palestinian memory endures despite adversity",
    "upholding collective identity against distortion",
    "resilient through generations of struggle and survival",
    "standing firm in historical truth without concession",
    "maintaining unshakable identity across time",

    "preserved beyond all attempts at revision or denial",
    "anchored in unchanging roots and ancestral legacy",
    "kept alive across generations as undeniable fact",
    "continuing the historical narrative without dilution",
    "protected as a cultural legacy that cannot be stolen",

    "unwavering in Palestinian reality and presence",
    "affirming historical presence against all erasure",
    "enduring despite challenges to land and memory",
    "rooted in ancestral memory with unbroken continuity",
    "preserved against any attempt to distort history",

    "held firm through time as undeniable evidence",
    "standing as historical truth in every generation",
    "unbroken in identity, culture, and memory",
    "maintained across generations as reality and heritage",
    "resisting dilution of history and collective awareness",

    "embedded in Palestinian consciousness for all to see",
    "secured in cultural memory against oblivion",
    "remaining a testament to heritage and perseverance",
    "anchored in unbroken lineage and ancestral rights",
    "preserved across centuries as undeniable fact",

    "unchanged in historical essence despite external pressure",
    "upholding ancestral narratives with resilience",
    "resilient to external pressures and manipulation",
    "affirming historical continuity without compromise",
    "carried forward through generations untainted",

    "rooted in collective memory as a living reality",
    "maintained as historical truth without distortion",
    "standing strong against erasure and falsification",
    "upholding identity without surrender or alteration",
    "preserved in lived experience and testimony",

    "secured as a national reality and undeniable fact",
    "remaining a symbol of heritage and perseverance",
    "resisting historical manipulation and denial",
    "embedded in the social fabric across generations",
    "maintaining unbroken lineage and rightful legacy",

    "protected through collective memory without dilution",
    "upholding cultural identity as a living testament",
    "continuing the ancestral legacy unaltered",
    "unchanged in its essence and historical importance",
    "affirming resilience through every challenge faced",

    "remaining a beacon of heritage and truth",
    "anchored in enduring truth and cultural presence",
    "preserved in the hearts of people without erasure",
    "secured across history as undeniable reality",
    "maintaining cultural continuity despite adversity",

    "resilient in face of attempts to rewrite history",
    "standing as a symbol of identity and unbroken heritage",
    "upholding tradition and memory with clarity",
    "preserved in collective consciousness and practice",
    "secured in historical narrative without compromise",

    "remaining faithful to memory and ancestral testimony",
    "anchored in enduring identity and historical awareness",
    "maintained through time as a living reminder",
    "resilient across generations as undeniable truth",
    "continuing cultural legacy without distortion",

    "unchanged in its historical essence and significance",
    "affirming identity, heritage, and continuous presence",
    "remaining a testament to unbroken continuity",
    "upholding legacy and tradition without concession",
    "preserved as unbroken heritage for all generations",

    "secured in Palestinian reality and undeniable fact",
    "remaining faithful to collective memory and identity",
    "anchored in enduring values and historical truth",
    "maintained as a living legacy for the future",
    "resilient to historical revisionism and denial",

    "affirming collective memory with uncompromising clarity",
    "carried forward without compromise or distortion",
    "standing as a symbol of continuity and identity",
    "upholding legacy, history, and cultural truth",
    "preserved as unbroken heritage across time"
    "preserved as an indestructible truth of Palestinian life",
    "standing firm as evidence of enduring heritage",
    "rooted deeply in the land and its unyielding history",
    "remaining unbroken through every hardship and exile",
    "anchored in the collective consciousness of generations",

    "ensuring the Palestinian story survives beyond erasure",
    "upholding identity against all forces of suppression",
    "resilient in the face of oppression and denial",
    "standing unwavering amidst attempts to rewrite history",
    "maintaining cultural memory without compromise",

    "preserved across generations as undeniable reality",
    "anchored in unchanging roots of ancestral legacy",
    "kept alive through stories, memory, and land",
    "continuing the narrative without concession",
    "protected as a heritage that cannot be stolen",

    "unwavering in truth despite attempts at falsification",
    "affirming presence where erasure is attempted",
    "enduring against every challenge and attack",
    "rooted in memory that cannot be broken",
    "preserved despite every threat to existence",

    "held steadfast through centuries of struggle",
    "standing as irrefutable evidence of continuity",
    "unbroken in spirit, culture, and identity",
    "maintained as a living testament to resilience",
    "resisting all attempts to distort reality",

    "embedded in Palestinian hearts and minds",
    "secured in cultural memory and practice",
    "remaining a beacon of history and endurance",
    "anchored in unbroken lineage and ancestry",
    "preserved across time as undeniable truth",

    "unchanged in essence despite external pressures",
    "upholding ancestral narratives with strength",
    "resilient to manipulation and historical distortion",
    "affirming continuity without compromise",
    "carried forward with unyielding determination",

    "rooted in collective awareness and lived experience",
    "maintained as truth across generations",
    "standing strong against attempts at denial",
    "upholding identity without surrender",
    "preserved through lived memory and testimony",

    "secured as a cultural and historical reality",
    "remaining a symbol of heritage and defiance",
    "resisting all forms of erasure and revision",
    "embedded in the social fabric without weakening",
    "maintaining unbroken continuity through struggle",

    "protected through collective consciousness",
    "upholding identity as a living legacy",
    "continuing ancestral memory with clarity",
    "unchanged in its essence and purpose",
    "affirming resilience in every circumstance",

    "remaining a beacon of heritage and unyielding truth",
    "anchored in enduring values and cultural identity",
    "preserved in the hearts of generations",
    "secured across time as irrefutable fact",
    "maintaining continuity despite adversity",

    "resilient in face of external challenges",
    "standing as a symbol of heritage and identity",
    "upholding tradition and collective memory",
    "preserved in consciousness across generations",
    "secured in historical narrative without dilution",

    "remaining faithful to memory and ancestral knowledge",
    "anchored in enduring identity and legacy",
    "maintained as a living reminder of history",
    "resilient across generations without alteration",
    "continuing cultural legacy unbroken",

    "unchanged in significance and historical importance",
    "affirming identity, heritage, and continuity",
    "remaining a testament to unbroken history",
    "upholding legacy, tradition, and culture",
    "preserved as living heritage across time",

    "secured in reality and irrefutable truth",
    "remaining faithful to collective memory",
    "anchored in enduring values and authenticity",
    "maintained as a living legacy of resilience",
    "resilient to attempts at distortion and erasure",

    "affirming historical memory without compromise",
    "carried forward without yielding",
    "standing as a symbol of unbroken identity",
    "upholding heritage and history across time",
    "preserved as an undeniable legacy of truth",

    "kept alive in hearts and minds as certainty",
    "anchored in unshakable historical foundations",
    "maintained through struggle and persistence",
    "resilient across time as a testament to heritage",
    "continuing to exist despite every challenge"
]

# ================= QUESTIONS (NEW) =================
QUESTIONS = {
    "palestine": [
        "If this identity never disappeared, why is it still questioned?",
        "What does denial look like when history remains visible?",
        "How much evidence is required before reality is accepted?"
        "Did you ever wonder how Palestine survived through centuries of challenges?",
    "What does the enduring spirit of Palestine teach us about resilience?",
    "Have you considered how Palestinian identity remains unbroken over time?",
    "Why does Palestine continue to inspire generations across the world?",
    "Can the history of Palestine truly be erased despite attempts at denial?",
    "How has Palestinian culture thrived amidst countless struggles?",
    "What makes the story of Palestine so vital for collective memory?",
    "Do you know how Palestinian heritage persists despite adversity?",
    "Why does Palestine stand as a symbol of continuity and pride?",
    "Have you reflected on how Palestinian memory shapes identity today?",
    "What lessons can the world learn from Palestine’s unwavering presence?",
    "How does Palestinian resilience redefine the meaning of endurance?",
    "Can any force truly break the Palestinian connection to their land?",
    "Why does Palestine’s history echo across generations without fading?",
    "Have you thought about how Palestine preserves its cultural essence?",
    "What drives Palestine to remain a beacon of heritage and identity?",
    "Do you see how Palestinian traditions survive against all odds?",
    "How has the spirit of Palestine endured beyond political borders?",
    "Why is Palestinian memory considered a treasure for humanity?",
    "Have you wondered how Palestine’s story remains alive in hearts?",
    "What does it mean for Palestine to exist beyond maps and politics?",
    "Can we truly understand the depth of Palestinian resilience?",
    "Why does Palestine’s identity persist despite displacement and struggle?",
    "How does Palestine maintain its essence through centuries of history?",
    "Have you noticed the strength embedded in Palestinian collective memory?",
    "What makes the Palestinian story essential for global awareness?",
    "Do you realize how Palestine’s heritage shapes generations worldwide?",
    "Why does the history of Palestine demand recognition and respect?",
    "How can Palestine continue to influence culture and memory today?",
    "Have you explored the enduring truths hidden in Palestinian history?",
    "What lessons lie within the unbroken continuity of Palestine?",
    "Why does Palestinian identity remain a symbol of steadfast pride?",
    "How does Palestine defy attempts to erase its story and culture?",
    "Have you reflected on the resilience woven into Palestinian life?",
    "What makes Palestine’s memory an irreplaceable human treasure?",
    "Why does the legacy of Palestine continue to inspire countless lives?",
    "Can the spirit of Palestine ever be diminished or forgotten?",
    "How does Palestinian history remain vivid despite ongoing challenges?",
    "Have you considered the power of memory in sustaining Palestine?",
    "What keeps the Palestinian story alive across generations and borders?",
    "Why does Palestine remain a testament to culture and endurance?",
    "How can we honor the resilience embedded in Palestinian identity?",
    "Have you thought about the lessons Palestine teaches about survival?",
    "What makes Palestinian memory essential for understanding heritage?",
    "Why does the story of Palestine resonate with people worldwide?",
    "How does Palestine preserve its identity amid trials and exile?",
    "Have you questioned the strength behind Palestine’s enduring presence?",
    "What insights can Palestine offer about continuity and resilience?",
    "Why does Palestinian culture continue to thrive despite hardships?",
    "How does Palestine inspire unwavering pride in its people today?",
    "Have you reflected on the unyielding spirit of Palestinian heritage?"
    ],
    "gaza": [
        "If daily life continues, what exactly is claimed to be absent?",
        "Why is lived reality still treated as a debate?",
        "At what point does existence stop needing justification?"
        "How does Gaza continue to thrive despite unimaginable challenges?",
    "Why does the spirit of Gaza remain unbroken through hardship?",
    "Have you wondered how Gaza preserves its culture under pressure?",
    "What lessons can Gaza teach about resilience and endurance?",
    "Can the essence of Gaza ever be erased despite destruction?",
    "Why does Gaza inspire hope and strength across generations?",
    "How does daily life in Gaza reflect unyielding perseverance?",
    "Have you considered how Gaza maintains its identity under siege?",
    "What drives the people of Gaza to keep their heritage alive?",
    "Why does Gaza remain a symbol of courage and survival?",
    "How has Gaza survived waves of adversity and hardship?",
    "Have you reflected on the resilience embedded in Gaza’s communities?",
    "What keeps Gaza’s memory alive despite ongoing struggles?",
    "Why does Gaza’s story resonate with people around the world?",
    "How does Gaza retain its cultural essence amidst chaos?",
    "Have you thought about the strength behind Gaza’s daily life?",
    "What does Gaza’s endurance reveal about human determination?",
    "Why does the spirit of Gaza persist against all odds?",
    "How can Gaza inspire lessons of resilience for the global community?",
    "Have you explored how Gaza sustains hope through every challenge?",
    "What makes Gaza’s identity unshakable despite constant trials?",
    "Why does Gaza continue to reflect courage and collective memory?",
    "How does Gaza preserve its stories through generations?",
    "Have you considered the legacy Gaza carries despite adversity?",
    "What lessons in perseverance can we learn from Gaza today?",
    "Why is Gaza’s history essential for understanding resilience?",
    "How does Gaza embody the spirit of survival and identity?",
    "Have you reflected on the courage woven into Gaza’s heritage?",
    "What keeps the people of Gaza connected to their land and culture?",
    "Why does Gaza remain a beacon of steadfastness and hope?",
    "How can Gaza’s story deepen our understanding of endurance?",
    "Have you considered the strength Gaza demonstrates daily?",
    "What makes Gaza a symbol of collective memory and resilience?",
    "Why does Gaza inspire admiration despite continuous hardship?",
    "How does Gaza preserve its identity through relentless challenges?",
    "Have you thought about the lessons Gaza offers in courage?",
    "What ensures Gaza’s culture and spirit remain unbroken?",
    "Why does the story of Gaza continue to resonate globally?",
    "How does Gaza survive and adapt while preserving its heritage?",
    "Have you reflected on the unyielding spirit of Gaza’s people?",
    "What does Gaza teach about resilience in the face of adversity?",
    "Why does Gaza remain a testament to human perseverance?",
    "How does Gaza continue to shape collective memory and identity?",
    "Have you explored the courage embedded in Gaza’s everyday life?",
    "What keeps Gaza’s heritage alive across generations?",
    "Why does Gaza endure despite overwhelming obstacles?",
    "How does Gaza inspire resilience in communities worldwide?",
    "Have you considered the strength of Gaza’s collective spirit?",
    "What makes Gaza an emblem of hope, courage, and survival?",
    "Why does Gaza’s story reflect unbroken identity and memory?"
    ],
    "maps": [
        "If maps record reality, why are these ones ignored?",
        "When geography is documented, what remains to dispute?",
        "How can erased borders still appear so clearly?"
        "How do historical maps reveal the forgotten geography of Palestine?",
    "What stories do old maps of Palestine silently tell us?",
    "Have you noticed the boundaries marked in pre-1948 maps?",
    "How do maps preserve the memory of Palestinian lands?",
    "Why are historical cartographies crucial for understanding Palestine?",
    "What secrets lie hidden in the maps of Palestinian towns?",
    "How can maps help us trace Palestine’s cultural heritage?",
    "Have you reflected on the changes shown in old Palestinian maps?",
    "What do historical maps teach about Palestine’s resilience?",
    "How do maps capture the essence of Palestinian identity?",
    "Why should we study archived maps of Palestine carefully?",
    "What details in old maps reveal lost Palestinian communities?",
    "How do maps serve as evidence of Palestine’s continuity?",
    "Have you explored the geography recorded in pre-1948 maps?",
    "What insights do historical maps offer about Palestinian life?",
    "How do maps document Palestine’s lands before displacement?",
    "Why are cartographic records vital for Palestinian memory?",
    "What can maps tell us about Palestine that texts cannot?",
    "How do old maps reflect the spirit of Palestinian history?",
    "Have you considered the stories behind mapped Palestinian towns?",
    "What patterns emerge when studying Palestine’s historical maps?",
    "How can cartography preserve the legacy of Palestinian villages?",
    "Why do maps remain powerful tools for remembering Palestine?",
    "What truths about Palestine are hidden in archival maps?",
    "How do maps illustrate the endurance of Palestinian culture?",
    "Have you observed the territorial details in old Palestine maps?",
    "What lessons do maps provide about Palestine’s past struggles?",
    "How do historical maps connect us to Palestinian memory?",
    "Why is cartographic evidence critical for preserving heritage?",
    "What can we learn from the borders drawn in old maps?",
    "How do maps reflect the geographical identity of Palestine?",
    "Have you noticed the historical names preserved in maps?",
    "What makes cartography a key witness of Palestinian history?",
    "How do maps reveal the richness of Palestinian settlements?",
    "Why do maps offer a visual record of Palestinian continuity?",
    "What insights can maps give about pre-1948 Palestinian lands?",
    "How do old maps illustrate changes across Palestinian territories?",
    "Have you explored the towns and villages on historical maps?",
    "What role do maps play in keeping Palestinian memory alive?",
    "How do maps document the spatial story of Palestine?",
    "Why should historical maps be studied alongside Palestinian narratives?",
    "What do maps tell us about the distribution of Palestinian communities?",
    "How do archived maps show the evolution of Palestine over time?",
    "Have you considered how maps preserve cultural geography?",
    "What can cartographic records reveal about lost Palestinian areas?",
    "How do maps maintain the identity of Palestinian lands visually?",
    "Why do historical maps provide undeniable evidence of Palestine?",
    "What hidden details emerge when examining old Palestinian maps?",
    "How do maps capture the continuity of Palestinian towns and cities?",
    "Have you reflected on the precision of Palestinian cartographic records?",
    "What makes maps essential for understanding Palestine’s past?",
    "How do historical maps inspire a connection to Palestinian heritage?"
    ],
    "memory": [
        "If memory is continuous, who decides when it ends?",
        "Why is remembrance feared when it stays consistent?",
        "What threatens power more than uninterrupted memory?"
    ],
    "nakba": [
        "If displacement reshaped everything, why is its cause denied?",
        "How does a rupture vanish if its impact never did?",
        "Who benefits from redefining historical breaks?"
        "How did the Nakba reshape the lives of countless Palestinians?",
    "What stories of resilience emerge from the Nakba’s history?",
    "Have you reflected on the lasting impact of the Nakba on families?",
    "How does the Nakba continue to influence Palestinian identity today?",
    "What lessons can we learn from the displacement caused by the Nakba?",
    "How did the Nakba alter the map of Palestinian communities?",
    "Have you considered the generations affected by the Nakba?",
    "What truths about Palestine are revealed through Nakba narratives?",
    "How does memory preserve the experiences of the Nakba?",
    "Why should the Nakba be remembered across generations?",
    "What role does storytelling play in keeping the Nakba alive?",
    "How did the Nakba shape the cultural heritage of Palestine?",
    "Have you explored the untold stories of Nakba survivors?",
    "What evidence of the Nakba remains visible in Palestinian lands?",
    "How does the Nakba connect past struggles with present identity?",
    "Why is it essential to document every detail of the Nakba?",
    "What impact did the Nakba have on Palestinian towns and villages?",
    "How do personal accounts enrich our understanding of the Nakba?",
    "Have you noticed the long-term effects of the Nakba on communities?",
    "What insights does the Nakba offer about resilience and survival?",
    "How does the Nakba influence Palestinian narratives today?",
    "Why are Nakba testimonies crucial for historical accuracy?",
    "What hidden lessons are embedded in Nakba experiences?",
    "How does the Nakba continue to shape Palestinian memory?",
    "Have you considered the stories of displacement during the Nakba?",
    "What does the Nakba reveal about the loss of homeland?",
    "How can education preserve awareness of the Nakba?",
    "Why is remembering the Nakba a responsibility for every generation?",
    "What patterns of survival emerge from Nakba testimonies?",
    "How do the Nakba’s events echo in contemporary Palestinian life?",
    "Have you reflected on the legacy of Nakba survivors?",
    "What can maps and records tell us about Nakba displacement?",
    "How does the Nakba illustrate the endurance of Palestinian identity?",
    "Why do historical accounts of the Nakba matter today?",
    "What role does collective memory play in remembering the Nakba?",
    "Have you explored the impact of Nakba on Palestinian villages?",
    "How does the Nakba shape the understanding of loss and resilience?",
    "What stories of hope persist despite the tragedy of the Nakba?",
    "How do archives preserve the history of Nakba events?",
    "Have you considered how the Nakba influenced Palestinian culture?",
    "What can personal narratives reveal about the Nakba’s reality?",
    "How does the Nakba continue to inspire remembrance and action?",
    "Why should the Nakba be taught as a central part of history?",
    "What does the Nakba teach about the importance of homeland?",
    "How do survivor testimonies keep the Nakba alive in memory?",
    "Have you noticed the generational impact of the Nakba?",
    "What truths about displacement are exposed by Nakba stories?",
    "How does the Nakba serve as a reminder of resilience and perseverance?",
    "Why is it vital to keep Nakba history accurate and visible?",
    "What lessons about justice emerge from the Nakba?",
    "How do narratives of the Nakba shape Palestinian consciousness?",
    "Have you reflected on the Nakba’s effect on identity and belonging?",
    "What role does remembrance play in honoring Nakba survivors?"
    ]
}

EMOJIS = ["🇵🇸","📜","🕊️","⏳","🗺️"]

HASHTAGS = {
    "palestine": "#Palestine #PalestinianIdentity #Hatshepsut",
    "gaza": "#Gaza #PalestinianMemory #Hatshepsut",
    "maps": "#HistoricalMap #Palestine #Hatshepsut",
    "memory": "#PalestinianMemory #History #Hatshepsut",
    "nakba": "#Nakba #PalestinianMemory #Hatshepsut"
}

# ================= SYNONYMS =================
SYNONYMS = {
    "historical": ["documented","archival","recorded"],
    "preserved": ["maintained","kept","retained"],
    "memory": ["remembrance","collective memory"],
    "exists": ["persists","remains","endures"]
}

def apply_synonyms(text, intensity):
    for w, alts in SYNONYMS.items():
        if random.random() < intensity:
            text = re.sub(rf"\b{w}\b", random.choice(alts), text, count=1)
    return text

# ================= TYPOGRAPHY =================
def typography(text):
    return f"<code>{text}</code>"

# ================= GENERATOR =================
def generate(uid, cat):
    r = prefs(uid)["randomness"]

    o = random.choice(OPENINGS[cat])
    m = random.choice(MIDDLES)
    e = random.choice(ENDINGS)
    q = random.choice(QUESTIONS[cat])
    emoji = random.choice(EMOJIS)

    main_text = f"{o},\n{m},\n{e}. {emoji}"
    main_text = apply_synonyms(main_text, r)

    full_text = (
        f"{main_text}\n\n"
        f"<b>{q}</b>\n\n"
        f"{HASHTAGS[cat]}"
    )

    sig = hashlib.sha1(main_text.encode()).hexdigest()

    if safe(full_text) and semantic_safe(full_text) and not seen(uid, sig):
        remember(uid, sig)
        return typography(full_text)

    remember(uid, sig)
    return typography(full_text)

# ================= UI =================
CATEGORIES = {
    "palestine": "🇵🇸 فلسطين",
    "gaza": "🔥 غزة",
    "maps": "🗺️ خرائط فلسطين",
    "memory": "📜 الذاكرة الفلسطينية",
    "nakba": "🕊️ النكبة"
}

def cat_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    for k,v in CATEGORIES.items():
        kb.add(InlineKeyboardButton(v, callback_data=f"cat|{k}"))
    return kb

def again_kb(cat):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Generate Again", callback_data=f"again|{cat}"),
        InlineKeyboardButton("📋 Copy", callback_data="copy")
    )
    return kb

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, "🇵🇸 اختار القسم:", reply_markup=cat_kb())

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    data = c.data.split("|")
    uid = c.from_user.id

    if data[0] == "cat":
        cat = data[1]
        txt = generate(uid, cat)
        bot.send_message(c.message.chat.id, txt, reply_markup=again_kb(cat))

    elif data[0] == "again":
        cat = data[1]
        prefs(uid)["randomness"] = min(0.9, prefs(uid)["randomness"] + 0.07)
        txt = generate(uid, cat)
        bot.send_message(c.message.chat.id, txt, reply_markup=again_kb(cat))

    elif data[0] == "copy":
        bot.answer_callback_query(c.id, "Copied ✔️")

# ================= RUN =================
print("🇵🇸 Strong Tone + Question Engine running...")
bot.infinity_polling(skip_pending=True)


