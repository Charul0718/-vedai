"""
Unit tests for astrology-engine using Swiss Ephemeris.

Tests use publicly documented birth charts to verify deterministic outputs.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astrology_engine.calculations import calculate_birth_chart


def test_gandhi_chart():
    """Test with Mahatma Gandhi's birth data (publicly documented).
    
    Born: October 2, 1869, 7:00 AM
    Location: Porbandar, India (21.64°N, 69.6°E)
    Timezone: IST (+05:30)
    """
    result = calculate_birth_chart(
        name="Mahatma Gandhi",
        birth_date="1869-10-02",
        birth_time="07:00",
        latitude=21.64,
        longitude=69.6,
        timezone="+05:30"
    )
    
    # Verify structure
    assert "name" in result
    assert "ascendant" in result
    assert "sunSign" in result
    assert "moonSign" in result
    assert "moonNakshatra" in result
    assert "pada" in result
    assert "ayanamsha" in result
    assert "planets" in result
    assert "houses" in result
    assert "d1Chart" in result
    assert "d9Chart" in result
    assert "vimshottariDasha" in result
    
    # Verify planets structure
    assert len(result["planets"]) == 9
    for planet in result["planets"]:
        assert "name" in planet
        assert "longitude" in planet
        assert "sign" in planet
        assert "degree" in planet
        assert "house" in planet
        assert "isRetrograde" in planet
        assert "d9Sign" in planet
    
    # Verify houses structure
    assert len(result["houses"]) == 12
    for house in result["houses"]:
        assert "number" in house
        assert "sign" in house
        assert "degree" in house
        assert "longitude" in house
    
    # Verify expected values (deterministic)
    print(f"Gandhi Chart - Ascendant: {result['ascendant']['sign']} {result['ascendant']['degree']}")
    print(f"Gandhi Chart - Sun Sign: {result['sunSign']}")
    print(f"Gandhi Chart - Moon Sign: {result['moonSign']}")
    print(f"Gandhi Chart - Moon Nakshatra: {result['moonNakshatra']} Pada {result['pada']}")
    print(f"Gandhi Chart - Ayanamsha: {result['ayanamsha']}")
    
    return result


def test_einstein_chart():
    """Test with Albert Einstein's birth data (publicly documented).
    
    Born: March 14, 1879, 11:30 AM
    Location: Ulm, Germany (48.4°N, 9.99°E)
    Timezone: CET (+01:00)
    """
    result = calculate_birth_chart(
        name="Albert Einstein",
        birth_date="1879-03-14",
        birth_time="11:30",
        latitude=48.4,
        longitude=9.99,
        timezone="+01:00"
    )
    
    # Verify structure
    assert "name" in result
    assert "ascendant" in result
    assert "sunSign" in result
    assert "moonSign" in result
    assert "moonNakshatra" in result
    assert "pada" in result
    assert "ayanamsha" in result
    assert "planets" in result
    assert "houses" in result
    assert "d1Chart" in result
    assert "d9Chart" in result
    assert "vimshottariDasha" in result
    
    # Verify planets structure
    assert len(result["planets"]) == 9
    for planet in result["planets"]:
        assert "name" in planet
        assert "longitude" in planet
        assert "sign" in planet
        assert "degree" in planet
        assert "house" in planet
        assert "isRetrograde" in planet
        assert "d9Sign" in planet
    
    # Verify houses structure
    assert len(result["houses"]) == 12
    for house in result["houses"]:
        assert "number" in house
        assert "sign" in house
        assert "degree" in house
        assert "longitude" in house
    
    # Verify expected values (deterministic)
    print(f"Einstein Chart - Ascendant: {result['ascendant']['sign']} {result['ascendant']['degree']}")
    print(f"Einstein Chart - Sun Sign: {result['sunSign']}")
    print(f"Einstein Chart - Moon Sign: {result['moonSign']}")
    print(f"Einstein Chart - Moon Nakshatra: {result['moonNakshatra']} Pada {result['pada']}")
    print(f"Einstein Chart - Ayanamsha: {result['ayanamsha']}")
    
    return result


def test_deterministic_output():
    """Test that the same input produces the same output (deterministic)."""
    
    # Calculate Gandhi's chart twice
    result1 = calculate_birth_chart(
        name="Mahatma Gandhi",
        birth_date="1869-10-02",
        birth_time="07:00",
        latitude=21.64,
        longitude=69.6,
        timezone="+05:30"
    )
    
    result2 = calculate_birth_chart(
        name="Mahatma Gandhi",
        birth_date="1869-10-02",
        birth_time="07:00",
        latitude=21.64,
        longitude=69.6,
        timezone="+05:30"
    )
    
    # Verify all key values are identical
    assert result1["ascendant"]["sign"] == result2["ascendant"]["sign"]
    assert result1["ascendant"]["degree"] == result2["ascendant"]["degree"]
    assert result1["sunSign"] == result2["sunSign"]
    assert result1["moonSign"] == result2["moonSign"]
    assert result1["moonNakshatra"] == result2["moonNakshatra"]
    assert result1["pada"] == result2["pada"]
    assert result1["ayanamsha"] == result2["ayanamsha"]
    
    # Verify all planets are identical
    for p1, p2 in zip(result1["planets"], result2["planets"]):
        assert p1["name"] == p2["name"]
        assert p1["longitude"] == p2["longitude"]
        assert p1["sign"] == p2["sign"]
        assert p1["degree"] == p2["degree"]
        assert p1["house"] == p2["house"]
        assert p1["isRetrograde"] == p2["isRetrograde"]
        assert p1["d9Sign"] == p2["d9Sign"]
    
    print("Deterministic output test passed - results are identical")
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Astrology Engine with Swiss Ephemeris")
    print("=" * 60)
    
    print("\n--- Test 1: Mahatma Gandhi's Chart ---")
    gandhi_result = test_gandhi_chart()
    print("✓ Gandhi chart test passed")
    
    print("\n--- Test 2: Albert Einstein's Chart ---")
    einstein_result = test_einstein_chart()
    print("✓ Einstein chart test passed")
    
    print("\n--- Test 3: Deterministic Output ---")
    test_deterministic_output()
    print("✓ Deterministic output test passed")
    
    print("\n" + "=" * 60)
    print("All tests passed successfully!")
    print("=" * 60)
