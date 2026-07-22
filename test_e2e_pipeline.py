"""
End-to-end pipeline test: birth input → chart → knowledge → explainability → output.

Tests the full flow from raw birth data through all engine layers,
verifying deterministic output at every stage.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "packages", "astrology-engine"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "packages", "knowledge-engine"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from astrology_engine.calculations import calculate_birth_chart
from knowledge_engine import KnowledgeEngine
from explainability_engine import ExplainabilityEngine


def _birth_input():
    return {
        "name": "Arjun",
        "birth_date": "1995-10-25",
        "birth_time": "08:30",
        "latitude": 19.076,
        "longitude": 72.877,
        "timezone": "+05:30",
    }


def test_full_pipeline():
    print("=" * 60)
    print("E2E Pipeline Test: Birth → Chart → Knowledge → Explainability")
    print("=" * 60)

    # Stage 1: Birth input → Chart calculation
    print("\n[Stage 1] Calculating birth chart...")
    inp = _birth_input()
    chart = calculate_birth_chart(
        name=inp["name"],
        birth_date=inp["birth_date"],
        birth_time=inp["birth_time"],
        latitude=inp["latitude"],
        longitude=inp["longitude"],
        timezone=inp["timezone"],
    )
    assert chart is not None, "Chart calculation returned None"
    assert "planets" in chart, "Chart missing planets"
    assert len(chart["planets"]) == 9, f"Expected 9 planets, got {len(chart['planets'])}"
    assert "houses" in chart, "Chart missing houses"
    assert len(chart["houses"]) == 12, f"Expected 12 houses, got {len(chart['houses'])}"
    assert "ascendant" in chart, "Chart missing ascendant"
    print(f"  ✓ Chart calculated: {chart['ascendant']['sign']} ascendant, {len(chart['planets'])} planets, {len(chart['houses'])} houses")
    print(f"  ✓ Moon sign: {chart['moonSign']}, Nakshatra: {chart['moonNakshatra']}")

    # Stage 2: Chart → Knowledge lookups
    print("\n[Stage 2] Knowledge engine lookups...")
    ke = KnowledgeEngine()
    for p in chart["planets"]:
        planet_data = ke.get_planet(p["name"])
        assert planet_data is not None, f"No knowledge for planet {p['name']}"
        assert "career_themes" in planet_data, f"Planet {p['name']} missing career_themes"

        sign_data = ke.get_sign(p["sign"])
        assert sign_data is not None, f"No knowledge for sign {p['sign']}"
        assert "element" in sign_data, f"Sign {p['sign']} missing element"

    asc_sign = chart["ascendant"]["sign"]
    asc_data = ke.get_sign(asc_sign)
    assert asc_data is not None, f"No knowledge for ascendant sign {asc_sign}"
    print(f"  ✓ All 9 planets have knowledge entries")
    print(f"  ✓ All signs have element/modality data")
    print(f"  ✓ Ascendant {asc_sign}: element={asc_data['element']}, modality={asc_data['modality']}")

    # Stage 3: Chart + Knowledge → Explainability
    print("\n[Stage 3] Running explainability engine...")
    explainer = ExplainabilityEngine(ke)
    results = explainer.evaluate_all(chart)
    assert len(results) == 9, f"Expected 9 domain results, got {len(results)}"

    for domain_name, result in results.items():
        assert 0.0 <= result.score <= 10.0, f"{domain_name} score {result.score} out of range"
        assert 0.0 <= result.confidence <= 1.0, f"{domain_name} confidence {result.confidence} out of range"
        assert len(result.planetaryEvidence) > 0, f"{domain_name} has no planetary evidence"
        assert len(result.reasoningSteps) >= 3, f"{domain_name} has < 3 reasoning steps"
        assert len(result.explanationSummary) > 0, f"{domain_name} has no summary"

    print(f"  ✓ All 9 domains scored successfully")
    for domain_name, result in results.items():
        print(f"    {domain_name:15s}: {result.score:5.1f}/10 (confidence: {result.confidence:.0%})")

    # Stage 4: Serialization
    print("\n[Stage 4] Serialization to JSON-compatible dict...")
    all_dict = explainer.evaluate_all_to_dict(chart)
    assert len(all_dict) == 9
    for domain_name, d in all_dict.items():
        assert isinstance(d, dict)
        assert "score" in d
        assert "supportingFactors" in d
        assert "planetaryEvidence" in d
        assert "reasoningSteps" in d
        assert "explanationSummary" in d
        # Verify JSON serializable
        import json
        json.dumps(d)  # will throw if not serializable

    print(f"  ✓ All 9 domains serialize to valid JSON")

    # Stage 5: Determinism check
    print("\n[Stage 5] Determinism verification...")
    results2 = explainer.evaluate_all(chart)
    for domain_name in results:
        r1 = results[domain_name]
        r2 = results2[domain_name]
        assert r1.score == r2.score, f"{domain_name} non-deterministic: {r1.score} != {r2.score}"
        assert r1.confidence == r2.confidence
        assert len(r1.supportingFactors) == len(r2.supportingFactors)
        assert len(r1.reasoningSteps) == len(r2.reasoningSteps)
    print(f"  ✓ Same input produces identical output (deterministic)")

    print("\n" + "=" * 60)
    print("ALL E2E PIPELINE TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_full_pipeline()
