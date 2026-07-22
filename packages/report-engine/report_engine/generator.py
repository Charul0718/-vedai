import os
from typing import Dict, Any, List
from fpdf import FPDF

# Traditional Vedic Astrological Interpretation Database
# These are symbolic representations based on classical Jyotish rules (e.g., Parashara)
TRADITIONAL_ASCENDANTS = {
    "Aries": "Aries Ascendant (Mesha Lagna): Ruled by Mars. Indicates a pioneering, energetic, and courageous nature. Expresses life with direct action and enthusiasm.",
    "Taurus": "Taurus Ascendant (Vrishabha Lagna): Ruled by Venus. Represents stability, beauty, perseverance, and appreciation of material and sensory comforts.",
    "Gemini": "Gemini Ascendant (Mithuna Lagna): Ruled by Mercury. Signifies intellectual curiosity, dual perspectives, adaptability, and expressive communication skills.",
    "Cancer": "Cancer Ascendant (Karka Lagna): Ruled by the Moon. Highlights intuition, maternal protection, emotional depth, sensitivity, and strong connection to home.",
    "Leo": "Leo Ascendant (Simha Lagna): Ruled by the Sun. Reflects leadership qualities, magnanimity, vital self-expression, and a strong sense of personal dignity.",
    "Virgo": "Virgo Ascendant (Kanya Lagna): Ruled by Mercury. Denotes analytical precision, service-oriented nature, focus on health, and detail-oriented execution.",
    "Libra": "Libra Ascendant (Tula Lagna): Ruled by Venus. Focuses on harmony, relationship balance, justice, artistic inclination, and social diplomacy.",
    "Scorpio": "Scorpio Ascendant (Vrischika Lagna): Ruled by Mars/Ketu. Represents intense emotional depth, transformation, interest in esoteric mysteries, and strong willpower.",
    "Sagittarius": "Sagittarius Ascendant (Dhanu Lagna): Ruled by Jupiter. Represents philosophical optimism, search for truth, academic wisdom, and love for exploration.",
    "Capricorn": "Capricorn Ascendant (Makara Lagna): Ruled by Saturn. Emphasizes duty, career ambition, structured discipline, structural organization, and patient growth.",
    "Aquarius": "Aquarius Ascendant (Kumbha Lagna): Ruled by Saturn/Rahu. Highlights humanitarian visions, progressive thoughts, social networking, and unconventional approaches.",
    "Pisces": "Pisces Ascendant (Meena Lagna): Ruled by Jupiter/Ketu. Signifies imaginative depth, spiritual surrender, compassion, artistic dreams, and dissolution of boundaries."
}

TRADITIONAL_PLANETS_IN_SIGNS = {
    "Sun": {
        "Aries": "Sun is Exalted in Aries. Represents high confidence, leadership capability, strong vitality, and independent willpower.",
        "Libra": "Sun is Debilitated in Libra. Indicates challenges in self-assertion, tendency to compromise personal authority for peace.",
        "default": "Sun represents the core soul identity (Atmakaraka) and authority. Its placement here indicates where you seek recognition."
    },
    "Moon": {
        "Taurus": "Moon is Exalted in Taurus. Signifies emotional stability, contented mind, sensory appreciation, and nurturing qualities.",
        "Scorpio": "Moon is Debilitated in Scorpio. Points to emotional sensitivity, intense inner processing, and vulnerability to mood swings.",
        "default": "Moon governs the mind (Manas) and emotional responses. Its placement indicates emotional focus."
    },
    "default": "Traditional texts describe planetary placements as planetary states (Avasthas) reflecting spiritual tendencies."
}

