from pathlib import Path
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier


BASE_PATH = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_PATH / "data" / "clean_supply_chain.csv"
MODEL_PATH = BASE_PATH / "app" / "ml" / "model.pkl"


def main():
    print("Loading cleaned dataset...")
    df = pd.read_csv(DATA_PATH)

    target = "Late_delivery_risk"

    # Features we'll use
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

    categorical_features = [
        "Shipping Mode",
        "Category Name",
        "Market",
        "Order Region"
    ]

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
        ("classifier", RandomForestClassifier(
            n_estimators=100,
            random_state=42
        ))
    ])

    print("Splitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    print("Training model...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("\n==============================")
    print(f"Accuracy: {accuracy:.4f}")
    print("==============================")

    print(classification_report(y_test, predictions))

    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved to:\n{MODEL_PATH}")


if __name__ == "__main__":
    main()