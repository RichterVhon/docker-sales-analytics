import pandas as pd
import numpy as np
from scipy import stats

def analyze_data(df):
    """Generate key statistics"""
    print("\n📈 STATISTICS ANALYSIS")
    
    analysis = {
        'total_rows': len(df),
        'numeric_columns': [],
        'categorical_columns': [],
        'summary_stats': {}
    }
    
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            analysis['numeric_columns'].append(col)
            analysis['summary_stats'][col] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max()
            }
        else:
            analysis['categorical_columns'].append(col)
    
    print(f"Numeric columns: {analysis['numeric_columns']}")
    print(f"Categorical columns: {analysis['categorical_columns']}")
    
    return analysis

if __name__ == "__main__":
    from data_loader import load_dataset
    df = load_dataset()
    stats = analyze_data(df)