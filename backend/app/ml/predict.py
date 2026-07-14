from pathlib import Path
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


class DelayPredictor:
    def __init__(self, model_path=None):
        self.model_path = Path(model_path) if model_path else Path(__file__).with_name("model.pkl")
        self.model = None
        self._load_or_train_model()

    def _load_or_train_model(self):
        if self.model_path.exists():
            self.model = joblib.load(self.model_path)
            return

        print(f"Model file not found at {self.model_path}. Training a fallback model...")
        self.model = self._train_model()
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, self.model_path)

    def _train_model(self):
        base_path = Path(__file__).resolve().parents[2]
        data_path = base_path / "data" / "clean_supply_chain.csv"

        if not data_path.exists():
            raise FileNotFoundError(f"Training data not found: {data_path}")

        df = pd.read_csv(data_path)

        target = "Late_delivery_risk"
        features = [
            "Shipping Mode",
            "Category Name",
            "Market",
            "Order Region",
            "Order Item Quantity",
            "Product Price",
            "Sales",
            "Days for shipping (real)",
            "Days for shipment (scheduled)"
        ]

        X = df[features]
        y = df[target]

        categorical_features = ["Shipping Mode", "Category Name", "Market", "Order Region"]
        numeric_features = [
            "Order Item Quantity",
            "Product Price",
            "Sales",
            "Days for shipping (real)",
            "Days for shipment (scheduled)"
        ]

        categorical_transformer = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ])

        numeric_transformer = Pipeline([
            ("imputer", SimpleImputer(strategy="median"))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", categorical_transformer, categorical_features),
                ("num", numeric_transformer, numeric_features)
            ]
        )

        model = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
        ])

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Fallback model trained with accuracy: {accuracy:.4f}")

        return model

    def predict(self, data: dict):
        if self.model is None:
            self._load_or_train_model()

        df = pd.DataFrame([data])
        prediction = self.model.predict(df)[0]
        probability = self.model.predict_proba(df)[0]

        confidence = round(max(probability) * 100, 2)

        return {
            "late_delivery_risk": int(prediction),
            "confidence": confidence
        }


predictor = DelayPredictor()