from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.api.prediction import router as prediction_router
from app.api.dashboard import router as dashboard_router

app = FastAPI(
    title="Supply Chain Risk Intelligence API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router)
app.include_router(dashboard_router)


@app.on_event("startup")
def startup_event():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        print(f"Warning: database initialization skipped: {exc}")


@app.get("/")
def home():
    return {
        "message": "Welcome to the Supply Chain Risk Intelligence API",
        "status": "Running Successfully 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }