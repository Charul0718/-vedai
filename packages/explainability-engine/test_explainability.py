"""
Unit tests for the Explainability Engine.

Tests verify deterministic scoring, evidence generation, and reasoning
for all 9 life domains without any LLM involvement.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "knowledge-engine"))

from knowledge_engine import KnowledgeEngine
from explainability_engine import ExplainabilityEngine, DomainResult, LifeDomain
from explainability_engine.types import Evidence, ReasoningStep, PlanetaryEvidence
from explainability_engine.planet_scorer import (
    score_planet_for_domain, compute_domain_score, get_planet_dignity, _load_domain_rules,
)
from explainability_engine.yoga_dosha_analyzer import (
    detect_yogas, detect_doshas, get_yoga_dosha_adjustments,
    _mutual_aspect_or_conjunction,
)
from explainability_engine.dasha_analyzer import get_dasha_adjustment


# --- Test fixtures ---

def _make_chart():
    """Create a realistic test chart dict matching astrology-engine output format."""
    return {
        "name": "Test Person",
        "ascendant": {"sign": "Leo", "degree": 15.0, "longitude": 135.0},
        "sunSign": "Leo",
        "moonSign": "Cancer",
        "moonNakshatra": "Ashlesha",
        "pada": 2,
        "ayanamsha": 24.15,
        "planets": [
            {"name": "Sun", "longitude": 135.0, "sign": "Leo", "degree": 15.0, "house": 1, "isRetrograde": False, "d9Sign": "Leo"},
            {"name": "Moon", "longitude": 105.0, "sign": "Cancer", "degree": 15.0, "house": 12, "isRetrograde": False, "d9Sign": "Cancer"},
            {"name": "Mars", "longitude": 30.0, "sign": "Aries", "degree": 0.0, "house": 9, "isRetrograde": False, "d9Sign": "Aries"},
            {"name": "Mercury", "longitude": 165.0, "sign": "Virgo", "degree": 15.0, "house": 2, "isRetrograde": False, "d9Sign": "Virgo"},
            {"name": "Jupiter", "longitude": 225.0, "sign": "Sagittarius", "degree": 15.0, "house": 5, "isRetrograde": False, "d9Sign": "Sagittarius"},
            {"name": "Venus", "longitude": 195.0, "sign": "Libra", "degree": 15.0, "house": 3, "isRetrograde": False, "d9Sign": "Libra"},
            {"name": "Saturn", "longitude": 285.0, "sign": "Capricorn", "degree": 15.0, "house": 6, "isRetrograde": False, "d9Sign": "Capricorn"},
            {"name": "Rahu", "longitude": 75.0, "sign": "Gemini", "degree": 15.0, "house": 11, "isRetrograde": True, "d9Sign": "Gemini"},
            {"name": "Ketu", "longitude": 255.0, "sign": "Sagittarius", "degree": 15.0, "house": 5, "isRetrograde": True, "d9Sign": "Sagittarius"},
        ],
        "houses": [
            {"number": 1, "sign": "Leo", "degree": 135.0, "longitude": 135.0},
            {"number": 2, "sign": "Virgo", "degree": 165.0, "longitude": 165.0},
            {"number": 3, "sign": "Libra", "degree": 195.0, "longitude": 195.0},
            {"number": 4, "sign": "Scorpio", "degree": 225.0, "longitude": 225.0},
            {"number": 5, "sign": "Sagittarius", "degree": 255.0, "longitude": 255.0},
            {"number": 6, "sign": "Capricorn", "degree": 285.0, "longitude": 285.0},
            {"number": 7, "sign": "Aquarius", "degree": 315.0, "longitude": 315.0},
            {"number": 8, "sign": "Pisces", "degree": 345.0, "longitude": 345.0},
            {"number": 9, "sign": "Aries", "degree": 15.0, "longitude": 15.0},
            {"number": 10, "sign": "Taurus", "degree": 45.0, "longitude": 45.0},
            {"number": 11, "sign": "Gemini", "degree": 75.0, "longitude": 75.0},
            {"number": 12, "sign": "Cancer", "degree": 105.0, "longitude": 105.0},
        ],
        "d1Chart": {"ascendant": {"sign": "Leo"}, "planets": {}},
        "d9Chart": {"ascendant": "Leo", "planets": {}},
        "vimshottariDasha": {
            "currentDasha": "Jupiter",
            "dashaSequence": [],
            "dashaPeriods": {},
        },
    }


def _make_mangal_dosh_chart():
    chart = _make_chart()
    for p in chart["planets"]:
        if p["name"] == "Mars":
            p["house"] = 7
            p["sign"] = "Libra"
    return chart


def _make_kaal_sarp_chart():
    chart = _make_chart()
    for p in chart["planets"]:
        if p["name"] == "Rahu":
            p["house"] = 3
            p["sign"] = "Gemini"
        elif p["name"] == "Ketu":
            p["house"] = 9
            p["sign"] = "Sagittarius"
        elif p["name"] == "Sun":
            p["house"] = 4
            p["sign"] = "Cancer"
        elif p["name"] == "Moon":
            p["house"] = 5
            p["sign"] = "Leo"
        elif p["name"] == "Mars":
            p["house"] = 6
            p["sign"] = "Virgo"
        elif p["name"] == "Mercury":
            p["house"] = 7
            p["sign"] = "Libra"
        elif p["name"] == "Jupiter":
            p["house"] = 8
            p["sign"] = "Scorpio"
        elif p["name"] == "Venus":
            p["house"] = 4
            p["sign"] = "Cancer"
        elif p["name"] == "Saturn":
            p["house"] = 6
            p["sign"] = "Virgo"
    return chart


def _make_budhaditya_chart():
    chart = _make_chart()
    for p in chart["planets"]:
        if p["name"] == "Sun":
            p["sign"] = "Leo"
            p["house"] = 1
        elif p["name"] == "Mercury":
            p["sign"] = "Leo"
            p["house"] = 1
    return chart


# --- Planet dignity tests ---

def test_planet_dignity_exalted():
    assert get_planet_dignity("Sun", "Aries") == "exalted"
    assert get_planet_dignity("Jupiter", "Cancer") == "exalted"
    assert get_planet_dignity("Saturn", "Libra") == "exalted"
    assert get_planet_dignity("Mars", "Capricorn") == "exalted"
    print("✓ Planet dignity: exalted detection correct")


def test_planet_dignity_own_sign():
    assert get_planet_dignity("Sun", "Leo") == "own_sign"
    assert get_planet_dignity("Mars", "Aries") == "own_sign"
    assert get_planet_dignity("Mars", "Scorpio") == "own_sign"
    assert get_planet_dignity("Jupiter", "Sagittarius") == "own_sign"
    assert get_planet_dignity("Jupiter", "Pisces") == "own_sign"
    print("✓ Planet dignity: own_sign detection correct")


def test_planet_dignity_debilitated():
    assert get_planet_dignity("Sun", "Libra") == "debilitated"
    assert get_planet_dignity("Jupiter", "Capricorn") == "debilitated"
    assert get_planet_dignity("Venus", "Virgo") == "debilitated"
    print("✓ Planet dignity: debilitated detection correct")


def test_planet_dignity_friendly():
    assert get_planet_dignity("Sun", "Cancer") == "friendly"  # Moon rules Cancer, Moon is friend of Sun
    assert get_planet_dignity("Jupiter", "Aries") == "friendly"  # Mars rules Aries, Mars is friend of Jupiter
    print("✓ Planet dignity: friendly detection correct")


def test_planet_dignity_neutral():
    dignity = get_planet_dignity("Sun", "Aquarius")
    assert dignity in ("neutral", "enemy")
    print(f"✓ Planet dignity: Sun in Aquarius = {dignity}")


# --- Planet scorer tests ---

def test_score_planet_for_domain():
    engine = KnowledgeEngine()
    score, explanation = score_planet_for_domain("Jupiter", 10, "Sagittarius", False, "career", engine)
    assert isinstance(score, float)
    assert isinstance(explanation, str)
    assert "Jupiter" in explanation
    assert "career" in explanation
    print(f"✓ Planet scorer: Jupiter in H10 Sagittarius for career = {score:.4f}")


def test_score_planet_retrograde():
    engine = KnowledgeEngine()
    score_normal, _ = score_planet_for_domain("Jupiter", 10, "Sagittarius", False, "career", engine)
    score_retro, _ = score_planet_for_domain("Jupiter", 10, "Sagittarius", True, "career", engine)
    assert score_retro < score_normal, "Retrograde should reduce score"
    print(f"✓ Retrograde reduces score: normal={score_normal:.4f}, retro={score_retro:.4f}")


def test_compute_domain_score():
    engine = KnowledgeEngine()
    chart = _make_chart()
    score, results = compute_domain_score(chart, "career", engine)
    assert 0.0 <= score <= 10.0
    assert len(results) > 0
    print(f"✓ Domain score (career): {score}/10 with {len(results)} planet results")


def test_all_domains_score_range():
    engine = KnowledgeEngine()
    chart = _make_chart()
    for domain in LifeDomain:
        score, _ = compute_domain_score(chart, domain.value, engine)
        assert 0.0 <= score <= 10.0, f"Domain {domain.value} score {score} out of range"
    print("✓ All 9 domains produce scores in 0-10 range")


# --- Yoga/Dosha tests ---

def test_detect_yogas_budhaditya():
    engine = KnowledgeEngine()
    chart = _make_budhaditya_chart()
    yogas = detect_yogas(chart, engine)
    yoga_names = [y[0] for y in yogas]
    assert "Budhaditya Yoga" in yoga_names, f"Expected Budhaditya Yoga, got {yoga_names}"
    print(f"✓ Detected yogas: {yoga_names}")


def test_detect_doshas_mangal():
    engine = KnowledgeEngine()
    chart = _make_mangal_dosh_chart()
    doshas = detect_doshas(chart, engine)
    dosha_names = [d[0] for d in doshas]
    assert "Mangal Dosh" in dosha_names, f"Expected Mangal Dosh, got {dosha_names}"
    print(f"✓ Detected doshas: {dosha_names}")


def test_detect_doshas_kaal_sarp():
    engine = KnowledgeEngine()
    chart = _make_kaal_sarp_chart()
    doshas = detect_doshas(chart, engine)
    dosha_names = [d[0] for d in doshas]
    assert "Kaal Sarp Dosh" in dosha_names, f"Expected Kaal Sarp Dosh, got {dosha_names}"
    print(f"✓ Kaal Sarp detection: {dosha_names}")


def test_yoga_dosha_adjustments():
    engine = KnowledgeEngine()
    chart = _make_chart()
    adj, yoga_descs, dosha_descs = get_yoga_dosha_adjustments(chart, "career", engine)
    assert isinstance(adj, float)
    assert isinstance(yoga_descs, list)
    assert isinstance(dosha_descs, list)
    print(f"✓ Yoga/Dosha adjustments: adj={adj:.4f}, yogas={len(yoga_descs)}, doshas={len(dosha_descs)}")


def test_mutual_aspect_conjunction():
    p1 = {"name": "Jupiter", "house": 1, "sign": "Aries"}
    p2 = {"name": "Sun", "house": 1, "sign": "Aries"}
    assert _mutual_aspect_or_conjunction(p1, p2), "Same sign should be conjunction"

    p3 = {"name": "Mars", "house": 1, "sign": "Aries"}
    p4 = {"name": "Saturn", "house": 7, "sign": "Libra"}
    assert _mutual_aspect_or_conjunction(p3, p4), "7th aspect should be mutual"

    p5 = {"name": "Mercury", "house": 1, "sign": "Aries"}
    p6 = {"name": "Venus", "house": 3, "sign": "Gemini"}
    assert not _mutual_aspect_or_conjunction(p5, p6), "Non-aspecting planets"
    print("✓ Mutual aspect/conjunction detection correct")


# --- Dasha tests ---

def test_dasha_adjustment():
    engine = KnowledgeEngine()
    chart = _make_chart()
    adj, explanation = get_dasha_adjustment(chart, "career", engine)
    assert isinstance(adj, float)
    assert -1.0 <= adj <= 1.0
    assert "Jupiter" in explanation
    print(f"✓ Dasha adjustment: {adj:.4f} ({explanation[:60]}...)")


def test_dasha_all_domains():
    engine = KnowledgeEngine()
    chart = _make_chart()
    for domain in LifeDomain:
        adj, explanation = get_dasha_adjustment(chart, domain.value, engine)
        assert isinstance(adj, float)
        assert -1.0 <= adj <= 1.0
    print("✓ Dasha adjustments valid for all 9 domains")


# --- Domain evaluator tests ---

def test_evaluate_single_domain():
    engine = KnowledgeEngine()
    chart = _make_chart()
    from explainability_engine.domain_evaluator import evaluate_domain
    result = evaluate_domain(chart, LifeDomain.CAREER, engine)
    assert isinstance(result, DomainResult)
    assert result.domain == "career"
    assert 0.0 <= result.score <= 10.0
    assert 0.0 <= result.confidence <= 1.0
    assert len(result.supportingFactors) > 0 or len(result.challengingFactors) > 0
    assert len(result.planetaryEvidence) == 9
    assert len(result.reasoningSteps) >= 3
    assert len(result.explanationSummary) > 0
    print(f"✓ Career evaluation: score={result.score}, confidence={result.confidence}, "
          f"supporting={len(result.supportingFactors)}, challenging={len(result.challengingFactors)}")


def test_evaluate_all_domains():
    engine = KnowledgeEngine()
    chart = _make_chart()
    from explainability_engine.domain_evaluator import evaluate_domain
    for domain in LifeDomain:
        result = evaluate_domain(chart, domain, engine)
        assert isinstance(result, DomainResult)
        assert result.domain == domain.value
        assert 0.0 <= result.score <= 10.0
        assert 0.0 <= result.confidence <= 1.0
        assert len(result.planetaryEvidence) == 9
        assert len(result.reasoningSteps) >= 3
    print("✓ All 9 domains evaluate correctly")


def test_reasoning_steps_are_numbered():
    engine = KnowledgeEngine()
    chart = _make_chart()
    from explainability_engine.domain_evaluator import evaluate_domain
    result = evaluate_domain(chart, LifeDomain.FINANCE, engine)
    for i, step in enumerate(result.reasoningSteps, 1):
        assert step.step == i, f"Step numbering broken: expected {i}, got {step.step}"
        assert len(step.description) > 0
        assert len(step.detail) > 0
    print(f"✓ Reasoning steps numbered sequentially (1-{len(result.reasoningSteps)})")


def test_evidence_has_source():
    engine = KnowledgeEngine()
    chart = _make_chart()
    from explainability_engine.domain_evaluator import evaluate_domain
    result = evaluate_domain(chart, LifeDomain.HEALTH, engine)
    for e in result.supportingFactors + result.challengingFactors:
        assert isinstance(e, Evidence)
        assert len(e.factor) > 0
        assert len(e.source) > 0
        assert -1.0 <= e.impact <= 1.0
        assert len(e.explanation) > 0
    print("✓ Evidence items have valid structure")


def test_planetary_evidence_roles():
    engine = KnowledgeEngine()
    chart = _make_chart()
    from explainability_engine.domain_evaluator import evaluate_domain
    result = evaluate_domain(chart, LifeDomain.CAREER, engine)
    for pe in result.planetaryEvidence:
        assert isinstance(pe, PlanetaryEvidence)
        assert pe.planet in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")
        assert 1 <= pe.house <= 12
        assert pe.sign in ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")
        assert -1.0 <= pe.contribution <= 1.0
    print("✓ Planetary evidence has valid planet/house/sign data")


# --- ExplainabilityEngine orchestrator tests ---

def test_engine_evaluate_all():
    engine = KnowledgeEngine()
    explainer = ExplainabilityEngine(engine)
    chart = _make_chart()
    results = explainer.evaluate_all(chart)
    assert len(results) == 9
    for domain_name, result in results.items():
        assert isinstance(result, DomainResult)
        assert result.domain == domain_name
    print(f"✓ ExplainabilityEngine.evaluate_all: {len(results)} domains")


def test_engine_evaluate_single():
    engine = KnowledgeEngine()
    explainer = ExplainabilityEngine(engine)
    chart = _make_chart()
    result = explainer.evaluate(chart, "career")
    assert isinstance(result, DomainResult)
    assert result.domain == "career"
    print(f"✓ ExplainabilityEngine.evaluate('career'): score={result.score}")


def test_engine_to_dict():
    engine = KnowledgeEngine()
    explainer = ExplainabilityEngine(engine)
    chart = _make_chart()
    result = explainer.evaluate(chart, "finance")
    d = explainer.to_dict(result)
    assert isinstance(d, dict)
    assert d["domain"] == "finance"
    assert "score" in d
    assert "confidence" in d
    assert "supportingFactors" in d
    assert "challengingFactors" in d
    assert "planetaryEvidence" in d
    assert "reasoningSteps" in d
    assert "explanationSummary" in d
    assert isinstance(d["supportingFactors"], list)
    assert isinstance(d["planetaryEvidence"], list)
    print("✓ to_dict produces valid JSON-serializable structure")


def test_engine_evaluate_all_to_dict():
    engine = KnowledgeEngine()
    explainer = ExplainabilityEngine(engine)
    chart = _make_chart()
    results = explainer.evaluate_all_to_dict(chart)
    assert len(results) == 9
    for domain_name, d in results.items():
        assert isinstance(d, dict)
        assert d["domain"] == domain_name
        assert "score" in d
        assert "reasoningSteps" in d
    print(f"✓ evaluate_all_to_dict: {len(results)} domains with full structure")


# --- Determinism tests ---

def test_deterministic_scoring():
    engine = KnowledgeEngine()
    chart = _make_chart()
    score1, _ = compute_domain_score(chart, "career", engine)
    score2, _ = compute_domain_score(chart, "career", engine)
    assert score1 == score2, f"Non-deterministic: {score1} != {score2}"
    print(f"✓ Deterministic: same input → same score ({score1})")


def test_deterministic_full_evaluation():
    engine = KnowledgeEngine()
    explainer = ExplainabilityEngine(engine)
    chart = _make_chart()
    r1 = explainer.evaluate(chart, "marriage")
    r2 = explainer.evaluate(chart, "marriage")
    assert r1.score == r2.score
    assert r1.confidence == r2.confidence
    assert len(r1.supportingFactors) == len(r2.supportingFactors)
    assert len(r1.reasoningSteps) == len(r2.reasoningSteps)
    print("✓ Full evaluation is deterministic")


# --- Edge cases ---

def test_empty_planets():
    engine = KnowledgeEngine()
    chart = _make_chart()
    chart["planets"] = []
    score, results = compute_domain_score(chart, "career", engine)
    rules = _load_domain_rules()
    assert score == rules["baseScore"]  # neutral default
    assert results == []
    print("✓ Empty planets → neutral base score")


def test_all_retrograde():
    engine = KnowledgeEngine()
    chart = _make_chart()
    for p in chart["planets"]:
        p["isRetrograde"] = True
    score, _ = compute_domain_score(chart, "career", engine)
    assert 0.0 <= score <= 10.0
    print(f"✓ All retrograde planets: score={score}")


def test_no_dasha():
    engine = KnowledgeEngine()
    chart = _make_chart()
    chart["vimshottariDasha"] = {}
    adj, explanation = get_dasha_adjustment(chart, "career", engine)
    assert adj == 0.0
    assert "not available" in explanation
    print("✓ No dasha data → neutral adjustment")


def test_domain_rules_loaded():
    rules = _load_domain_rules()
    assert "domains" in rules
    assert len(rules["domains"]) == 9
    assert "career" in rules["domains"]
    assert "finance" in rules["domains"]
    assert "dignityScores" in rules
    assert "baseScore" in rules
    print(f"✓ Domain rules loaded: {len(rules['domains'])} domains, base score = {rules['baseScore']}")


# --- Run all tests ---

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Explainability Engine")
    print("=" * 60)

    tests = [
        test_planet_dignity_exalted,
        test_planet_dignity_own_sign,
        test_planet_dignity_debilitated,
        test_planet_dignity_friendly,
        test_planet_dignity_neutral,
        test_score_planet_for_domain,
        test_score_planet_retrograde,
        test_compute_domain_score,
        test_all_domains_score_range,
        test_detect_yogas_budhaditya,
        test_detect_doshas_mangal,
        test_detect_doshas_kaal_sarp,
        test_yoga_dosha_adjustments,
        test_mutual_aspect_conjunction,
        test_dasha_adjustment,
        test_dasha_all_domains,
        test_evaluate_single_domain,
        test_evaluate_all_domains,
        test_reasoning_steps_are_numbered,
        test_evidence_has_source,
        test_planetary_evidence_roles,
        test_engine_evaluate_all,
        test_engine_evaluate_single,
        test_engine_to_dict,
        test_engine_evaluate_all_to_dict,
        test_deterministic_scoring,
        test_deterministic_full_evaluation,
        test_empty_planets,
        test_all_retrograde,
        test_no_dasha,
        test_domain_rules_loaded,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            print(f"\n--- {test.__name__} ---")
            test()
            passed += 1
        except Exception as e:
            print(f"✗ FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {len(tests)} total")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)
