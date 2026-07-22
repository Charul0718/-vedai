import datetime
import uuid
from sqlalchemy import (
    Column,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    birth_details = relationship("BirthDetails", back_populates="user", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")

class BirthDetails(Base):
    __tablename__ = "birth_details"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False) # YYYY-MM-DD
    time_of_birth = Column(String, nullable=False) # HH:MM
    location_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timezone = Column(String, nullable=False) # e.g. Asia/Kolkata
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="birth_details")
    charts = relationship("BirthChart", back_populates="birth_details", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="birth_details", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="birth_details", cascade="all, delete-orphan")

class BirthChart(Base):
    __tablename__ = "birth_charts"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    birth_details_id = Column(String, ForeignKey("birth_details.id"), nullable=False)
    chart_type = Column(String, default="Rasi (D1)")
    ascendant_sign = Column(String, nullable=False)
    ascendant_degree = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    birth_details = relationship("BirthDetails", back_populates="charts")
    planets = relationship("PlanetPosition", back_populates="chart", cascade="all, delete-orphan")
    houses = relationship("House", back_populates="chart", cascade="all, delete-orphan")

class PlanetPosition(Base):
    __tablename__ = "planet_positions"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    birth_chart_id = Column(String, ForeignKey("birth_charts.id"), nullable=False)
    planet_name = Column(String, nullable=False)
    longitude = Column(Float, nullable=False)
    sign = Column(String, nullable=False)
    degree = Column(Float, nullable=False)
    house_number = Column(Integer, nullable=False)
    is_retrograde = Column(Boolean, default=False)
    
    chart = relationship("BirthChart", back_populates="planets")

class House(Base):
    __tablename__ = "houses"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    birth_chart_id = Column(String, ForeignKey("birth_charts.id"), nullable=False)
    house_number = Column(Integer, nullable=False)
    sign = Column(String, nullable=False)
    start_degree = Column(Float, default=0.0)
    mid_degree = Column(Float, default=15.0)
    end_degree = Column(Float, default=30.0)
    
    chart = relationship("BirthChart", back_populates="houses")

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    birth_details_id = Column(String, ForeignKey("birth_details.id"), nullable=False)
    report_type = Column(String, default="comprehensive")
    input_details = Column(JSON, nullable=False)
    calculation_results = Column(JSON, nullable=False)
    traditional_interpretations = Column(JSON, nullable=False)
    ai_explanation = Column(Text, nullable=False)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)
    pdf_url = Column(String, nullable=True)
    
    user = relationship("User", back_populates="reports")
    birth_details = relationship("BirthDetails", back_populates="reports")

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    birth_details_id = Column(String, ForeignKey("birth_details.id"), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="chat_sessions")
    birth_details = relationship("BirthDetails", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    chat_session_id = Column(String, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String, nullable=False) # user or assistant
    content = Column(Text, nullable=False)
    astronomical_data = Column(JSON, nullable=True)
    interpretation_data = Column(JSON, nullable=True)
    ai_insights = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    session = relationship("ChatSession", back_populates="messages")
