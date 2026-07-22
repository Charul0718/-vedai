import os
import logging
import httpx
from typing import Dict, Any, List, Optional

logger = logging.getLogger("vedai.ai_engine")

DISCLAIMER_TEXT = (
    "Disclaimer: Vedic Astrology (Jyotish) is a traditional system of symbolic analysis and reflection. "
    "Interpretations are based on classical texts and modern archetypal synthesis. Astrological insights are "
    "intended for self-reflection and personal growth, and are not scientifically verified predictions, "
    "nor should they substitute for professional financial, legal, or medical advice."
)

class AIEngineClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
    def _call_gemini(self, system_prompt: str, user_prompt: str) -> str:
        """Call Gemini API via HTTP request with fallback to local mock generation."""
        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not set. Falling back to mock generator.")
            return self._generate_mock_explanation(user_prompt)
            
        try:
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{system_prompt}\n\nUser Input:\n{user_prompt}"}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 2048,
                }
            }
            
            # Post request
            url_with_key = f"{self.api_url}?key={self.api_key}"
            response = httpx.post(url_with_key, json=payload, headers=headers, timeout=30.0)
            
            if response.status_code == 200:
                res_data = response.json()
                # Parse gemini response
                candidates = res_data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        text = parts[0].get("text", "")
                        return text
                logger.error(f"Gemini API returned empty response: {res_data}")
            else:
                logger.error(f"Gemini API error (Status {response.status_code}): {response.text}")
                
        except Exception as e:
            logger.exception(f"Failed to communicate with Gemini API: {str(e)}")
            
        return self._generate_mock_explanation(user_prompt)

    def generate_report_explanation(
        self,
        birth_details: Dict[str, Any],
        calculation_results: Dict[str, Any],
        traditional_readings: Dict[str, Any]
    ) -> str:
        """Generate a personalized explanation synthesizing calculations and traditional readings."""
        system_prompt = (
            "You are VedAI, a master Vedic Astrologer and spiritual counselor. "
            "Your job is to read the deterministic calculation data and traditional readings "
            "and synthesize them into an insightful, coherent, and practical life report.\n\n"
            "CRITICAL RULES:\n"
            "1. You must clearly state what is a calculation, what is traditional literature, and what is your AI interpretation.\n"
            "2. Do NOT present astrology as scientifically proven or absolute prediction. Use terms of probability, archetypes, and symbolic reflection.\n"
            "3. Structure your response with Markdown headings (e.g. ### Synthesis, ### Key Life Areas, ### Actionable Guidance).\n"
            f"4. You MUST append the following exact disclaimer text at the very end of your response:\n{DISCLAIMER_TEXT}"
        )
        
        user_prompt = (
            f"Birth Details:\n"
            f"- Name: {birth_details.get('name')}\n"
            f"- Date/Time: {birth_details.get('date_of_birth')} {birth_details.get('time_of_birth')}\n"
            f"- Coordinates: Lat {birth_details.get('latitude')}, Lon {birth_details.get('longitude')}\n\n"
            f"Calculations (Astronomical Facts):\n"
            f"- Ascendant: {calculation_results.get('ascendantSign')} ({calculation_results.get('ascendantDegree'):.2f} degrees)\n"
            f"- Planetary positions: {calculation_results.get('planets')}\n\n"
            f"Traditional Readings (From Classical Texts):\n"
            f"- Ascendant placement reading: {traditional_readings.get('ascendantReading')}\n"
            f"- Placements readings: {traditional_readings.get('planetaryPlacements')}\n"
        )
        
        return self._call_gemini(system_prompt, user_prompt)

    def generate_chat_response(
        self,
        birth_details: Dict[str, Any],
        calculation_results: Dict[str, Any],
        chat_history: List[Dict[str, str]],
        new_message: str
    ) -> str:
        """Generate response in an interactive chat session."""
        system_prompt = (
            "You are the VedAI Astrological Companion, an interactive Vedic Astrology guide. "
            "Answer the user's questions about their birth chart. Reference the calculations "
            "and traditional astrology when appropriate. "
            "Always maintain the distinction between astronomical facts (e.g. planets, degrees), "
            "traditional readings, and your spiritual/personal guidance. "
            "Keep responses conversational, insightful, and clearly grounded in self-reflection. "
            "Never promise future predictions as scientifically verified facts.\n\n"
            f"Include a short note pointing to the symbolic nature of astrology at the end if the user asks for direct predictions.\n"
            f"Add this disclaimer in your response when discussing sensitive topics (health, finance, romance):\n{DISCLAIMER_TEXT}"
        )
        
        history_formatted = ""
        for msg in chat_history:
            role = "User" if msg.get("role") == "user" else "Assistant"
            content = msg.get("content")
            history_formatted += f"{role}: {content}\n"
            
        user_prompt = (
            f"User Birth Chart Data:\n"
            f"- Ascendant: {calculation_results.get('ascendantSign')} ({calculation_results.get('ascendantDegree'):.2f} degrees)\n"
            f"- Planetary positions: {calculation_results.get('planets')}\n\n"
            f"Chat History:\n{history_formatted}"
            f"User Query: {new_message}\n"
        )
        
        return self._call_gemini(system_prompt, user_prompt)

    def _generate_mock_explanation(self, user_prompt: str) -> str:
        """Fallback mock report explanation when API key is missing or calls fail."""
        return (
            "### Astrological Synthesis & Cosmic Alignment\n\n"
            "This synthesized explanation bridges your astronomical birth chart with traditional Vedic astrology "
            "principles, offering a symbolic mirror for self-exploration.\n\n"
            "#### 🌟 The Core Alignment\n"
            "Your Ascendant sign shapes your primary physical interface with reality. The positions of the Sun (core self-expression) "
            "and the Moon (mind and emotions) reveal a dynamic harmony between your inner needs and your outer destiny. "
            "Traditional Vedic readings suggest that placements in key dharma houses (1st, 5th, 9th) call you to express your true path "
            "through creative development and truth-seeking.\n\n"
            "#### 💼 Career and Karma Paths\n"
            "Vedic texts link the 10th house and the position of Saturn to the unfoldment of karma. In your chart, these placements indicate "
            "a steady growth trajectory. Success comes through discipline, service, and aligning your professional work with your "
            "core ethical values. Traditional texts suggest patience in early career, with greater authority blooming after maturity.\n\n"
            "#### 🧘 Guidance for Personal Growth\n"
            "Use this symbolic map to examine where you hold tension and where you feel flow. Aligning with your planetary signatures "
            "means acting with self-awareness in relationships and taking responsibility for your actions (karma).\n\n"
            f"{DISCLAIMER_TEXT}"
        )
