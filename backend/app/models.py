from sqlalchemy import Column, Integer, Float, String
from app.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    shipping_mode = Column(String)
    category_name = Column(String)
    market = Column(String)
    order_region = Column(String)

    quantity = Column(Integer)
    product_price = Column(Float)
    sales = Column(Float)

    real_shipping_days = Column(Integer)
    scheduled_shipping_days = Column(Integer)

    predicted_risk = Column(Integer)
    confidence = Column(Float)