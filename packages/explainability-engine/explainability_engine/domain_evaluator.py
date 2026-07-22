from __future__ import annotations

from typing import Any

from knowledge_engine import KnowledgeEngine

from .types import DomainResult, Evidence, ReasoningStep, PlanetaryEvidence, LifeDomain
from .planet_scorer import compute_domain_score, get_planet_dignity, _load_domain_rules
from .yoga_dosha_analyzer import get_yoga_dosha_adjustments, detect_yogas, detect_doshas
from .dasha_analyzer import get_dasha_adjustment


_SIGN_TO_LORD: dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}


def _get_house_lord(house_sign: str) -> str:
    return _SIGN_TO_LORD.get(house_sign, "Unknown")


def _build_planetary_evidence(chart: dict, domain: str, rules: dict[str, Any]) -> list[PlanetaryEvidence]:
    """Build detailed planetary evidence for each planet in the chart."""
    planets = chart.get("planets", [])
    domain_rules = rules["domains"][domain]
    primary_planets = set(domain_rules["primaryPlanets"])
    secondary_planets = set(domain_rules["secondaryPlanets"])
    evidence: list[PlanetaryEvidence] = []

    for p in planets:
        house_num = p["house"]
        is_primary = p["name"] in primary_planets
        is_secondary = p["name"] in secondary_planets

        role = ""
        if is_primary:
            role = "primary_planet"
        elif is_secondary:
            role = "secondary_planet"

        # Check if planet is lord of a key house
        houses = chart.get("houses", [])
        for h in houses:
            h_num = h.get("number", h.get("houseNumber", 0))
            h_sign = h.get("sign", "")
            if _get_house_lord(h_sign) == p["name"]:
                role = f"lord_of_house_{h_num}"
                break

        dignity = get_planet_dignity(p["name"], p["sign"])
        domain_themes_key = f"{domain}_themes"
        planet_data_obj = None
        theme_keywords: list[str] = []
        from knowledge_engine import KnowledgeEngine as KE
        # Use the rules for scoring
        dignity_scores = rules["dignityScores"]
        dignity_score = dignity_scores.get(dignity, 0.4)
        house_weight = domain_rules["houseWeights"].get(str(house_num), 0.3)
        planet_weight = domain_rules["planetWeights"].get(p["name"], 0.3)
        contribution = dignity_score * house_weight * planet_weight

        if p.get("isRetrograde", False):
            contribution *= rules["retrogradeModifier"]

        evidence.append(PlanetaryEvidence(
            planet=p["name"],
            house=p["house"],
            sign=p["sign"],
            isRetrograde=p.get("isRetrograde", False),
            role=role,
            contribution=round(contribution, 2),
        ))

    return evidence


def _build_supporting_challenging_factors(
    chart: dict,
    domain: str,
    engine: KnowledgeEngine,
    planet_results: list[tuple[float, str]],
    yoga_adjustment: float,
    dosha_adjustment: float,
    dasha_adjustment: float,
    rules: dict[str, Any],
) -> tuple[list[Evidence], list[Evidence]]:
    """Separate supporting and challenging factors."""
    supporting: list[Evidence] = []
    challenging: list[Evidence] = []

    planets = chart.get("planets", [])
    domain_rules = rules["domains"][domain]
    primary_planets = set(domain_rules["primaryPlanets"])
    secondary_planets = set(domain_rules["secondaryPlanets"])
    all_relevant = primary_planets | secondary_planets

    # Planet-based factors
    relevant_idx = 0
    for p in planets:
        if p["name"] not in all_relevant:
            continue
        if relevant_idx < len(planet_results):
            score, explanation = planet_results[relevant_idx]
            source = f"planet:{p['name']}"
            if score > 0.05:
                supporting.append(Evidence(
                    factor=f"{p['name']} placement",
                    source=source,
                    impact=round(min(score, 1.0), 2),
                    explanation=explanation,
                ))
            elif score < -0.05:
                challenging.append(Evidence(
                    factor=f"{p['name']} placement",
                    source=source,
                    impact=round(max(score, -1.0), 2),
                    explanation=explanation,
                ))
            relevant_idx += 1

    # Yoga factors
    yogas = detect_yogas(chart, engine)
    for yname, formation, data in yogas:
        keywords = data.get("keywords", [])
        kw_str = ", ".join(keywords[:3]) if keywords else yname
        if yoga_adjustment > 0:
            supporting.append(Evidence(
                factor=yname,
                source=f"yoga:{yname}",
                impact=round(min(yoga_adjustment / max(len(yogas), 1), 1.0), 2),
                explanation=f"{yname}: {formation}. Themes: {kw_str}",
            ))
        else:
            challenging.append(Evidence(
                factor=yname,
                source=f"yoga:{yname}",
                impact=round(max(yoga_adjustment / max(len(yogas), 1), -1.0), 2),
                explanation=f"{yname}: {formation}. Themes: {kw_str}",
            ))

    # Dosha factors
    doshas = detect_doshas(chart, engine)
    for dname, formation, data in doshas:
        keywords = data.get("keywords", [])
        kw_str = ", ".join(keywords[:3]) if keywords else dname
        challenging.append(Evidence(
            factor=dname,
            source=f"dosha:{dname}",
            impact=round(max(dosha_adjustment / max(len(doshas), 1), -1.0), 2),
            explanation=f"{dname}: {formation}. Themes: {kw_str}",
        ))

    # Dasha factor
    if dasha_adjustment != 0:
        source_list = supporting if dasha_adjustment > 0 else challenging
        source_list.append(Evidence(
            factor="Current Dasha",
            source="dasha:current",
            impact=round(dasha_adjustment, 2),
            explanation=f"Current dasha period influence on {domain}",
        ))

    return supporting, challenging


