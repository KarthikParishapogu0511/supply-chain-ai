from pathlib import Path
import joblib
import pandas as pd


class DelayPredictor:
    def __init__(self):
        model_path = Path(__file__).parent / "model.pkl"
        self.model = joblib.load(model_path)

    def predict(self, data: dict):

        df = pd.DataFrame([data])

        prediction = self.model.predict(df)[0]
        probability = self.model.predict_proba(df)[0]

        confidence = round(max(probability) * 100, 2)

        return {
            "late_delivery_risk": int(prediction),
            "confidence": confidence
        }


predictor = DelayPredictor()