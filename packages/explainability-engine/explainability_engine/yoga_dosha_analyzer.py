from __future__ import annotations

from typing import Any

from knowledge_engine import KnowledgeEngine

# Natural planet rulers for house lords
_SIGN_TO_LORD: dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

KENDRA_HOUSES = {1, 4, 7, 10}
TRIKONA_HOUSES = {1, 5, 9}
MANGAL_DOSH_HOUSES = {1, 4, 7, 8, 12}

# Domain impacts for yogas and doshas
_YOGA_DOMAIN_IMPACT: dict[str, dict[str, float]] = {
    "Raj Yoga": {"career": 0.15, "finance": 0.1, "marriage": 0.05, "relationships": 0.05, "children": 0.03, "health": 0.03, "education": 0.05, "business": 0.1, "spirituality": 0.05},
    "Gaja Kesari Yoga": {"career": 0.1, "finance": 0.12, "marriage": 0.08, "relationships": 0.07, "children": 0.08, "health": 0.05, "education": 0.1, "business": 0.08, "spirituality": 0.08},
    "Budhaditya Yoga": {"career": 0.08, "finance": 0.06, "marriage": 0.04, "relationships": 0.05, "children": 0.03, "health": 0.03, "education": 0.12, "business": 0.06, "spirituality": 0.03},
    "Ruchaka Yoga": {"career": 0.13, "finance": 0.07, "marriage": -0.02, "relationships": -0.01, "children": 0.02, "health": 0.05, "education": 0.03, "business": 0.07, "spirituality": 0.03},
    "Bhadra Yoga": {"career": 0.1, "finance": 0.08, "marriage": 0.05, "relationships": 0.06, "children": 0.04, "health": 0.03, "education": 0.12, "business": 0.08, "spirituality": 0.04},
    "Hamsa Yoga": {"career": 0.1, "finance": 0.1, "marriage": 0.07, "relationships": 0.07, "children": 0.08, "health": 0.05, "education": 0.1, "business": 0.07, "spirituality": 0.12},
    "Malavya Yoga": {"career": 0.07, "finance": 0.08, "marriage": 0.13, "relationships": 0.12, "children": 0.04, "health": 0.04, "education": 0.04, "business": 0.07, "spirituality": 0.05},
    "Shasha Yoga": {"career": 0.1, "finance": 0.08, "marriage": 0.03, "relationships": 0.03, "children": 0.02, "health": -0.02, "education": 0.05, "business": 0.08, "spirituality": 0.08},
    "Dhan Yoga": {"career": 0.07, "finance": 0.15, "marriage": 0.05, "relationships": 0.04, "children": 0.03, "health": 0.03, "education": 0.04, "business": 0.12, "spirituality": 0.03},
    "Aristha Yoga": {"career": -0.1, "finance": -0.08, "marriage": -0.07, "relationships": -0.06, "children": -0.05, "health": -0.1, "education": -0.05, "business": -0.07, "spirituality": 0.03},
    "Vipreet Raj Yoga": {"career": 0.08, "finance": 0.07, "marriage": 0.05, "relationships": 0.05, "children": 0.03, "health": 0.06, "education": 0.04, "business": 0.07, "spirituality": 0.08},
}

