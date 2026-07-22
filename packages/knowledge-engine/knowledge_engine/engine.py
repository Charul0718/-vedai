"""
Knowledge Engine for VedAI Astrology System.

Provides structured lookup for astrological entities without AI or natural language generation.
"""

import json
import os
from typing import Dict, Any, Optional


class KnowledgeEngine:
    """Structured knowledge base for Vedic astrology."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """Initialize the knowledge engine with data directory."""
        if data_dir is None:
            # Default to data directory relative to this file
            self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        else:
            self.data_dir = data_dir
        
        # Load all knowledge bases
        self._planets = self._load_json("planets.json", "planets")
        self._houses = self._load_json("houses.json", "houses")
        self._signs = self._load_json("signs.json", "signs")
        self._nakshatras = self._load_json("nakshatras.json", "nakshatras")
        self._bhavas = self._load_json("bhavas.json", "bhavas")
        self._dasha = self._load_json("dasha.json", "vimshottari_dasha")
        self._yogas = self._load_json("yogas.json", "yogas")
        self._doshas = self._load_json("doshas.json", "doshas")
    
    def _load_json(self, filename: str, key: str) -> Dict[str, Any]:
        """Load JSON file from data directory."""
        file_path = os.path.join(self.data_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get(key, {})
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
    
    def lookup(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lookup astrological knowledge based on query parameters.
        
        Input:
        {
            planet: str (optional),
            house: str/int (optional),
            sign: str (optional),
            dasha: str (optional),
            nakshatra: str (optional),
            bhava: str/int (optional),
            yoga: str (optional),
            dosha: str (optional)
        }
        
        Returns structured JSON with matching knowledge entries.
        """
        result = {}
        
        # Lookup planet
        if "planet" in query and query["planet"]:
            planet_name = query["planet"]
            if planet_name in self._planets:
                result["planet"] = self._planets[planet_name]
        
        # Lookup house
        if "house" in query and query["house"]:
            house_key = str(query["house"])
            if house_key in self._houses:
                result["house"] = self._houses[house_key]
        
        # Lookup sign
        if "sign" in query and query["sign"]:
            sign_name = query["sign"]
            if sign_name in self._signs:
                result["sign"] = self._signs[sign_name]
        
        # Lookup nakshatra
        if "nakshatra" in query and query["nakshatra"]:
            nakshatra_name = query["nakshatra"]
            if nakshatra_name in self._nakshatras:
                result["nakshatra"] = self._nakshatras[nakshatra_name]
        
        # Lookup bhava
        if "bhava" in query and query["bhava"]:
            bhava_key = str(query["bhava"])
            if bhava_key in self._bhavas:
                result["bhava"] = self._bhavas[bhava_key]
        
        # Lookup dasha
        if "dasha" in query and query["dasha"]:
            dasha_name = query["dasha"]
            if dasha_name in self._dasha:
                result["dasha"] = self._dasha[dasha_name]
        
        # Lookup yoga
        if "yoga" in query and query["yoga"]:
            yoga_name = query["yoga"]
            if yoga_name in self._yogas:
                result["yoga"] = self._yogas[yoga_name]
        
        # Lookup dosha
        if "dosha" in query and query["dosha"]:
            dosha_name = query["dosha"]
            if dosha_name in self._doshas:
                result["dosha"] = self._doshas[dosha_name]
        
        return result
    
    def get_planet(self, planet_name: str) -> Optional[Dict[str, Any]]:
        """Get knowledge for a specific planet."""
        return self._planets.get(planet_name)
    
    def get_house(self, house_number: int) -> Optional[Dict[str, Any]]:
        """Get knowledge for a specific house."""
        return self._houses.get(str(house_number))
    
    def get_sign(self, sign_name: str) -> Optional[Dict[str, Any]]:
        """Get knowledge for a specific zodiac sign."""
        return self._signs.get(sign_name)
    
    def get_nakshatra(self, nakshatra_name: str) -> Optional[Dict[str, Any]]:
        """Get knowledge for a specific nakshatra."""
        return self._nakshatras.get(nakshatra_name)
    
    def get_bhava(self, bhava_number: int) -> Optional[Dict[str, Any]]:
        """Get knowledge for a specific bhava."""
        return self._bhavas.get(str(bhava_number))
    
    def get_dasha(self, dasha_name: str) -> Optional[Dict[str, Any]]:
        """Get knowledge for a specific Vimshottari dasha."""
        return self._dasha.get(dasha_name)
    
    def get_yoga(self, yoga_name: str) -> Optional[Dict[str, Any]]:
        """Get knowledge for a specific yoga."""
        return self._yogas.get(yoga_name)
    
    def get_dosha(self, dosha_name: str) -> Optional[Dict[str, Any]]:
        """Get knowledge for a specific dosha."""
        return self._doshas.get(dosha_name)
    
    def list_planets(self) -> list:
        """List all available planets."""
        return list(self._planets.keys())
    
    def list_houses(self) -> list:
        """List all available houses."""
        return list(self._houses.keys())
    
    def list_signs(self) -> list:
        """List all available zodiac signs."""
        return list(self._signs.keys())
    
    def list_nakshatras(self) -> list:
        """List all available nakshatras."""
        return list(self._nakshatras.keys())
    
    def list_bhavas(self) -> list:
        """List all available bhavas."""
        return list(self._bhavas.keys())
    
    def list_dasha_periods(self) -> list:
        """List all available Vimshottari dasha periods."""
        return list(self._dasha.keys())
    
    def list_yogas(self) -> list:
        """List all available yogas."""
        return list(self._yogas.keys())
    
    def list_doshas(self) -> list:
        """List all available doshas."""
        return list(self._doshas.keys())


# Global instance for easy access
_engine_instance = None


def get_engine(data_dir: Optional[str] = None) -> KnowledgeEngine:
    """Get or create the global knowledge engine instance."""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = KnowledgeEngine(data_dir)
    return _engine_instance


def lookup(query: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function for knowledge lookup.
    
    Input:
    {
        planet: str (optional),
        house: str/int (optional),
        sign: str (optional),
        dasha: str (optional)
    }
    
    Returns structured JSON with matching knowledge entries.
    """
    engine = get_engine()
    return engine.lookup(query)
