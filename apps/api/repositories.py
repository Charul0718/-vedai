from sqlalchemy.orm import Session
from typing import List, Optional
import models

class UserRepository:
    @staticmethod
    def get_by_id(db: Session, user_id: str) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def create(db: Session, user: models.User) -> models.User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

class BirthDetailsRepository:
    @staticmethod
    def get_by_id(db: Session, details_id: str) -> Optional[models.BirthDetails]:
        return db.query(models.BirthDetails).filter(models.BirthDetails.id == details_id).first()

    @staticmethod
    def list_by_user(db: Session, user_id: str) -> List[models.BirthDetails]:
        return db.query(models.BirthDetails).filter(models.BirthDetails.user_id == user_id).order_by(models.BirthDetails.created_at.desc()).all()

    @staticmethod
    def create(db: Session, details: models.BirthDetails) -> models.BirthDetails:
        db.add(details)
        db.commit()
        db.refresh(details)
        return details

class BirthChartRepository:
    @staticmethod
    def get_by_birth_details_id(db: Session, details_id: str) -> Optional[models.BirthChart]:
        return db.query(models.BirthChart).filter(models.BirthChart.birth_details_id == details_id).first()

    @staticmethod
    def create(db: Session, chart: models.BirthChart) -> models.BirthChart:
        db.add(chart)
        db.commit()
        db.refresh(chart)
        return chart

class ReportRepository:
    @staticmethod
    def get_by_id(db: Session, report_id: str) -> Optional[models.Report]:
        return db.query(models.Report).filter(models.Report.id == report_id).first()

    @staticmethod
    def list_by_user(db: Session, user_id: str) -> List[models.Report]:
        return db.query(models.Report).filter(models.Report.user_id == user_id).order_by(models.Report.generated_at.desc()).all()

    @staticmethod
    def create(db: Session, report: models.Report) -> models.Report:
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

class ChatSessionRepository:
    @staticmethod
    def get_by_id(db: Session, session_id: str) -> Optional[models.ChatSession]:
        return db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()

    @staticmethod
    def list_by_user(db: Session, user_id: str) -> List[models.ChatSession]:
        return db.query(models.ChatSession).filter(models.ChatSession.user_id == user_id).order_by(models.ChatSession.created_at.desc()).all()

    @staticmethod
    def create(db: Session, session: models.ChatSession) -> models.ChatSession:
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def add_message(db: Session, message: models.ChatMessage) -> models.ChatMessage:
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def list_messages(db: Session, session_id: str) -> List[models.ChatMessage]:
        return db.query(models.ChatMessage).filter(models.ChatMessage.chat_session_id == session_id).order_by(models.ChatMessage.created_at.asc()).all()