def _build_reasoning_steps(
    domain: str,
    chart: dict,
    engine: KnowledgeEngine,
    base_score: float,
    yoga_adj: float,
    dosha_adj: float,
    dasha_adj: float,
    final_score: float,
    rules: dict[str, Any],
) -> list[ReasoningStep]:
    """Build deterministic reasoning trail."""
    steps: list[ReasoningStep] = []
    step = 1
    domain_rules = rules["domains"][domain]

    steps.append(ReasoningStep(
        step=step,
        description=f"Identify {domain}-relevant houses and planets",
        detail=f"Primary planets: {domain_rules['primaryPlanets']}, Secondary: {domain_rules['secondaryPlanets']}",
    ))
    step += 1

    steps.append(ReasoningStep(
        step=step,
        description="Evaluate planetary dignities and placements",
        detail=f"Base score from relevant planets: {base_score:.2f}/10",
    ))
    step += 1

    if yoga_adj != 0:
        steps.append(ReasoningStep(
            step=step,
            description="Apply yoga adjustments",
            detail=f"Yoga influence: {'+'if yoga_adj > 0 else ''}{yoga_adj:.3f}",
        ))
        step += 1

    if dosha_adj != 0:
        steps.append(ReasoningStep(
            step=step,
            description="Apply dosha adjustments",
            detail=f"Dosha influence: {'+'if dosha_adj > 0 else ''}{dosha_adj:.3f}",
        ))
        step += 1

    if dasha_adj != 0:
        steps.append(ReasoningStep(
            step=step,
            description="Apply current dasha influence",
            detail=f"Dasha influence: {'+'if dasha_adj > 0 else ''}{dasha_adj:.3f}",
        ))
        step += 1

    steps.append(ReasoningStep(
        step=step,
        description="Compute final score",
        detail=f"Final: {base_score:.2f} + {yoga_adj:.3f} + {dosha_adj:.3f} + {dasha_adj:.3f} = {final_score:.2f}",
    ))

    return steps


def evaluate_domain(
    chart: dict,
    domain: LifeDomain,
    engine: KnowledgeEngine,
) -> DomainResult:
    """Evaluate a single life domain deterministically from chart data."""
    domain_str = domain.value
    rules = _load_domain_rules()

    # Step 1: Base planet scoring
    base_score, planet_results = compute_domain_score(chart, domain_str, engine, rules)

    # Step 2: Yoga/Dosha adjustments
    yoga_adj, yoga_descs, dosha_descs = get_yoga_dosha_adjustments(chart, domain_str, engine)

    # Step 3: Dasha adjustment
    dasha_adj, dasha_explanation = get_dasha_adjustment(chart, domain_str, engine)

    # Step 4: Combine
    raw_final = base_score + yoga_adj + dasha_adj
    final_score = max(0.0, min(10.0, round(raw_final, 2)))

    # Step 5: Confidence calculation
    planets = chart.get("planets", [])
    houses = chart.get("houses", [])
    completeness = min(1.0, len(planets) / 9) * min(1.0, len(houses) / 12)
    factor_count = len(planet_results) + len(yoga_descs) + len(dosha_descs)
    if factor_count == 0:
        confidence = 0.2
    elif factor_count <= 3:
        confidence = 0.5
    elif factor_count <= 6:
        confidence = 0.7
    else:
        confidence = 0.85
    confidence = round(min(1.0, confidence), 2)

    # Step 6: Build evidence lists
    supporting, challenging = _build_supporting_challenging_factors(
        chart, domain_str, engine, planet_results, yoga_adj, dasha_adj, dasha_adj, rules,
    )

    # Step 7: Planetary evidence
    planetary_evidence = _build_planetary_evidence(chart, domain_str, rules)

    # Step 8: Reasoning steps
    reasoning = _build_reasoning_steps(
        domain_str, chart, engine, base_score, yoga_adj, dasha_adj, dasha_adj, final_score, rules,
    )

    # Step 9: Summary
    domain_name = rules["domains"].get(domain_str, {}).get("name", domain_str.title())
    summary_parts = [f"{domain_name}: Score {final_score}/10 (Confidence: {confidence:.0%})"]
    if supporting:
        top_support = sorted(supporting, key=lambda e: e.impact, reverse=True)[:3]
        summary_parts.append("Key supports: " + ", ".join(f"{e.factor}" for e in top_support))
    if challenging:
        top_challenge = sorted(challenging, key=lambda e: e.impact)[:3]
        summary_parts.append("Key challenges: " + ", ".join(f"{e.factor}" for e in top_challenge))

    current_dasha = chart.get("vimshottariDasha", {}).get("currentDasha", "")
    if current_dasha:
        summary_parts.append(f"Current Dasha: {current_dasha}")

    return DomainResult(
        domain=domain_str,
        score=final_score,
        confidence=confidence,
        supportingFactors=supporting,
        challengingFactors=challenging,
        planetaryEvidence=planetary_evidence,
        reasoningSteps=reasoning,
        explanationSummary=". ".join(summary_parts),
    )
