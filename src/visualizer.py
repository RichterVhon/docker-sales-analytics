import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import time
from datetime import datetime


def create_visualizations(df, analysis, output_dir='output'):
    """🚀 8-GRAPH BUSINESS INTELLIGENCE SUITE"""
    
    # 🕒 1. SETUP DIRECTORY
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_output_dir = os.path.join(output_dir, f"full_analysis_{timestamp}")
    os.makedirs(new_output_dir, exist_ok=True)
    
    print(f"\n📁 Initializing 7-Graph Analysis: '{new_output_dir}'")
    
    # PRO THEME
    sns.set_palette("husl")
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_context("notebook", font_scale=1.2)
    
    # 🧹 DATA CLEANING
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    numeric_cols = ['Sales', 'Discount', 'Quantity', 'SatisfactionScore', 'Return']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # 🔥 1. REGIONAL PERFORMANCE (Sales vs Volume)
    plt.figure(figsize=(15, 10))
    region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    region_qty = df.groupby('Region')['Quantity'].sum()
    x = np.arange(len(region_sales))
    width = 0.3
    plt.subplot(2, 1, 1)
    plt.bar(x - width/2, region_sales.values, width, label='Total Sales ($)', color='darkblue')
    plt.bar(x + width/2, region_qty.values, width, label='Total Quantity', color='darkgreen')
    plt.title('🏆 REGIONAL PERFORMANCE: Sales vs. Volume', fontweight='bold', fontsize=16)
    plt.xticks(x, region_sales.index); plt.legend()
    avg_order = region_sales / df.groupby('Region').size()
    plt.subplot(2, 1, 2)
    bars = plt.bar(region_sales.index, avg_order.values, color='coral', edgecolor='darkred')
    plt.title('💰 AVERAGE ORDER VALUE BY REGION', fontweight='bold', fontsize=16)
    for bar, val in zip(bars, avg_order.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'${val:,.0f}', ha='center', fontweight='bold')
    plt.tight_layout(); plt.savefig(f'{new_output_dir}/1_regional_performance.png', dpi=300); plt.close()

    # 🔥 2. CHANNEL EFFICIENCY (Revenue/Satisfaction/Returns)
    plt.figure(figsize=(14, 10))
    channel_metrics = df.groupby('SalesChannel').agg({'Sales': 'sum', 'SatisfactionScore': 'mean', 'Return': 'mean'}).round(2)
    x_ch = np.arange(len(channel_metrics))
    plt.subplot(2, 2, 1); plt.bar(x_ch, channel_metrics['Sales'], color='steelblue'); plt.title('💵 TOTAL REVENUE')
    plt.xticks(x_ch, channel_metrics.index)
    plt.subplot(2, 2, 2); plt.bar(x_ch, channel_metrics['SatisfactionScore'], color='gold'); plt.title('⭐ AVG SATISFACTION')
    plt.xticks(x_ch, channel_metrics.index)
    plt.subplot(2, 2, 3); plt.bar(x_ch, channel_metrics['Return'], color='red'); plt.title('⚠️ RETURN RATE')
    plt.xticks(x_ch, channel_metrics.index)
    plt.tight_layout(); plt.savefig(f'{new_output_dir}/2_channel_efficiency.png', dpi=300); plt.close()

    # 🔥 3. PAYMENT METHOD STRATEGY (Market Share)
    plt.figure(figsize=(14, 8))
    pay_sales = df.groupby('PaymentMethod')['Sales'].sum()
    plt.subplot(1, 2, 1)
    plt.pie(pay_sales, labels=pay_sales.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    plt.title('💳 PAYMENT MARKET SHARE')
    plt.subplot(1, 2, 2)
    df.groupby('PaymentMethod')['Sales'].mean().plot(kind='bar', color='purple', alpha=0.8)
    plt.title('💰 AVG TRANSACTION BY PAYMENT')
    plt.tight_layout(); plt.savefig(f'{new_output_dir}/3_payment_strategy.png', dpi=300); plt.close()

    # 🔥 4. SATISFACTION DISTRIBUTION (Violin Plot)
    plt.figure(figsize=(14, 8))
    sns.violinplot(data=df, x='CustomerType', y='SatisfactionScore', hue='SalesChannel', split=True, inner="quartile", palette="Set2")
    plt.title('🎻 SATISFACTION DENSITY: Segment vs. Channel', fontweight='bold', fontsize=16)
    plt.savefig(f'{new_output_dir}/4_satisfaction_distribution.png', dpi=300); plt.close()

    # 🔥 5. CORRELATION MATRIX (Drivers of Revenue)
    plt.figure(figsize=(10, 8))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", mask=np.triu(np.ones_like(corr, dtype=bool)))
    plt.title('🔬 STATISTICAL RELATIONSHIPS', fontweight='bold')
    plt.savefig(f'{new_output_dir}/5_correlation_matrix.png', dpi=300); plt.close()

    # 🔥 6. REVENUE PARETO (80/20 Rule)
    plt.figure(figsize=(14, 8))
    prod_sales = df.groupby('ProductCategory')['Sales'].sum().sort_values(ascending=False)
    cum_perc = 100 * prod_sales.cumsum() / prod_sales.sum()
    fig, ax1 = plt.subplots(figsize=(12, 7))
    ax1.bar(prod_sales.index, prod_sales.values, color='teal', alpha=0.7)
    ax2 = ax1.twinx()
    ax2.plot(prod_sales.index, cum_perc.values, color='crimson', marker='o')
    ax2.axhline(80, color='orange', linestyle='--')
    plt.title('🏆 PRODUCT PARETO ANALYSIS (80/20 Rule)', fontweight='bold')
    plt.savefig(f'{new_output_dir}/6_pareto_analysis.png', dpi=300); plt.close()

# 🔥 8. TRANSACTION SIZE vs. RETURN VOLUME
    # Histogram = "What is our most common sale amount?"
    # Pie Chart = "How much of our business is actually being returned?"
    plt.figure(figsize=(16, 8))
    
    # Left: Histogram of Transaction Sizes
    plt.subplot(1, 2, 1)
    sns.histplot(df['Sales'], bins=20, kde=True, color='teal', edgecolor='black')
    plt.axvline(df['Sales'].median(), color='red', linestyle='--', label=f"Median Sale: ${df['Sales'].median():,.2f}")
    plt.title('📊 TRANSACTION SIZE DISTRIBUTION\n(Most Common Sales Values)', fontweight='bold', fontsize=14)
    plt.xlabel('Sales Amount ($)')
    plt.ylabel('Number of Transactions')
    plt.legend()

    # Right: Pie Chart of Returns
    plt.subplot(1, 2, 2)
    return_status = df['Return'].value_counts().rename(index={0: 'Kept', 1: 'Returned'})
    plt.pie(return_status, labels=return_status.index, autopct='%1.1f%%', 
            colors=['#66b3ff','#ff9999'], startangle=90, explode=(0.05, 0))
    plt.title('🍕 OVERALL RETURN RATE\n(Logistics Health)', fontweight='bold', fontsize=14)
    
    plt.tight_layout()
    plt.savefig(f'{new_output_dir}/8_sales_return_summary.png', dpi=300)
    plt.close()
    
    print(f"✅ 8. Transaction & Return Summary generated.")
    print(f"\n🎉 ANALYSIS COMPLETE! Folder: '{new_output_dir}'")
    print("⏲️ Container will stay active for 30 minutes for file inspection...")

    # Keep the container alive for 1800 seconds (30 mins)
    time.sleep(1800) 
    return new_output_dir