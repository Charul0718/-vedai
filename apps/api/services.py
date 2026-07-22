import os
import sys
import datetime
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from typing import Dict, Any, List, Optional
import models
import schemas
from database import settings
from repositories import (
    UserRepository,
    BirthDetailsRepository,
    BirthChartRepository,
    ReportRepository,
    ChatSessionRepository
)

# Add packages to path for local development
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASTROLOGY_ENGINE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../packages/astrology-engine"))
AI_ENGINE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../packages/ai-engine"))
REPORT_ENGINE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../packages/report-engine"))
KNOWLEDGE_ENGINE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../packages/knowledge-engine"))
EXPLAINABILITY_ENGINE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../packages/explainability-engine"))

for pkg_dir in [ASTROLOGY_ENGINE_DIR, AI_ENGINE_DIR, REPORT_ENGINE_DIR, KNOWLEDGE_ENGINE_DIR, EXPLAINABILITY_ENGINE_DIR]:
    if pkg_dir not in sys.path:
        sys.path.insert(0, pkg_dir)

from astrology_engine.calculations import calculate_vedic_chart
from ai_engine.client import AIEngineClient
from report_engine.generator import ReportGenerator, compile_traditional_readings
from explainability_engine import ExplainabilityEngine

# Password Hashing & JWT Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ai_client = AIEngineClient(api_key=settings.GEMINI_API_KEY)
report_gen = ReportGenerator(output_dir=settings.PDF_OUTPUT_DIR)

class AuthService:
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

class AstrologyService:
    @staticmethod
    def get_or_create_chart(db: Session, details: models.BirthDetails) -> models.BirthChart:
        # Check if chart exists
        chart = BirthChartRepository.get_by_birth_details_id(db, details.id)
        if chart:
            return chart
            
        # Parse timezone offset (approximate from timezone string or keep static +5.5 for simplicity)
        # We can extract offset based on commonly used timezones or pass it
        # E.g. Asia/Kolkata is +5.5. Let's write a simple timezone offset mapper
        tz_offset = 5.5
        if "america" in details.timezone.lower():
            tz_offset = -5.0 # EST
        elif "europe" in details.timezone.lower():
            tz_offset = 1.0 # CET
            
        # Trigger deterministic astrology engine calculations
        calc_result = calculate_vedic_chart(
            name=details.name,
            dob=details.date_of_birth,
            tob=details.time_of_birth,
            lat=details.latitude,
            lon=details.longitude,
            tz_offset=tz_offset
        )
        
        # Save BirthChart
        chart = models.BirthChart(
            birth_details_id=details.id,
            chart_type="Rasi (D1)",
            ascendant_sign=calc_result["ascendantSign"],
            ascendant_degree=calc_result["ascendantDegree"]
        )
        chart = BirthChartRepository.create(db, chart)
        
        # Save Planets
        for p in calc_result["planets"]:
            planet_pos = models.PlanetPosition(
                birth_chart_id=chart.id,
                planet_name=p["name"],
                longitude=p["longitude"],
                sign=p["sign"],
                degree=p["degree"],
                house_number=p["house"],
                is_retrograde=p["isRetrograde"]
            )
            db.add(planet_pos)
            
        # Save Houses
        for h in calc_result["houses"]:
            house_item = models.House(
                birth_chart_id=chart.id,
                house_number=h["number"],
                sign=h["sign"],
                start_degree=h["startDegree"],
                mid_degree=h["midDegree"],
                end_degree=h["endDegree"]
            )
            db.add(house_item)
            
        db.commit()
        db.refresh(chart)
        return chart

