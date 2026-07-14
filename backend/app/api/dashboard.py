from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Prediction

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):

    total_predictions = db.query(Prediction).count()

    late_predictions = db.query(Prediction).filter(
        Prediction.predicted_risk == 1
    ).count()

    ontime_predictions = db.query(Prediction).filter(
        Prediction.predicted_risk == 0
    ).count()

    average_confidence = db.query(
        func.avg(Prediction.confidence)
    ).scalar()

    return {
        "total_predictions": total_predictions,
        "late_deliveries": late_predictions,
        "on_time_deliveries": ontime_predictions,
        "average_confidence": round(average_confidence or 0, 2)
    }