_DOSHA_DOMAIN_IMPACT: dict[str, dict[str, float]] = {
    "Kaal Sarp Dosh": {"career": -0.08, "finance": -0.07, "marriage": -0.06, "relationships": -0.05, "children": -0.04, "health": -0.06, "education": -0.05, "business": -0.06, "spirituality": 0.05},
    "Mangal Dosh": {"career": 0.03, "finance": 0.02, "marriage": -0.12, "relationships": -0.08, "children": -0.02, "health": -0.03, "education": 0.01, "business": 0.02, "spirituality": 0.01},
    "Pitra Dosh": {"career": -0.06, "finance": -0.05, "marriage": -0.05, "relationships": -0.04, "children": -0.03, "health": -0.05, "education": -0.04, "business": -0.05, "spirituality": 0.04},
    "Shani Dosh": {"career": -0.05, "finance": -0.04, "marriage": -0.05, "relationships": -0.03, "children": -0.03, "health": -0.07, "education": -0.03, "business": -0.04, "spirituality": 0.05},
    "Chandra Dosh": {"career": -0.03, "finance": -0.03, "marriage": -0.05, "relationships": -0.06, "children": -0.03, "health": -0.06, "education": -0.03, "business": -0.03, "spirituality": 0.03},
    "Guru Dosh": {"career": -0.05, "finance": -0.06, "marriage": -0.04, "relationships": -0.03, "children": -0.05, "health": -0.04, "education": -0.08, "business": -0.05, "spirituality": -0.06},
    "Shukra Dosh": {"career": -0.03, "finance": -0.04, "marriage": -0.1, "relationships": -0.09, "children": -0.02, "health": -0.04, "education": -0.02, "business": -0.04, "spirituality": -0.02},
    "Budh Dosh": {"career": -0.04, "finance": -0.04, "marriage": -0.03, "relationships": -0.03, "children": -0.02, "health": -0.04, "education": -0.07, "business": -0.04, "spirituality": -0.02},
    "Rahu Dosh": {"career": -0.04, "finance": -0.05, "marriage": -0.05, "relationships": -0.04, "children": -0.02, "health": -0.05, "education": -0.03, "business": -0.04, "spirituality": -0.03},
    "Ketu Dosh": {"career": -0.03, "finance": -0.03, "marriage": -0.03, "relationships": -0.03, "children": -0.02, "health": -0.04, "education": -0.02, "business": -0.03, "spirituality": 0.06},
}


def _mutual_aspect_or_conjunction(p1: dict, p2: dict) -> bool:
    """Check if two planets are in conjunction (same sign) or mutual aspect."""
    if p1["sign"] == p2["sign"]:
        return True
    diff = (p1["house"] - p2["house"]) % 12
    if diff == 6:
        return True
    if p1["name"] == "Jupiter" and diff in (4, 8):
        return True
    if p2["name"] == "Jupiter" and (-diff) % 12 in (4, 8):
        return True
    if p1["name"] == "Mars" and diff in (3, 7):
        return True
    if p2["name"] == "Mars" and (-diff) % 12 in (3, 7):
        return True
    if p1["name"] == "Saturn" and diff in (2, 9):
        return True
    if p2["name"] == "Saturn" and (-diff) % 12 in (2, 9):
        return True
    return False


def detect_yogas(chart: dict, engine: KnowledgeEngine) -> list[tuple[str, str, dict]]:
    """Detect present yogas in chart. Returns list of (yoga_name, formation_description, knowledge_data)."""
    planets = chart.get("planets", [])
    detected: list[tuple[str, str, dict]] = []

    # Gaja Kesari: Jupiter in kendra from Moon
    kendra_planets = {p["name"]: p["house"] for p in planets if p["house"] in KENDRA_HOUSES}
    moon_house = next((p["house"] for p in planets if p["name"] == "Moon"), None)
    if moon_house is not None and "Jupiter" in kendra_planets:
        jup_house = kendra_planets["Jupiter"]
        diff = (jup_house - moon_house) % 12
        if diff in (0, 3, 6, 9):
            data = engine.get_yoga("Gaja Kesari Yoga") or {}
            detected.append(("Gaja Kesari Yoga", "Jupiter in kendra from Moon", data))

    # Budhaditya: Sun and Mercury conjunction
    sun = next((p for p in planets if p["name"] == "Sun"), None)
    mer = next((p for p in planets if p["name"] == "Mercury"), None)
    if sun and mer and sun["sign"] == mer["sign"]:
        data = engine.get_yoga("Budhaditya Yoga") or {}
        detected.append(("Budhaditya Yoga", "Sun-Mercury conjunction", data))

    # Panch Mahapurusha yogas
    _check_panch_mahapurusha(planets, kendra_planets, engine, detected)

    # Raj Yoga: kendra and trikona lords in mutual aspect/conjunction
    _check_raj_yoga(planets, engine, detected)

    # Dhan Yoga: lords of 2, 5, 9, 11 in mutual aspect/conjunction
    _check_dhan_yoga(planets, chart, engine, detected)

    # Vipreet Raj Yoga: lords of 6, 8, 12 in 6, 8, 12
    _check_vipreet_raj_yoga(planets, chart, engine, detected)

    # Aristha Yoga: malefics in kendra
    _check_aristha_yoga(planets, engine, detected)

    return detected