class ReportService:
    @staticmethod
    def generate_report(db: Session, user_id: str, birth_details_id: str, report_type: str) -> models.Report:
        # Load details
        details = BirthDetailsRepository.get_by_id(db, birth_details_id)
        if not details or details.user_id != user_id:
            raise ValueError("Birth details not found or access denied")
            
        # 1. Compile or load astronomical chart
        chart = AstrologyService.get_or_create_chart(db, details)
        
        # Format calculations into matching payload
        calc_data = {
            "ascendantSign": chart.ascendant_sign,
            "ascendantDegree": chart.ascendant_degree,
            "ayanamsha": 23.85, # placeholder for rendering
            "planets": [
                {
                    "name": p.planet_name,
                    "longitude": p.longitude,
                    "sign": p.sign,
                    "degree": p.degree,
                    "house": p.house_number,
                    "isRetrograde": p.is_retrograde
                } for p in chart.planets
            ],
            "houses": [
                {
                    "number": h.house_number,
                    "sign": h.sign,
                    "midDegree": h.mid_degree
                } for h in chart.houses
            ]
        }
        
        # 2. Compile traditional readings from report engine
        traditional_readings = compile_traditional_readings(calc_data)
        
        # 3. Generate AI explanations using prompt system
        birth_details_dict = {
            "name": details.name,
            "date_of_birth": details.date_of_birth,
            "time_of_birth": details.time_of_birth,
            "latitude": details.latitude,
            "longitude": details.longitude
        }
        
        ai_explanation = ai_client.generate_report_explanation(
            birth_details=birth_details_dict,
            calculation_results=calc_data,
            traditional_readings=traditional_readings
        )
        
        # 4. Compile into final PDF
        report_id = str(datetime.datetime.utcnow().timestamp()).replace(".", "")
        pdf_path = report_gen.generate_pdf(
            report_id=report_id,
            birth_details=birth_details_dict,
            calc=calc_data,
            traditional=traditional_readings,
            ai_explanation=ai_explanation
        )
        
        # Save report DB entry
        report = models.Report(
            user_id=user_id,
            birth_details_id=details.id,
            report_type=report_type,
            input_details={
                "name": details.name,
                "dateTime": f"{details.date_of_birth} {details.time_of_birth}",
                "location": details.location_name
            },
            calculation_results=calc_data,
            traditional_interpretations=traditional_readings,
            ai_explanation=ai_explanation,
            pdf_url=f"/static/reports/vedai_report_{report_id}.pdf"
        )
        
        return ReportRepository.create(db, report)

class ChatService:
    @staticmethod
    def handle_message(db: Session, user_id: str, session_id: str, message_content: str) -> models.ChatMessage:
        # Load session
        session = ChatSessionRepository.get_by_id(db, session_id)
        if not session or session.user_id != user_id:
            raise ValueError("Chat session not found or access denied")
            
        # Get chart data
        chart = AstrologyService.get_or_create_chart(db, session.birth_details)
        calc_data = {
            "ascendantSign": chart.ascendant_sign,
            "ascendantDegree": chart.ascendant_degree,
            "planets": [
                {
                    "name": p.planet_name,
                    "longitude": p.longitude,
                    "sign": p.sign,
                    "degree": p.degree,
                    "house": p.house_number,
                    "isRetrograde": p.is_retrograde
                } for p in chart.planets
            ]
        }
        
        # Load message history
        messages_db = ChatSessionRepository.list_messages(db, session_id)
        chat_history = [{"role": msg.role, "content": msg.content} for msg in messages_db]
        
        # 1. Create and save user message
        user_message = models.ChatMessage(
            chat_session_id=session_id,
            role="user",
            content=message_content
        )
        ChatSessionRepository.add_message(db, user_message)
        
        # 2. Get AI companion response
        ai_response = ai_client.generate_chat_response(
            birth_details={"name": session.birth_details.name},
            calculation_results=calc_data,
            chat_history=chat_history,
            new_message=message_content
        )
        
        # 3. Create and save assistant message
        assistant_message = models.ChatMessage(
            chat_session_id=session_id,
            role="assistant",
            content=ai_response,
            astronomical_data=calc_data,
            interpretation_data=compile_traditional_readings(calc_data)
        )
        ChatSessionRepository.add_message(db, assistant_message)
        
        return assistant_message

class ExplainabilityService:
    _engine = ExplainabilityEngine()

    @staticmethod
    def evaluate_chart(
        db: Session, birth_details_id: str, domains: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        details = BirthDetailsRepository.get_by_id(db, birth_details_id)
        if not details:
            raise ValueError("Birth details not found")

        chart = AstrologyService.get_or_create_chart(db, details)
        calc_data = {
            "planets": [
                {
                    "name": p.planet_name,
                    "longitude": p.longitude,
                    "sign": p.sign,
                    "degree": p.degree,
                    "house": p.house_number,
                    "isRetrograde": p.is_retrograde,
                }
                for p in chart.planets
            ],
            "houses": [
                {
                    "number": h.house_number,
                    "sign": h.sign,
                    "midDegree": h.mid_degree,
                }
                for h in chart.houses
            ],
            "vimshottariDasha": {
                "currentDasha": "",
                "dashaSequence": [],
                "dashaPeriods": {},
            },
        }

        explainer = ExplainabilityService._engine
        if domains:
            results = {}
            for d in domains:
                result = explainer.evaluate(calc_data, d)
                if result:
                    results[d] = explainer.to_dict(result)
            return results

        all_results = explainer.evaluate_all(calc_data)
        return {d: explainer.to_dict(r) for d, r in all_results.items()}
