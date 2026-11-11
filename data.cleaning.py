import pandas as pd
import numpy as np

# 1. Load the uploaded dataset
file_name = next(iter(uploaded))
df = pd.read_csv(file_name)

print("Original dataset shape:", df.shape)

# 2. Remove extra spaces from column names
df.columns = df.columns.str.strip()

# 3. Remove extra spaces from text values
for col in df.select_dtypes(include=["object"]).columns:
    df[col] = df[col].str.strip()

# 4. Convert Datetime into proper date format
df["Datetime"] = pd.to_datetime(
    df["Datetime"], errors="coerce"
)

# 5. Convert pollution and AQI columns to numeric values
numeric_cols = [
    "PM2.5", "PM10", "NO", "NO2", "NOx", "NH3",
    "CO", "SO2", "O3", "Benzene", "Toluene",
    "Xylene", "AQI"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# 6. Replace infinite values with missing values
df = df.replace([np.inf, -np.inf], np.nan)

# 7. Remove completely duplicate rows
df = df.drop_duplicates()

# 8. Remove rows without essential information
df = df.dropna(subset=["City", "Datetime"])

# 9. Fill missing numeric values using each city's median
for col in numeric_cols:
    if col in df.columns:
        df[col] = df.groupby("City")[col].transform(
            lambda x: x.fillna(x.median())
        )

# 10. Fill remaining numeric missing values using overall median
for col in numeric_cols:
    if col in df.columns and df[col].isna().any():
        df[col] = df[col].fillna(df[col].median())

# 11. Fill missing text categories with "Unknown"
text_cols = df.select_dtypes(include=["object"]).columns

for col in text_cols:
    df[col] = df[col].fillna("Unknown")

# 12. Sort by city and date
df = df.sort_values(
    by=["City", "Datetime"]
).reset_index(drop=True)

# 13. Format date consistently
df["Datetime"] = df["Datetime"].dt.strftime("%Y-%m-%d")

# 14. Save the cleaned dataset
output_file = "city_day_cleaned.csv"
df.to_csv(output_file, index=False)

# 15. Display cleaning report
print("\nDATA CLEANING COMPLETED")
print("Final rows:", df.shape[0])
print("Final columns:", df.shape[1])
print("Duplicate rows:", df.duplicated().sum())
print("Missing values:", df.isna().sum().sum())

print("\nCleaned dataset preview:")
display(df.head(10))

print("\nColumn information:")
df.info()