def _check_panch_mahapurusha(planets: list[dict], kendra_planets: dict[str, int], engine: KnowledgeEngine, detected: list):
    _own_signs = {
        "Mercury": ["Gemini", "Virgo"],
        "Venus": ["Taurus", "Libra"],
        "Mars": ["Aries", "Scorpio"],
        "Jupiter": ["Sagittarius", "Pisces"],
        "Saturn": ["Capricorn", "Aquarius"],
    }
    _exalted_signs = {
        "Mercury": "Virgo",
        "Venus": "Pisces",
        "Mars": "Capricorn",
        "Jupiter": "Cancer",
        "Saturn": "Libra",
    }
    _yoga_names = {
        "Mercury": "Bhadra Yoga",
        "Venus": "Malavya Yoga",
        "Mars": "Ruchaka Yoga",
        "Jupiter": "Hamsa Yoga",
        "Saturn": "Shasha Yoga",
    }
    for pname in ["Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
        if pname not in kendra_planets:
            continue
        p = next((x for x in planets if x["name"] == pname), None)
        if not p:
            continue
        own = _own_signs.get(pname, [])
        exalt = _exalted_signs.get(pname, "")
        if p["sign"] in own or p["sign"] == exalt:
            yname = _yoga_names[pname]
            data = engine.get_yoga(yname) or {}
            detected.append((yname, f"{pname} in own/exalted sign in kendra", data))


def _check_raj_yoga(planets: list[dict], engine: KnowledgeEngine, detected: list):
    jup = next((p for p in planets if p["name"] == "Jupiter"), None)
    sun = next((p for p in planets if p["name"] == "Sun"), None)
    if jup and sun and _mutual_aspect_or_conjunction(jup, sun):
        data = engine.get_yoga("Raj Yoga") or {}
        detected.append(("Raj Yoga", "Jupiter-Sun mutual aspect/conjunction", data))

    ven = next((p for p in planets if p["name"] == "Venus"), None)
    moon = next((p for p in planets if p["name"] == "Moon"), None)
    if ven and moon and _mutual_aspect_or_conjunction(ven, moon):
        data = engine.get_yoga("Raj Yoga") or {}
        detected.append(("Raj Yoga", "Venus-Moon mutual aspect/conjunction", data))


def _check_dhan_yoga(planets: list[dict], chart: dict, engine: KnowledgeEngine, detected: list):
    houses = chart.get("houses", [])
    house_lords: dict[int, str] = {}
    for h in houses:
        num = h.get("number", h.get("houseNumber", 0))
        sign = h.get("sign", "")
        if num in (2, 5, 9, 11) and sign in _SIGN_TO_LORD:
            house_lords[num] = _SIGN_TO_LORD[sign]

    wealth_lords = list(house_lords.values())
    for i, lord1 in enumerate(wealth_lords):
        for lord2 in wealth_lords[i + 1:]:
            p1 = next((p for p in planets if p["name"] == lord1), None)
            p2 = next((p for p in planets if p["name"] == lord2), None)
            if p1 and p2 and _mutual_aspect_or_conjunction(p1, p2):
                data = engine.get_yoga("Dhan Yoga") or {}
                detected.append(("Dhan Yoga", f"Lords of wealth houses ({lord1}, {lord2}) linked", data))
                return


def _check_vipreet_raj_yoga(planets: list[dict], chart: dict, engine: KnowledgeEngine, detected: list):
    houses = chart.get("houses", [])
    dusthana_lords: list[str] = []
    for h in houses:
        num = h.get("number", h.get("houseNumber", 0))
        sign = h.get("sign", "")
        if num in (6, 8, 12) and sign in _SIGN_TO_LORD:
            dusthana_lords.append(_SIGN_TO_LORD[sign])

    for i, lord1 in enumerate(dusthana_lords):
        for lord2 in dusthana_lords[i + 1:]:
            p1 = next((p for p in planets if p["name"] == lord1), None)
            p2 = next((p for p in planets if p["name"] == lord2), None)
            if p1 and p2 and _mutual_aspect_or_conjunction(p1, p2):
                data = engine.get_yoga("Vipreet Raj Yoga") or {}
                detected.append(("Vipreet Raj Yoga", f"Dusthana lords ({lord1}, {lord2}) in exchange", data))
                return


def _check_aristha_yoga(planets: list[dict], engine: KnowledgeEngine, detected: list):
    malefics = {"Mars", "Saturn", "Rahu", "Ketu", "Sun"}
    malefic_count_kendra = sum(1 for p in planets if p["name"] in malefics and p["house"] in KENDRA_HOUSES)
    if malefic_count_kendra >= 2:
        data = engine.get_yoga("Aristha Yoga") or {}
        detected.append(("Aristha Yoga", f"{malefic_count_kendra} malefics in kendra", data))


def detect_doshas(chart: dict, engine: KnowledgeEngine) -> list[tuple[str, str, dict]]:
    """Detect present doshas in chart. Returns list of (dosha_name, formation_description, knowledge_data)."""
    planets = chart.get("planets", [])
    detected: list[tuple[str, str, dict]] = []

    rahu = next((p for p in planets if p["name"] == "Rahu"), None)
    ketu = next((p for p in planets if p["name"] == "Ketu"), None)

    # Kaal Sarp Dosh
    if rahu and ketu:
        rahu_house = rahu["house"]
        ketu_house = ketu["house"]
        between_count = 0
        for p in planets:
            if p["name"] in ("Rahu", "Ketu"):
                continue
            h = p["house"]
            if rahu_house < ketu_house:
                if rahu_house < h < ketu_house:
                    between_count += 1
            else:
                if h > rahu_house or h < ketu_house:
                    between_count += 1
        if between_count == 7:
            data = engine.get_dosha("Kaal Sarp Dosh") or {}
            detected.append(("Kaal Sarp Dosh", "All 7 planets between Rahu and Ketu", data))

    # Mangal Dosh
    mars = next((p for p in planets if p["name"] == "Mars"), None)
    if mars and mars["house"] in MANGAL_DOSH_HOUSES:
        data = engine.get_dosha("Mangal Dosh") or {}
        detected.append(("Mangal Dosh", f"Mars in house {mars['house']}", data))

    # Pitra Dosh
    sun = next((p for p in planets if p["name"] == "Sun"), None)
    if sun:
        if rahu and sun["sign"] == rahu["sign"]:
            data = engine.get_dosha("Pitra Dosh") or {}
            detected.append(("Pitra Dosh", "Sun conjunct Rahu", data))
        elif ketu and sun["sign"] == ketu["sign"]:
            data = engine.get_dosha("Pitra Dosh") or {}
            detected.append(("Pitra Dosh", "Sun conjunct Ketu", data))

    # Shani Dosh
    saturn = next((p for p in planets if p["name"] == "Saturn"), None)
    moon = next((p for p in planets if p["name"] == "Moon"), None)
    if saturn:
        if saturn["house"] in (1, 4, 7, 8, 12):
            data = engine.get_dosha("Shani Dosh") or {}
            detected.append(("Shani Dosh", f"Saturn in house {saturn['house']}", data))
        elif sun and saturn["sign"] == sun["sign"]:
            data = engine.get_dosha("Shani Dosh") or {}
            detected.append(("Shani Dosh", "Saturn conjunct Sun", data))
        elif moon and saturn["sign"] == moon["sign"]:
            data = engine.get_dosha("Shani Dosh") or {}
            detected.append(("Shani Dosh", "Saturn conjunct Moon", data))

    # Chandra Dosh
    if moon:
        if moon["house"] in (6, 8, 12):
            data = engine.get_dosha("Chandra Dosh") or {}
            detected.append(("Chandra Dosh", f"Moon in house {moon['house']}", data))
        elif rahu and moon["sign"] == rahu["sign"]:
            data = engine.get_dosha("Chandra Dosh") or {}
            detected.append(("Chandra Dosh", "Moon conjunct Rahu", data))
        elif saturn and moon["sign"] == saturn["sign"]:
            data = engine.get_dosha("Chandra Dosh") or {}
            detected.append(("Chandra Dosh", "Moon conjunct Saturn", data))

    # Guru Dosh
    jupiter = next((p for p in planets if p["name"] == "Jupiter"), None)
    if jupiter:
        if jupiter["house"] in (6, 8, 12):
            data = engine.get_dosha("Guru Dosh") or {}
            detected.append(("Guru Dosh", f"Jupiter in house {jupiter['house']}", data))
        elif rahu and jupiter["sign"] == rahu["sign"]:
            data = engine.get_dosha("Guru Dosh") or {}
            detected.append(("Guru Dosh", "Jupiter conjunct Rahu", data))

    # Shukra Dosh
    venus = next((p for p in planets if p["name"] == "Venus"), None)
    if venus:
        if venus["house"] in (6, 8, 12):
            data = engine.get_dosha("Shukra Dosh") or {}
            detected.append(("Shukra Dosh", f"Venus in house {venus['house']}", data))
        elif rahu and venus["sign"] == rahu["sign"]:
            data = engine.get_dosha("Shukra Dosh") or {}
            detected.append(("Shukra Dosh", "Venus conjunct Rahu", data))

    # Budh Dosh
    mercury = next((p for p in planets if p["name"] == "Mercury"), None)
    if mercury:
        if mercury["house"] in (6, 8, 12):
            data = engine.get_dosha("Budh Dosh") or {}
            detected.append(("Budh Dosh", f"Mercury in house {mercury['house']}", data))
        elif rahu and mercury["sign"] == rahu["sign"]:
            data = engine.get_dosha("Budh Dosh") or {}
            detected.append(("Budh Dosh", "Mercury conjunct Rahu", data))

    # Rahu Dosh
    if rahu and rahu["house"] in (1, 4, 7, 8, 12):
        data = engine.get_dosha("Rahu Dosh") or {}
        detected.append(("Rahu Dosh", f"Rahu in house {rahu['house']}", data))

    # Ketu Dosh
    if ketu and ketu["house"] in (1, 4, 7, 8, 12):
        data = engine.get_dosha("Ketu Dosh") or {}
        detected.append(("Ketu Dosh", f"Ketu in house {ketu['house']}", data))

    return detected


def get_yoga_dosha_adjustments(
    chart: dict,
    domain: str,
    engine: KnowledgeEngine,
) -> tuple[float, list[str], list[str]]:
    """Get cumulative yoga/dosha score adjustment for a domain.

    Returns: (adjustment, yoga_descriptions, dosha_descriptions)
    """
    yogas = detect_yogas(chart, engine)
    doshas = detect_doshas(chart, engine)

    adjustment = 0.0
    yoga_descs: list[str] = []
    dosha_descs: list[str] = []

    for yname, formation, _ in yogas:
        impact = _YOGA_DOMAIN_IMPACT.get(yname, {}).get(domain, 0.0)
        adjustment += impact
        yoga_descs.append(f"{yname} ({formation}): {'+'if impact > 0 else ''}{impact:.3f}")

    for dname, formation, _ in doshas:
        impact = _DOSHA_DOMAIN_IMPACT.get(dname, {}).get(domain, 0.0)
        adjustment += impact
        dosha_descs.append(f"{dname} ({formation}): {'+'if impact > 0 else ''}{impact:.3f}")

    return adjustment, yoga_descs, dosha_descs
