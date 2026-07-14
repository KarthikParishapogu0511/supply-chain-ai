import pandas as pd
from pathlib import Path


class DataPreprocessor:
    def __init__(self):
        # Project root -> backend/
        self.base_path = Path(__file__).resolve().parents[2]

        self.input_file = self.base_path / "data" / "DataCoSupplyChainDataset.csv"
        self.output_file = self.base_path / "data" / "clean_supply_chain.csv"

    def load_data(self):
        print("Loading dataset...")
        df = pd.read_csv(self.input_file, encoding="latin1")
        print(f"Dataset loaded successfully: {df.shape}")
        return df

    def clean_data(self, df):
        print("Cleaning dataset...")

        # Drop unnecessary columns
        columns_to_drop = [
            "Customer Password",
            "Customer Email",
            "Product Description",
            "Product Image",
            "Customer Street",
            "Order Zipcode"
        ]

        existing_columns = [col for col in columns_to_drop if col in df.columns]
        df.drop(columns=existing_columns, inplace=True)

        # Fill missing last names
        if "Customer Lname" in df.columns:
            df["Customer Lname"] = df["Customer Lname"].fillna("Unknown")

        # Fill customer zipcode
        if "Customer Zipcode" in df.columns:
            df["Customer Zipcode"] = df["Customer Zipcode"].fillna(0)

        # Convert dates
        df["order date (DateOrders)"] = pd.to_datetime(
            df["order date (DateOrders)"],
            errors="coerce"
        )

        df["shipping date (DateOrders)"] = pd.to_datetime(
            df["shipping date (DateOrders)"],
            errors="coerce"
        )

        # Feature Engineering
        df["Order Year"] = df["order date (DateOrders)"].dt.year
        df["Order Month"] = df["order date (DateOrders)"].dt.month
        df["Order Day"] = df["order date (DateOrders)"].dt.day
        df["Order Weekday"] = df["order date (DateOrders)"].dt.day_name()

        # Remove duplicate rows
        df.drop_duplicates(inplace=True)

        print(f"Dataset after cleaning: {df.shape}")

        return df

    def save_data(self, df):
        df.to_csv(self.output_file, index=False)
        print(f"Clean dataset saved to:\n{self.output_file}")


def main():
    processor = DataPreprocessor()

    df = processor.load_data()
    df = processor.clean_data(df)
    processor.save_data(df)

    print("\nData preprocessing completed successfully!")


if __name__ == "__main__":
    main()