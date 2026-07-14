import pandas as pd

# Load dataset
df = pd.read_csv("data/DataCoSupplyChainDataset.csv", encoding="latin1")

print("=" * 80)
print("Shape")
print(df.shape)

print("\n" + "=" * 80)
print("Columns")
print(df.columns.tolist())

print("\n" + "=" * 80)
print("First 5 Rows")
print(df.head())

print("\n" + "=" * 80)
print("Missing Values")
print(df.isnull().sum())

print("\n" + "=" * 80)
print("Data Types")
print(df.dtypes)