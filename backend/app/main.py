from fastapi import FastAPI
from app.database import Base, engine
from app.models import Prediction
from app.api.prediction import router as prediction_router
from app.api.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Supply Chain Risk Intelligence API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

app.include_router(prediction_router)
app.include_router(dashboard_router)


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