def compile_traditional_readings(calc: Dict[str, Any]) -> Dict[str, Any]:
    """Examine calculated planetary positions and compile traditional text-based readings."""
    asc_sign = calc.get("ascendantSign", "Aries")
    asc_reading = TRADITIONAL_ASCENDANTS.get(
        asc_sign, 
        f"Lagna in {asc_sign}: Traditional texts outline general personality patterns related to this sign's planetary ruler."
    )
    
    planetary_placements = []
    for p in calc.get("planets", []):
        p_name = p["name"]
        p_sign = p["sign"]
        p_house = p.get("house", 1)
        
        # Determine sign placement reading
        sign_reading = ""
        if p_name in TRADITIONAL_PLANETS_IN_SIGNS and p_sign in TRADITIONAL_PLANETS_IN_SIGNS[p_name]:
            sign_reading = TRADITIONAL_PLANETS_IN_SIGNS[p_name][p_sign]
        else:
            sign_reading = TRADITIONAL_PLANETS_IN_SIGNS.get(p_name, {}).get(
                "default", 
                f"Traditional scriptures state that {p_name} in {p_sign} directs planetary energy through the traits of {p_sign}."
            )
            
        # Determine house placement reading
        house_reading = (
            f"Traditional texts place {p_name} in the {p_house} House. "
            f"This placement influences the areas of life governed by this house (e.g. self, wealth, career, partner)."
        )
        
        planetary_placements.append({
            "planet": p_name,
            "reading": f"{sign_reading} {house_reading}"
        })
        
    return {
        "ascendantReading": asc_reading,
        "planetaryPlacements": planetary_placements
    }

class ReportPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42) # slate-900 background
        # We can write a simple header
        self.set_text_color(148, 163, 184) # slate-400
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, 'VedAI - Personalized Vedic Astrological Analysis', border=0, ln=1, align='L')
        self.ln(5)

    def footer(self):
        self.set_y(-25)
        self.set_font('helvetica', 'I', 7)
        self.set_text_color(148, 163, 184)
        
        # Mandatory Scientific Disclaimer
        disclaimer = (
            "Disclaimer: Vedic Astrology is an ancient system of symbolic reflection and archetypal analysis. "
            "It is not scientifically verified as a predictive tool. This report is for personal growth and educational purposes only."
        )
        self.multi_cell(0, 4, disclaimer, align='C')
        self.ln(2)
        self.cell(0, 10, f'Page {self.page_no()}', border=0, align='C')

class ReportGenerator:
    def __init__(self, output_dir: str = "/tmp"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_pdf(
        self,
        report_id: str,
        birth_details: Dict[str, Any],
        calc: Dict[str, Any],
        traditional: Dict[str, Any],
        ai_explanation: str
    ) -> str:
        """Compile reports and output a high-fidelity PDF file."""
        pdf = ReportPDF()
        pdf.set_auto_page_break(auto=True, margin=30)
        
        # ----------------------------------------------------
        # Page 1: COVER PAGE
        # ----------------------------------------------------
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 28)
        pdf.set_text_color(99, 102, 241) # Indigo primary
        pdf.ln(40)
        pdf.cell(0, 15, "VEDAI REPORT", ln=True, align='C')
        
        pdf.set_font('helvetica', 'I', 14)
        pdf.set_text_color(226, 232, 240) # Slate slate-200
        pdf.cell(0, 10, "Ancient Wisdom. Powered by AI.", ln=True, align='C')
        
        pdf.ln(30)
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(226, 232, 240)
        pdf.cell(0, 8, f"PREPARED FOR: {birth_details.get('name')}", ln=True, align='C')
        pdf.set_font('helvetica', '', 10)
        pdf.cell(0, 6, f"Birth Date: {birth_details.get('date_of_birth')}", ln=True, align='C')
        pdf.cell(0, 6, f"Birth Time: {birth_details.get('time_of_birth')}", ln=True, align='C')
        pdf.cell(0, 6, f"Location: {birth_details.get('location_name')}", ln=True, align='C')
        
        # ----------------------------------------------------
        # Page 2: ASTRONOMICAL CALCULATIONS (FACTS)
        # ----------------------------------------------------
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 16)
        pdf.set_text_color(99, 102, 241)
        pdf.cell(0, 10, "1. Deterministic Astronomical Calculations", ln=True)
        pdf.set_font('helvetica', 'I', 9)
        pdf.set_text_color(148, 163, 184)
        pdf.cell(0, 6, "Note: This section lists astronomically verified coordinates converted into Sidereal degrees (Lahiri Ayanamsha).", ln=True)
        pdf.ln(5)
        
        pdf.set_font('helvetica', 'B', 11)
        pdf.set_text_color(226, 232, 240)
        pdf.cell(0, 8, f"Ascendant (Lagna): {calc.get('ascendantSign')} ({calc.get('ascendantDegree'):.2f}°)", ln=True)
        pdf.cell(0, 8, f"Calculated Ayanamsha: {calc.get('ayanamsha'):.4f}°", ln=True)
        pdf.ln(4)
        
        # Table of Planet Coordinates
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(40, 7, "Planet Name", border=1, align='C')
        pdf.cell(50, 7, "Sidereal Longitude", border=1, align='C')
        pdf.cell(40, 7, "Zodiac Sign", border=1, align='C')
        pdf.cell(30, 7, "House No.", border=1, align='C')
        pdf.cell(30, 7, "Retrograde?", border=1, align='C')
        pdf.ln(7)
        
        pdf.set_font('helvetica', '', 9)
        for p in calc.get("planets", []):
            retro_text = "Yes" if p.get("isRetrograde") else "No"
            pdf.cell(40, 6, p["name"], border=1, align='C')
            pdf.cell(50, 6, f"{p['longitude']:.4f}°", border=1, align='C')
            pdf.cell(40, 6, f"{p['sign']} ({p['degree']:.2f}°)", border=1, align='C')
            pdf.cell(30, 6, str(p.get("house", 1)), border=1, align='C')
            pdf.cell(30, 6, retro_text, border=1, align='C')
            pdf.ln(6)
            
        # ----------------------------------------------------
        # Page 3: TRADITIONAL INTERPRETATIONS
        # ----------------------------------------------------
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 16)
        pdf.set_text_color(99, 102, 241)
        pdf.cell(0, 10, "2. Traditional Vedic Astrology Interpretations", ln=True)
        pdf.set_font('helvetica', 'I', 9)
        pdf.set_text_color(148, 163, 184)
        pdf.cell(0, 6, "Note: These interpretations are compiled from classical Hindu scriptures (Brihat Parashara Hora Shastra, etc.).", ln=True)
        pdf.ln(5)
        
        pdf.set_font('helvetica', 'B', 11)
        pdf.set_text_color(226, 232, 240)
        pdf.cell(0, 8, "Ascendant Influence:", ln=True)
        pdf.set_font('helvetica', '', 10)
        pdf.multi_cell(0, 5, traditional.get("ascendantReading", ""))
        pdf.ln(5)
        
        pdf.set_font('helvetica', 'B', 11)
        pdf.set_text_color(226, 232, 240)
        pdf.cell(0, 8, "Key Planetary Placements:", ln=True)
        pdf.set_font('helvetica', '', 10)
        for placement in traditional.get("planetaryPlacements", []):
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(0, 6, f"- {placement['planet']}:", ln=True)
            pdf.set_font('helvetica', '', 10)
            pdf.multi_cell(0, 5, placement["reading"])
            pdf.ln(2)
            
        # ----------------------------------------------------
        # Page 4: AI SPIRITUAL SYNTHESIS
        # ----------------------------------------------------
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 16)
        pdf.set_text_color(99, 102, 241)
        pdf.cell(0, 10, "3. AI-Generated Synthesized Explanation", ln=True)
        pdf.set_font('helvetica', 'I', 9)
        pdf.set_text_color(148, 163, 184)
        pdf.cell(0, 6, "Note: This section is generated by a large language model to synthesize facts and traditions into a modern narrative.", ln=True)
        pdf.ln(5)
        
        pdf.set_font('helvetica', '', 10)
        pdf.set_text_color(226, 232, 240)
        # We need to strip or split AI markdown output to cleanly output in FPDF
        cleaned_explanation = ai_explanation.replace("### ", "\n\n").replace("#### ", "\n").replace("**", "")
        # Add paragraphs
        pdf.multi_cell(0, 5, cleaned_explanation)
        
        # Save to output file
        filename = f"vedai_report_{report_id}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        pdf.output(filepath)
        
        return filepath
