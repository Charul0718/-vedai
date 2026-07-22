from __future__ import annotations

import json
import os
from typing import Any

from knowledge_engine import KnowledgeEngine


# --- Planet dignity constants ---

PLANET_OWN_SIGNS: dict[str, list[str]] = {
    "Sun": ["Leo"],
    "Moon": ["Cancer"],
    "Mars": ["Aries", "Scorpio"],
    "Mercury": ["Gemini", "Virgo"],
    "Jupiter": ["Sagittarius", "Pisces"],
    "Venus": ["Taurus", "Libra"],
    "Saturn": ["Capricorn", "Aquarius"],
    "Rahu": ["Aquarius"],
    "Ketu": ["Pisces"],
}

EXALTATION_SIGNS: dict[str, str] = {
    "Sun": "Aries",
    "Moon": "Taurus",
    "Mars": "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus": "Pisces",
    "Saturn": "Libra",
    "Rahu": "Taurus",
    "Ketu": "Scorpio",
}

DEBILITATION_SIGNS: dict[str, str] = {
    "Sun": "Libra",
    "Moon": "Scorpio",
    "Mars": "Cancer",
    "Mercury": "Pisces",
    "Jupiter": "Capricorn",
    "Venus": "Virgo",
    "Saturn": "Aries",
    "Rahu": "Scorpio",
    "Ketu": "Taurus",
}

FRIEND_MAP: dict[str, list[str]] = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Mercury", "Venus"],
    "Rahu": [],
    "Ketu": [],
}


def _load_domain_rules() -> dict[str, Any]:
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    with open(os.path.join(data_dir, "domain_rules.json"), "r") as f:
        return json.load(f)


def get_planet_dignity(planet: str, sign: str) -> str:
    """Determine planet's dignity in a sign: exalted, own_sign, friendly, neutral, enemy, debilitated."""
    if sign == EXALTATION_SIGNS.get(planet):
        return "exalted"
    if sign in PLANET_OWN_SIGNS.get(planet, []):
        return "own_sign"
    if sign == DEBILITATION_SIGNS.get(planet):
        return "debilitated"

    sign_ruler = None
    for p, signs in PLANET_OWN_SIGNS.items():
        if sign in signs:
            sign_ruler = p
            break

    if sign_ruler and sign_ruler in FRIEND_MAP.get(planet, []):
        return "friendly"

    return "neutral"


def score_planet_for_domain(
    planet_name: str,
    house_number: int,
    sign: str,
    is_retrograde: bool,
    domain: str,
    engine: KnowledgeEngine,
    rules: dict[str, Any] | None = None,
) -> tuple[float, str]:
    """Score a single planet's contribution to a domain. Returns (score, explanation)."""
    if rules is None:
        rules = _load_domain_rules()

    domain_rules = rules["domains"][domain]
    dignity_scores = rules["dignityScores"]
    retro_mod = rules["retrogradeModifier"]

    dignity = get_planet_dignity(planet_name, sign)
    dignity_score = dignity_scores.get(dignity, 0.4)

    house_weight = domain_rules["houseWeights"].get(str(house_number), 0.3)
    planet_weight = domain_rules["planetWeights"].get(planet_name, 0.3)

    raw_score = dignity_score * house_weight * planet_weight

    if is_retrograde:
        raw_score *= retro_mod

    # Get domain theme relevance from knowledge base
    domain_themes_key = f"{domain}_themes"
    planet_data = engine.get_planet(planet_name)
    sign_data = engine.get_sign(sign)

    theme_keywords: list[str] = []
    if planet_data and domain_themes_key in planet_data:
        theme_keywords = planet_data[domain_themes_key]
    if sign_data and domain_themes_key in sign_data:
        theme_keywords = theme_keywords + sign_data[domain_themes_key]

    domain_relevance = theme_keywords[0] if theme_keywords else f"{planet_name} in {sign} (House {house_number})"

    parts = [f"{planet_name} in House {house_number} ({sign}, dignity: {dignity})"]
    if is_retrograde:
        parts.append("retrograde")
    if raw_score > 0.3:
        parts.append(f"strongly supports {domain}")
    elif raw_score > 0:
        parts.append(f"supports {domain}")
    elif raw_score > -0.1:
        parts.append(f"neutral for {domain}")
    else:
        parts.append(f"challenges {domain}")
    parts.append(f"— {domain_relevance}")

    return raw_score, ". ".join(parts)


def compute_domain_score(
    chart: dict,
    domain: str,
    engine: KnowledgeEngine,
    rules: dict[str, Any] | None = None,
) -> tuple[float, list[tuple[float, str]]]:
    """Compute aggregate domain score from all planets. Returns (score 0-10, per-planet results)."""
    if rules is None:
        rules = _load_domain_rules()

    planets = chart.get("planets", [])
    domain_rules = rules["domains"][domain]
    base_score = rules["baseScore"]
    min_score = rules["minScore"]
    max_score = rules["maxScore"]

    primary_planets = set(domain_rules["primaryPlanets"])
    secondary_planets = set(domain_rules["secondaryPlanets"])
    all_relevant = primary_planets | secondary_planets

    results: list[tuple[float, str]] = []
    total_adjustment = 0.0

    for p in planets:
        if p["name"] not in all_relevant:
            continue

        score, explanation = score_planet_for_domain(
            planet_name=p["name"],
            house_number=p["house"],
            sign=p["sign"],
            is_retrograde=p.get("isRetrograde", False),
            domain=domain,
            engine=engine,
            rules=rules,
        )

        is_primary = p["name"] in primary_planets
        weight_mult = 1.2 if is_primary else 0.8
        adjusted = score * weight_mult

        results.append((adjusted, explanation))
        total_adjustment += adjusted

    raw_final = base_score + total_adjustment
    final_score = max(min_score, min(max_score, round(raw_final, 2)))

    return final_score, results
