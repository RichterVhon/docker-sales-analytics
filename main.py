#!/usr/bin/env python3
"""
🚀 MAIN ENTRY POINT - Containerized Data Analytics App
Run: python main.py
"""

print("🚀 Starting Data Analytics Pipeline...")
print("=" * 50)

from src.data_loader import load_dataset
from src.analyzer import analyze_data
from src.visualizer import create_visualizations

# Step 1: Load data
print("📂 Step 1: Loading dataset...")
df = load_dataset('dataset.csv')

# Step 2: Analyze
print("\n🔬 Step 2: Statistical analysis...")
analysis = analyze_data(df)

# Step 3: Visualize (creates 5+ graphs)
print("\n🎨 Step 3: Creating visualizations...")
create_visualizations(df, analysis)

print("\n🎉 ANALYSIS COMPLETE!")
print("📁 Check 'graphs/' folder for your 5+ beautiful charts!")