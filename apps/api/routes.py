from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import List, Dict
import database
import models
import schemas
from repositories import UserRepository, BirthDetailsRepository, ReportRepository, ChatSessionRepository
from services import AuthService, AstrologyService, ReportService, ChatService, ExplainabilityService
from astrology_engine import calculate_birth_chart

router = APIRouter(prefix="/api")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login-form")

# Authentication Dependency
def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, database.settings.SECRET_KEY, algorithms=[database.settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
        
    user = UserRepository.get_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# ==========================================
# AUTH ENDPOINTS
# ==========================================
@router.post("/auth/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = UserRepository.get_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_pwd = AuthService.get_password_hash(user_in.password)
    user = models.User(
        email=user_in.email,
        full_name=user_in.full_name,
        password_hash=hashed_pwd
    )
    return UserRepository.create(db, user)

@router.post("/auth/login", response_model=schemas.Token)
def login(user_in: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = UserRepository.get_by_email(db, email=user_in.email)
    if not user or not AuthService.verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    access_token = AuthService.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Form URL-encoded login for OAuth2 Swagger UI support
from fastapi.security import OAuth2PasswordRequestForm
@router.post("/auth/login-form", response_model=schemas.Token, include_in_schema=False)
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = UserRepository.get_by_email(db, email=form_data.username)
    if not user or not AuthService.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    access_token = AuthService.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# ==========================================
# BIRTH DETAILS ENDPOINTS
# ==========================================
@router.post("/birth-details", response_model=schemas.BirthDetailsResponse)
def create_birth_details(
    details_in: schemas.BirthDetailsCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    details = models.BirthDetails(
        user_id=current_user.id,
        name=details_in.name,
        date_of_birth=details_in.date_of_birth,
        time_of_birth=details_in.time_of_birth,
        location_name=details_in.location_name,
        latitude=details_in.latitude,
        longitude=details_in.longitude,
        timezone=details_in.timezone
    )
    return BirthDetailsRepository.create(db, details)

@router.get("/birth-details", response_model=List[schemas.BirthDetailsResponse])
def get_birth_details(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return BirthDetailsRepository.list_by_user(db, user_id=current_user.id)

@router.get("/birth-details/{details_id}/chart", response_model=schemas.BirthChartResponse)
def get_chart(
    details_id: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    details = BirthDetailsRepository.get_by_id(db, details_id)
    if not details or details.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Birth details profile not found")
        
    chart = AstrologyService.get_or_create_chart(db, details)
    return chart

# ==========================================
# REPORT ENDPOINTS
# ==========================================
@router.post("/reports", response_model=schemas.ReportResponse)
def generate_report(
    req: schemas.ReportCreateRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        return ReportService.generate_report(db, current_user.id, req.birth_details_id, req.report_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reports", response_model=List[schemas.ReportResponse])
def list_reports(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return ReportRepository.list_by_user(db, user_id=current_user.id)

@router.get("/reports/{report_id}", response_model=schemas.ReportResponse)
def get_report(
    report_id: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    report = ReportRepository.get_by_id(db, report_id)
    if not report or report.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

# ==========================================
# CHAT ENDPOINTS
# ==========================================
@router.post("/chat", response_model=schemas.ChatSessionResponse)
def create_chat_session(
    req: schemas.ChatSessionCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    details = BirthDetailsRepository.get_by_id(db, req.birth_details_id)
    if not details or details.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Birth details profile not found")
        
    session = models.ChatSession(
        user_id=current_user.id,
        birth_details_id=req.birth_details_id,
        title=req.title
    )
    return ChatSessionRepository.create(db, session)

@router.get("/chat", response_model=List[schemas.ChatSessionResponse])
def list_chat_sessions(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return ChatSessionRepository.list_by_user(db, user_id=current_user.id)

@router.post("/chat/{session_id}/messages", response_model=schemas.ChatMessageResponse)
def send_message(
    session_id: str,
    msg_in: schemas.ChatMessageCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        return ChatService.handle_message(db, current_user.id, session_id, msg_in.content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/chat/{session_id}/messages", response_model=List[schemas.ChatMessageResponse])
def list_messages(
    session_id: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    session = ChatSessionRepository.get_by_id(db, session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return ChatSessionRepository.list_messages(db, session_id)

# ==========================================
# CHART CALCULATION ENDPOINT
# ==========================================
@router.post("/chart/calculate", response_model=schemas.ChartCalculationResponse)
def calculate_chart(request: schemas.ChartCalculationRequest):
    """Calculate Vedic birth chart using Swiss Ephemeris."""
    try:
        result = calculate_birth_chart(
            name=request.name,
            birth_date=request.birthDate,
            birth_time=request.birthTime,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chart calculation failed: {str(e)}")

# ==========================================
# EXPLAINABILITY ENDPOINTS
# ==========================================
@router.post("/explainability", response_model=Dict[str, schemas.DomainResultResponse])
def explain_chart(
    req: schemas.ExplainabilityRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Generate deterministic explainability scores for all life domains."""
    try:
        return ExplainabilityService.evaluate_chart(db, req.birth_details_id, req.domains)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
