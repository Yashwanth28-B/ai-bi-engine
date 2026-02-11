import pandas as pd

def clean_data(df):
    # Fill missing values
    df = df.fillna("Unknown")

    # Normalize text
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.lower().str.strip()

    # Normalize dates
    for col in ["start date", "end date", "close date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    return df
