import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def create_visualizations(df, analysis, output_dir='output'):
    """🚀 SMART SALES ANALYTICS - 5 MEANINGFUL BUSINESS INSIGHTS"""
    
    # 🕒 CREATE BASE OUTPUT DIR IF MISSING
    # This ensures the 'output' folder exists before we try to put timestamps in it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 🕒 TIMESTAMPED SUB-FOLDER
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_output_dir = os.path.join(output_dir, f"graphs_{timestamp}")
    os.makedirs(new_output_dir, exist_ok=True)
    
    print(f"\n📁 New analysis session: '{new_output_dir}'")
    
    # PRO STYLE
    sns.set_palette("husl")
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_context("notebook", font_scale=1.3)
    
    # CLEAN DATA
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df['SatisfactionScore'] = pd.to_numeric(df['SatisfactionScore'], errors='coerce')
    
    # 🔥 GRAPH 1: REGIONAL REVENUE BATTLE
    plt.figure(figsize=(15, 10))
    region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    region_qty = df.groupby('Region')['Quantity'].sum()
    region_orders = df.groupby('Region').size()
    
    x = np.arange(len(region_sales))
    width = 0.25
    
    plt.subplot(2, 1, 1)
    plt.bar(x - width, region_sales.values, width, label='Total Sales', alpha=0.9, color='darkblue')
    plt.bar(x, region_qty.values, width, label='Total Quantity', alpha=0.9, color='darkgreen')
    plt.title('🏆 REGIONAL PERFORMANCE\nSales vs Volume', fontweight='bold', fontsize=18, pad=20)
    plt.ylabel('Amount', fontsize=14)
    plt.xticks(x, region_sales.index)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    avg_order = region_sales / region_orders
    plt.subplot(2, 1, 2)
    bars = plt.bar(region_sales.index, avg_order.values, alpha=0.9, color='coral', edgecolor='darkred')
    plt.title('💰 AVERAGE ORDER VALUE BY REGION', fontweight='bold', fontsize=18, pad=20)
    plt.ylabel('Avg Order ($)')
    
    for bar, val in zip(bars, avg_order.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(avg_order)*0.01,
                f'${val:,.0f}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{new_output_dir}/1_regional_battle.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 1. Regional Revenue Battle")

    # 🔥 GRAPH 2: CATEGORY PROFITABILITY MATRIX
    plt.figure(figsize=(15, 12))
    cat_metrics = df.groupby('ProductCategory').agg({
        'Sales': ['sum', 'mean', 'count'],
        'Quantity': 'sum',
        'Return': 'mean'
    }).round(2)
    cat_metrics.columns = ['TotalSales', 'AvgSales', 'Orders', 'TotalQty', 'ReturnRate']
    cat_metrics['RevenuePerOrder'] = cat_metrics['TotalSales'] / cat_metrics['Orders']
    
    plt.subplot(2, 2, 1)
    metrics_subset = cat_metrics[['RevenuePerOrder', 'ReturnRate']].T
    sns.heatmap(metrics_subset, annot=True, cmap='RdYlGn', fmt='.1f', cbar_kws={'label': 'Value'})
    plt.title('🔥 CATEGORY PERFORMANCE MATRIX', fontweight='bold', fontsize=14)
    
    plt.subplot(2, 2, 2)
    cat_metrics['TotalSales'].sort_values(ascending=False)[:6].plot(kind='barh', color='teal', alpha=0.9)
    plt.title('🏅 TOP REVENUE GENERATORS')
    
    plt.subplot(2, 2, 3)
    cat_metrics.nsmallest(4, 'RevenuePerOrder')['RevenuePerOrder'].plot(kind='barh', color='orange', alpha=0.9)
    plt.title('⚠️ LOWEST AOV CATEGORIES')
    
    plt.subplot(2, 2, 4)
    cat_metrics['ReturnRate'].sort_values(ascending=False).plot(kind='barh', color='red', alpha=0.8)
    plt.title('🚨 HIGHEST RETURN RISK')
    
    plt.tight_layout()
    plt.savefig(f'{new_output_dir}/2_category_matrix.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 2. Category Profitability")

    # 🔥 GRAPH 3: CHANNEL EFFICIENCY COMPARISON
    plt.figure(figsize=(14, 10))
    channel_metrics = df.groupby('SalesChannel').agg({
        'Sales': ['sum', 'mean'],
        'Quantity': 'sum',
        'Return': 'mean',
        'SatisfactionScore': 'mean'
    }).round(2)
    channel_metrics.columns = ['TotalSales', 'AvgSales', 'TotalQty', 'ReturnRate', 'AvgSatisfaction']
    
    x = np.arange(len(channel_metrics))
    
    plt.subplot(2, 2, 1); plt.bar(x, channel_metrics['TotalSales'], color='steelblue')
    plt.title('💵 TOTAL REVENUE'); plt.xticks(x, channel_metrics.index)
    
    plt.subplot(2, 2, 2); plt.bar(x, channel_metrics['AvgSatisfaction'], color='gold')
    plt.title('⭐ SATISFACTION'); plt.xticks(x, channel_metrics.index)
    
    plt.subplot(2, 2, 3); plt.bar(x, channel_metrics['ReturnRate'], color='red')
    plt.title('⚠️ RETURN RATE'); plt.xticks(x, channel_metrics.index)
    
    plt.subplot(2, 2, 4); plt.bar(x, channel_metrics['AvgSales'], color='green')
    plt.title('💰 AVG SALE'); plt.xticks(x, channel_metrics.index)
    
    plt.tight_layout()
    plt.savefig(f'{new_output_dir}/3_channel_efficiency.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 3. Channel Efficiency")

    # 🔥 GRAPH 4: CUSTOMER LIFETIME VALUE
    plt.figure(figsize=(14, 10))
    cust_metrics = df.groupby('CustomerType').agg({
        'Sales': ['sum', 'mean', 'count'],
        'Quantity': 'sum',
        'SatisfactionScore': 'mean',
        'Return': 'mean'
    }).round(2)
    cust_metrics.columns = ['TotalSales', 'AvgSales', 'Orders', 'TotalQty', 'AvgSatisfaction', 'ReturnRate']
    cust_metrics['LifetimeValue'] = cust_metrics['TotalSales'] / cust_metrics['Orders']
    
    plt.subplot(2, 1, 1)
    x_cust = np.arange(len(cust_metrics))
    bars = plt.bar(x_cust, cust_metrics['LifetimeValue'], color=['gold' if t == 'VIP' else 'silver' for t in cust_metrics.index])
    plt.title('💎 CUSTOMER LIFETIME VALUE', fontweight='bold', fontsize=16)
    plt.xticks(x_cust, cust_metrics.index)
    
    plt.subplot(2, 1, 2)
    sns.heatmap(cust_metrics[['AvgSatisfaction', 'ReturnRate']].T, annot=True, cmap='RdYlGn')
    
    plt.tight_layout()
    plt.savefig(f'{new_output_dir}/4_customer_lifetime.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 4. Customer Lifetime Value")

    # 🔥 GRAPH 5: PAYMENT METHOD INSIGHTS
    plt.figure(figsize=(14, 10))
    payment_metrics = df.groupby('PaymentMethod').agg({'Sales': ['sum', 'mean'], 'Return': 'mean'}).round(2)
    payment_metrics.columns = ['TotalSales', 'AvgSales', 'ReturnRate']
    
    plt.subplot(2, 2, 1)
    plt.pie(payment_metrics['TotalSales'], labels=payment_metrics.index, autopct='%1.1f%%')
    plt.title('💳 MARKET SHARE')
    
    plt.subplot(2, 2, 2)
    plt.bar(payment_metrics.index, payment_metrics['AvgSales'], color='purple')
    plt.title('💰 AVG SALE')
    
    plt.subplot(2, 2, 3)
    plt.bar(payment_metrics.index, payment_metrics['ReturnRate'], color='red')
    plt.title('⚠️ RETURN RATE')
    
    plt.subplot(2, 2, 4)
    plt.scatter(payment_metrics['TotalSales'], payment_metrics['ReturnRate'], s=payment_metrics['TotalSales']/1000, alpha=0.7, c='orange')
    plt.title('🎯 SIZE vs RISK')
    
    plt.tight_layout()
    plt.savefig(f'{new_output_dir}/5_payment_insights.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 5. Payment Method Strategy")

    print(f"\n🎉 ANALYSIS COMPLETE! Folder: '{new_output_dir}'")
    return new_output_dir