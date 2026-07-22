import math
import swisseph as swe
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

RASIS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Swiss Ephemeris planet IDs
PLANET_IDS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,  # Mean North Node
    "Ketu": swe.MEAN_NODE,  # Will calculate as opposite to Rahu
}

PLANET_NAMES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

def get_julian_date(dt: datetime) -> float:
    """Calculate Julian Date for a given datetime using Swiss Ephemeris."""
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0 + dt.second / 3600.0)

def calculate_ayanamsha(jd: float) -> float:
    """Calculate Lahiri Ayanamsha using Swiss Ephemeris."""
    # Set sidereal mode to Lahiri
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayanamsha = swe.get_ayanamsa(jd)
    return ayanamsha

def get_planet_longitude(planet: str, jd: float) -> tuple[float, bool]:
    """Calculate tropical longitude of planet using Swiss Ephemeris.
    Returns (longitude, is_retrograde).
    """
    if planet == "Ketu":
        # Ketu is opposite to Rahu
        rahu_long, rahu_retro = get_planet_longitude("Rahu", jd)
        return (rahu_long + 180.0) % 360.0, rahu_retro
    
    planet_id = PLANET_IDS.get(planet)
    if planet_id is None:
        return 0.0, False
    
    # Calculate position
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    try:
        result = swe.calc_ut(jd, planet_id, flags)
        
        if result is None or len(result) < 4:
            return 0.0, False
        
        longitude = result[0] % 360.0
        speed = result[3]  # Speed in degrees/day
        
        # Retrograde if speed is negative
        is_retrograde = speed < 0
        
        return longitude, is_retrograde
    except Exception:
        return 0.0, False

def calculate_ascendant(jd: float, latitude: float, longitude: float) -> float:
    """Calculate tropical ascendant using Swiss Ephemeris."""
    geopos = (longitude, latitude, 0.0)
    hsys = b'P'  # Placidus house system
    ascmc, _ = swe.houses(jd, latitude, longitude, hsys)
    return ascmc[0] % 360.0  # Ascendant

