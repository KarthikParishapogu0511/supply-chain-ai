import sys
import tempfile
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.ml.predict import DelayPredictor


class DelayPredictorTests(unittest.TestCase):
    def test_missing_model_file_triggers_fallback_or_training(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = Path(tmpdir) / "model.pkl"
            predictor = DelayPredictor(model_path=model_path)

            result = predictor.predict(
                {
                    "Shipping Mode": "Express",
                    "Category Name": "Office Supplies",
                    "Market": "US",
                    "Order Region": "West",
                    "Order Item Quantity": 5,
                    "Product Price": 12.5,
                    "Sales": 62.5,
                    "Days for shipping (real)": 3,
                    "Days for shipment (scheduled)": 2,
                }
            )

            self.assertIn("late_delivery_risk", result)
            self.assertIn("confidence", result)
            self.assertTrue(0 <= result["late_delivery_risk"] <= 1)
            self.assertTrue(0 <= result["confidence"] <= 100)


if __name__ == "__main__":
    unittest.main()
