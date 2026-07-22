"""
Test the Knowledge Engine lookup functionality.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from knowledge_engine import lookup, KnowledgeEngine


def test_planet_lookup():
    """Test planet knowledge lookup."""
    print("=== Test 1: Planet Lookup ===")
    result = lookup({"planet": "Sun"})
    
    assert "planet" in result
    assert result["planet"]["keywords"] is not None
    assert "strengths" in result["planet"]
    assert "weaknesses" in result["planet"]
    assert "career_themes" in result["planet"]
    assert "finance_themes" in result["planet"]
    assert "relationship_themes" in result["planet"]
    assert "health_themes" in result["planet"]
    assert "spirituality_themes" in result["planet"]
    assert "traditional_remedies" in result["planet"]
    
    print(f"✓ Planet lookup successful: {result['planet']['keywords'][:3]}")
    return result


def test_house_lookup():
    """Test house knowledge lookup."""
    print("\n=== Test 2: House Lookup ===")
    result = lookup({"house": 1})
    
    assert "house" in result
    assert result["house"]["keywords"] is not None
    assert "strengths" in result["house"]
    assert "weaknesses" in result["house"]
    assert "career_themes" in result["house"]
    assert "finance_themes" in result["house"]
    
    print(f"✓ House lookup successful: {result['house']['keywords'][:3]}")
    return result


def test_sign_lookup():
    """Test zodiac sign knowledge lookup."""
    print("\n=== Test 3: Sign Lookup ===")
    result = lookup({"sign": "Aries"})
    
    assert "sign" in result
    assert result["sign"]["keywords"] is not None
    assert "strengths" in result["sign"]
    assert "weaknesses" in result["sign"]
    assert "career_themes" in result["sign"]
    assert "element" in result["sign"]
    assert "ruler" in result["sign"]
    
    print(f"✓ Sign lookup successful: {result['sign']['keywords'][:3]}")
    return result


def test_nakshatra_lookup():
    """Test nakshatra knowledge lookup."""
    print("\n=== Test 4: Nakshatra Lookup ===")
    result = lookup({"nakshatra": "Ashwini"})
    
    assert "nakshatra" in result
    assert result["nakshatra"]["keywords"] is not None
    assert "strengths" in result["nakshatra"]
    assert "weaknesses" in result["nakshatra"]
    assert "ruler" in result["nakshatra"]
    assert "deity" in result["nakshatra"]
    
    print(f"✓ Nakshatra lookup successful: {result['nakshatra']['keywords'][:3]}")
    return result


def test_dasha_lookup():
    """Test Vimshottari dasha knowledge lookup."""
    print("\n=== Test 5: Dasha Lookup ===")
    result = lookup({"dasha": "Jupiter"})
    
    assert "dasha" in result
    assert result["dasha"]["keywords"] is not None
    assert "strengths" in result["dasha"]
    assert "weaknesses" in result["dasha"]
    assert "period_years" in result["dasha"]
    assert "career_themes" in result["dasha"]
    
    print(f"✓ Dasha lookup successful: {result['dasha']['keywords'][:3]}")
    return result


def test_yoga_lookup():
    """Test yoga knowledge lookup."""
    print("\n=== Test 6: Yoga Lookup ===")
    result = lookup({"yoga": "Raj Yoga"})
    
    assert "yoga" in result
    assert result["yoga"]["keywords"] is not None
    assert "strengths" in result["yoga"]
    assert "weaknesses" in result["yoga"]
    assert "formation" in result["yoga"]
    assert "description" in result["yoga"]
    
    print(f"✓ Yoga lookup successful: {result['yoga']['keywords'][:3]}")
    return result


def test_dosha_lookup():
    """Test dosha knowledge lookup."""
    print("\n=== Test 7: Dosha Lookup ===")
    result = lookup({"dosha": "Mangal Dosh"})
    
    assert "dosha" in result
    assert result["dosha"]["keywords"] is not None
    assert "strengths" in result["dosha"]
    assert "weaknesses" in result["dosha"]
    assert "formation" in result["dosha"]
    assert "traditional_remedies" in result["dosha"]
    
    print(f"✓ Dosha lookup successful: {result['dosha']['keywords'][:3]}")
    return result


def test_combined_lookup():
    """Test combined lookup with multiple parameters."""
    print("\n=== Test 8: Combined Lookup ===")
    result = lookup({
        "planet": "Moon",
        "house": 4,
        "sign": "Cancer",
        "dasha": "Moon"
    })
    
    assert "planet" in result
    assert "house" in result
    assert "sign" in result
    assert "dasha" in result
    
    print(f"✓ Combined lookup successful: Found {len(result)} entities")
    return result


def test_engine_instance():
    """Test KnowledgeEngine class instance."""
    print("\n=== Test 9: Engine Instance ===")
    engine = KnowledgeEngine()
    
    # Test individual methods
    sun = engine.get_planet("Sun")
    assert sun is not None
    assert "keywords" in sun
    
    house1 = engine.get_house(1)
    assert house1 is not None
    assert "keywords" in house1
    
    # Test list methods
    planets = engine.list_planets()
    assert len(planets) == 9
    
    signs = engine.list_signs()
    assert len(signs) == 12
    
    nakshatras = engine.list_nakshatras()
    assert len(nakshatras) == 27
    
    print(f"✓ Engine instance successful: {len(planets)} planets, {len(signs)} signs, {len(nakshatras)} nakshatras")
    return engine


def test_bhava_lookup():
    """Test bhava knowledge lookup."""
    print("\n=== Test 10: Bhava Lookup ===")
    result = lookup({"bhava": 1})
    
    assert "bhava" in result
    assert result["bhava"]["keywords"] is not None
    assert "sanskrit_name" in result["bhava"]
    assert "meaning" in result["bhava"]
    assert "strengths" in result["bhava"]
    
    print(f"✓ Bhava lookup successful: {result['bhava']['sanskrit_name']}")
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Knowledge Engine")
    print("=" * 60)
    
    test_planet_lookup()
    test_house_lookup()
    test_sign_lookup()
    test_nakshatra_lookup()
    test_dasha_lookup()
    test_yoga_lookup()
    test_dosha_lookup()
    test_combined_lookup()
    test_engine_instance()
    test_bhava_lookup()
    
    print("\n" + "=" * 60)
    print("All tests passed successfully!")
    print("=" * 60)
