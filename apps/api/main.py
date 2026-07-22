import os
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import database
import models
from routes import router

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("vedai.api")

# Auto-create tables if they don't exist (simplifies local setup)
try:
    logger.info("Initializing database tables...")
    models.Base.metadata.create_all(bind=database.engine)
    logger.info("Database tables initialized successfully.")
except Exception as e:
    logger.exception("Failed to initialize database tables:")

app = FastAPI(
    title="VedAI API",
    description="Ancient Wisdom. Powered by AI. Astrological report engine & calculator.",
    version="1.0.0"
)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the web domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files to serve generated PDFs
static_reports_dir = database.settings.PDF_OUTPUT_DIR
os.makedirs(static_reports_dir, exist_ok=True)
app.mount("/static/reports", StaticFiles(directory=static_reports_dir), name="static")

# Include Router
app.include_router(router)

@app.get("/api/health")
def health(db: Session = Depends(database.get_db)):
    """Health check endpoint validating database connectivity."""
    try:
        # Simple query to verify connection
        db.execute(models.text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = "unhealthy"
        
    return {
        "status": "online",
        "database": db_status,
        "ayanamsha_system": "Lahiri (Sidereal)",
        "timestamp": models.datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
