import pandas as pd
import os

def load_dataset(csv_path='dataset.csv'):
    """Load CSV and do basic cleaning"""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found!")
    
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"📊 Columns: {list(df.columns)}")
    print(f"🔍 First 3 rows:\n{df.head(3)}")
    
    # Basic cleaning
    df = df.dropna()  # Remove missing values
    df = df.drop_duplicates()  # Remove duplicates
    
    return df

if __name__ == "__main__":
    # Test it
    data = load_dataset()