def calculate_houses(jd: float, latitude: float, longitude: float, ayanamsha: float) -> List[Dict[str, Any]]:
    """Calculate house cusps using Swiss Ephemeris (Placidus system)."""
    geopos = (longitude, latitude, 0.0)
    hsys = b'P'  # Placidus house system
    cusps, ascmc = swe.houses(jd, latitude, longitude, hsys)
    
    houses = []
    for i in range(12):
        tropical_cusp = cusps[i] % 360.0
        sidereal_cusp = (tropical_cusp - ayanamsha) % 360.0
        
        sign_idx = int(sidereal_cusp // 30)
        sign = RASIS[sign_idx]
        degree = sidereal_cusp % 30
        
        houses.append({
            "number": i + 1,
            "sign": sign,
            "degree": degree,
            "longitude": sidereal_cusp
        })
    
    return houses

def get_nakshatra(longitude: float) -> tuple[str, int]:
    """Calculate Nakshatra and Pada from sidereal longitude."""
    # Each Nakshatra spans 13°20' (13.333... degrees)
    nakshatra_idx = int(longitude / 13.3333333333) % 27
    pada = int((longitude % 13.3333333333) / 3.3333333333) + 1
    return NAKSHATRAS[nakshatra_idx], pada

def calculate_d9_chart(sidereal_longitude: float) -> str:
    """Calculate Navamsa (D9) sign from sidereal longitude."""
    # Each sign is divided into 9 parts (3°20' each)
    navamsa_idx = int(sidereal_longitude / 3.3333333333) % 12
    return RASIS[navamsa_idx]

def calculate_vimshottari_dasha(moon_longitude: float) -> Dict[str, Any]:
    """Calculate Vimshottari Dasha sequence based on Moon's Nakshatra."""
    nakshatra_idx = int(moon_longitude / 13.3333333333) % 27
    
    # Dasha lords in order
    dasha_lords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    
    # Starting lord based on Nakshatra
    start_lord_idx = nakshatra_idx % 9
    start_lord = dasha_lords[start_lord_idx]
    
    # Dasha periods in years
    dasha_periods = {
        "Ketu": 7,
        "Venus": 20,
        "Sun": 6,
        "Moon": 10,
        "Mars": 7,
        "Rahu": 18,
        "Jupiter": 16,
        "Saturn": 19,
        "Mercury": 17
    }
    
    return {
        "currentDasha": start_lord,
        "dashaSequence": dasha_lords,
        "dashaPeriods": dasha_periods
    }

def calculate_birth_chart(
    name: str,
    birth_date: str,  # "YYYY-MM-DD"
    birth_time: str,  # "HH:MM"
    latitude: float,
    longitude: float,
    timezone: str  # e.g., "Asia/Kolkata" or offset like "+05:30"
) -> Dict[str, Any]:
    """Calculate complete Vedic birth chart using Swiss Ephemeris.
    
    Returns structured JSON with:
    - ascendant
    - sunSign
    - moonSign
    - moonNakshatra
    - pada
    - ayanamsha
    - planets
    - houses
    - d1Chart (Rasi)
    - d9Chart (Navamsa)
    - vimshottariDasha
    """
    # Parse datetime
    dt_local = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    
    # Handle timezone
    if timezone.startswith(('+', '-')):
        # Parse offset like "+05:30" or "-08:00"
        sign = 1 if timezone[0] == '+' else -1
        hours = int(timezone[1:3])
        minutes = int(timezone[4:6])
        offset = timedelta(hours=sign * hours, minutes=sign * minutes)
        dt_utc = dt_local - offset
    else:
        # Assume UTC if timezone not provided
        dt_utc = dt_local
    
    # Calculate Julian Date
    jd = get_julian_date(dt_utc)
    
    # Calculate Ayanamsha (Lahiri)
    ayanamsha = calculate_ayanamsha(jd)
    
    # Calculate Ascendant
    ascendant_tropical = calculate_ascendant(jd, latitude, longitude)
    ascendant_sidereal = (ascendant_tropical - ayanamsha) % 360.0
    ascendant_sign_idx = int(ascendant_sidereal // 30)
    ascendant_sign = RASIS[ascendant_sign_idx]
    ascendant_degree = ascendant_sidereal % 30
    
    # Calculate planets
    planets = []
    for planet_name in PLANET_NAMES:
        tropical_long, is_retrograde = get_planet_longitude(planet_name, jd)
        sidereal_long = (tropical_long - ayanamsha) % 360.0
        
        sign_idx = int(sidereal_long // 30)
        sign = RASIS[sign_idx]
        degree = sidereal_long % 30
        
        # Calculate house
        house = calculate_planet_house(sidereal_long, ascendant_sidereal)
        
        # Calculate D9 (Navamsa)
        d9_sign = calculate_d9_chart(sidereal_long)
        
        planet_data = {
            "name": planet_name,
            "longitude": round(sidereal_long, 6),
            "sign": sign,
            "degree": round(degree, 6),
            "house": house,
            "isRetrograde": is_retrograde,
            "d9Sign": d9_sign
        }
        
        planets.append(planet_data)
    
    # Calculate houses
    houses = calculate_houses(jd, latitude, longitude, ayanamsha)
    
    # Get Sun and Moon data for quick access
    sun_data = next(p for p in planets if p["name"] == "Sun")
    moon_data = next(p for p in planets if p["name"] == "Moon")
    
    # Calculate Moon Nakshatra
    moon_nakshatra, moon_pada = get_nakshatra(moon_data["longitude"])
    
    # Calculate Vimshottari Dasha
    vimshottari_dasha = calculate_vimshottari_dasha(moon_data["longitude"])
    
    # Build D1 chart (Rasi) - simplified representation
    d1_chart = {
        "ascendant": {
            "sign": ascendant_sign,
            "degree": round(ascendant_degree, 6)
        },
        "planets": {p["name"]: p["sign"] for p in planets}
    }
    
    # Build D9 chart (Navamsa)
    d9_chart = {
        "ascendant": calculate_d9_chart(ascendant_sidereal),
        "planets": {p["name"]: p["d9Sign"] for p in planets}
    }
    
    return {
        "name": name,
        "ascendant": {
            "sign": ascendant_sign,
            "degree": round(ascendant_degree, 6),
            "longitude": round(ascendant_sidereal, 6)
        },
        "sunSign": sun_data["sign"],
        "moonSign": moon_data["sign"],
        "moonNakshatra": moon_nakshatra,
        "pada": moon_pada,
        "ayanamsha": round(ayanamsha, 6),
        "planets": planets,
        "houses": houses,
        "d1Chart": d1_chart,
        "d9Chart": d9_chart,
        "vimshottariDasha": vimshottari_dasha
    }

def calculate_planet_house(planet_longitude: float, ascendant_longitude: float) -> int:
    """Calculate house number for a planet based on its longitude relative to ascendant."""
    # House spans 30 degrees starting from ascendant
    relative_long = (planet_longitude - ascendant_longitude) % 360.0
    house = int(relative_long // 30) + 1
    return house
