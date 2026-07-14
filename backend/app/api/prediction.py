from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.ml.predict import predictor
from app.database import get_db
from app.models import Prediction

router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"]
)


class PredictionRequest(BaseModel):
    Shipping_Mode: str
    Category_Name: str
    Market: str
    Order_Region: str
    Order_Item_Quantity: int
    Product_Price: float
    Sales: float
    Days_for_shipping_real: int
    Days_for_shipment_scheduled: int


@router.post("/predict-delay")
def predict_delay(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):

    data = {
        "Shipping Mode": request.Shipping_Mode,
        "Category Name": request.Category_Name,
        "Market": request.Market,
        "Order Region": request.Order_Region,
        "Order Item Quantity": request.Order_Item_Quantity,
        "Product Price": request.Product_Price,
        "Sales": request.Sales,
        "Days for shipping (real)": request.Days_for_shipping_real,
        "Days for shipment (scheduled)": request.Days_for_shipment_scheduled
    }

    result = predictor.predict(data)

    prediction = Prediction(
        shipping_mode=request.Shipping_Mode,
        category_name=request.Category_Name,
        market=request.Market,
        order_region=request.Order_Region,
        quantity=request.Order_Item_Quantity,
        product_price=request.Product_Price,
        sales=request.Sales,
        real_shipping_days=request.Days_for_shipping_real,
        scheduled_shipping_days=request.Days_for_shipment_scheduled,
        predicted_risk=result["late_delivery_risk"],
        confidence=result["confidence"]
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return result 

@router.get("/history")
def prediction_history(db: Session = Depends(get_db)):

    predictions = db.query(Prediction).order_by(
        Prediction.id.desc()
    ).all()

    return [
        {
            "id": p.id,
            "shipping_mode": p.shipping_mode,
            "category_name": p.category_name,
            "market": p.market,
            "order_region": p.order_region,
            "predicted_risk": p.predicted_risk,
            "confidence": p.confidence
        }
        for p in predictions
    ]