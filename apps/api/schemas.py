from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Birth Details Schemas
class BirthDetailsCreate(BaseModel):
    name: str = Field(..., example="Arjun")
    date_of_birth: str = Field(..., example="1995-10-25")
    time_of_birth: str = Field(..., example="08:30")
    location_name: str = Field(..., example="Mumbai, India")
    latitude: float = Field(..., example=19.076)
    longitude: float = Field(..., example=72.877)
    timezone: str = Field(..., example="Asia/Kolkata")

class BirthDetailsResponse(BirthDetailsCreate):
    id: str
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Planetary Positions & Houses
class PlanetPositionResponse(BaseModel):
    planet_name: str
    longitude: float
    sign: str
    degree: float
    house_number: int
    is_retrograde: bool
    
    class Config:
        from_attributes = True

class HouseResponse(BaseModel):
    house_number: int
    sign: str
    start_degree: float
    mid_degree: float
    end_degree: float
    
    class Config:
        from_attributes = True

class BirthChartResponse(BaseModel):
    id: str
    birth_details_id: str
    chart_type: str
    ascendant_sign: str
    ascendant_degree: float
    planets: List[PlanetPositionResponse]
    houses: List[HouseResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Reports
class ReportCreateRequest(BaseModel):
    birth_details_id: str
    report_type: str = Field("comprehensive", example="comprehensive")

class ReportResponse(BaseModel):
    id: str
    user_id: str
    birth_details_id: str
    report_type: str
    input_details: Dict[str, Any]
    calculation_results: Dict[str, Any]
    traditional_interpretations: Dict[str, Any]
    ai_explanation: str
    generated_at: datetime
    pdf_url: Optional[str] = None
    
    class Config:
        from_attributes = True

# Chat
class ChatSessionCreate(BaseModel):
    birth_details_id: str
    title: str = Field("New Astrology Chat")

class ChatSessionResponse(BaseModel):
    id: str
    user_id: str
    birth_details_id: str
    title: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatMessageCreate(BaseModel):
    content: str

class ChatMessageResponse(BaseModel):
    id: str
    chat_session_id: str
    role: str
    content: str
    astronomical_data: Optional[Dict[str, Any]] = None
    interpretation_data: Optional[Dict[str, Any]] = None
    ai_insights: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Chart Calculation
class ChartCalculationRequest(BaseModel):
    name: str = Field(..., example="Arjun")
    birthDate: str = Field(..., example="1995-10-25")
    birthTime: str = Field(..., example="08:30")
    latitude: float = Field(..., example=19.076)
    longitude: float = Field(..., example=72.877)
    timezone: str = Field(..., example="+05:30")

class ChartCalculationResponse(BaseModel):
    name: str
    ascendant: Dict[str, Any]
    sunSign: str
    moonSign: str
    moonNakshatra: str
    pada: int
    ayanamsha: float
    planets: List[Dict[str, Any]]
    houses: List[Dict[str, Any]]
    d1Chart: Dict[str, Any]
    d9Chart: Dict[str, Any]
    vimshottariDasha: Dict[str, Any]

# Explainability
class ExplainabilityRequest(BaseModel):
    birth_details_id: str
    domains: Optional[List[str]] = None

class EvidenceItem(BaseModel):
    factor: str
    source: str
    impact: float
    explanation: str

class PlanetaryEvidenceItem(BaseModel):
    planet: str
    house: Optional[int] = None
    sign: Optional[str] = None
    isRetrograde: bool = False
    role: str = ""
    contribution: float = 0.0

class ReasoningStepItem(BaseModel):
    step: int
    description: str
    detail: str

class DomainResultResponse(BaseModel):
    domain: str
    score: float
    confidence: float
    supportingFactors: List[EvidenceItem] = []
    challengingFactors: List[EvidenceItem] = []
    planetaryEvidence: List[PlanetaryEvidenceItem] = []
    reasoningSteps: List[ReasoningStepItem] = []
    explanationSummary: str = ""
