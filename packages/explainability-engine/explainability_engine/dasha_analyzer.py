from __future__ import annotations

from knowledge_engine import KnowledgeEngine

_DASHA_DOMAIN_RELEVANCE: dict[str, dict[str, float]] = {
    "Ketu": {"career": 0.2, "finance": 0.1, "marriage": 0.1, "relationships": 0.1, "children": 0.1, "health": 0.3, "education": 0.2, "business": 0.1, "spirituality": 0.8},
    "Venus": {"career": 0.5, "finance": 0.6, "marriage": 0.9, "relationships": 0.9, "children": 0.3, "health": 0.3, "education": 0.3, "business": 0.6, "spirituality": 0.4},
    "Sun": {"career": 0.8, "finance": 0.5, "marriage": 0.3, "relationships": 0.2, "children": 0.3, "health": 0.6, "education": 0.4, "business": 0.5, "spirituality": 0.6},
    "Moon": {"career": 0.4, "finance": 0.5, "marriage": 0.7, "relationships": 0.7, "children": 0.6, "health": 0.5, "education": 0.5, "business": 0.4, "spirituality": 0.5},
    "Mars": {"career": 0.7, "finance": 0.4, "marriage": -0.3, "relationships": -0.2, "children": -0.1, "health": 0.5, "education": 0.3, "business": 0.5, "spirituality": 0.2},
    "Rahu": {"career": 0.4, "finance": 0.3, "marriage": -0.2, "relationships": -0.1, "children": -0.1, "health": -0.3, "education": 0.2, "business": 0.4, "spirituality": -0.1},
    "Jupiter": {"career": 0.7, "finance": 0.8, "marriage": 0.7, "relationships": 0.6, "children": 0.8, "health": 0.5, "education": 0.9, "business": 0.6, "spirituality": 0.9},
    "Saturn": {"career": 0.5, "finance": 0.4, "marriage": -0.2, "relationships": -0.1, "children": -0.2, "health": -0.3, "education": 0.3, "business": 0.4, "spirituality": 0.6},
    "Mercury": {"career": 0.6, "finance": 0.7, "marriage": 0.4, "relationships": 0.5, "children": 0.4, "health": 0.3, "education": 0.8, "business": 0.7, "spirituality": 0.3},
}


def get_dasha_adjustment(
    chart: dict,
    domain: str,
    engine: KnowledgeEngine,
) -> tuple[float, str]:
    """Get current dasha's impact on a domain.

    Returns: (adjustment, explanation)
    """
    dasha_data = chart.get("vimshottariDasha", {})
    current_dasha = dasha_data.get("currentDasha", "")

    if not current_dasha:
        return 0.0, "Current dasha not available"

    relevance = _DASHA_DOMAIN_RELEVANCE.get(current_dasha, {}).get(domain, 0.5)
    dasha_knowledge = engine.get_dasha(current_dasha) or {}

    # Get the domain-specific themes from dasha knowledge
    domain_key = f"{domain}_themes"
    themes = dasha_knowledge.get(domain_key, [])

    # Compute adjustment based on dasha lord's natural affinity
    # Scale: relevance ranges from -0.3 to 0.9, we map it to -0.5 to +0.5
    adjustment = (relevance - 0.3) * 0.625  # maps 0.3->0, 0.9->0.375
    adjustment = max(-0.5, min(0.5, adjustment))

    themes_str = ", ".join(themes[:3]) if themes else "general themes"
    explanation = f"Current dasha: {current_dasha} ({dasha_knowledge.get('period_years', '?')} years). Domain relevance: {domain_key}. Key themes: {themes_str}"

    return round(adjustment, 3), explanation
