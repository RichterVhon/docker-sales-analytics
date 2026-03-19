import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def create_visualizations(df, analysis, output_dir='graphs'):
    """🚀 SMART SALES ANALYTICS - 5 MEANINGFUL BUSINESS INSIGHTS"""
    
    # 🕒 TIMESTAMP FOLDER
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_output_dir = f"{output_dir}_{timestamp}"
    os.makedirs(new_output_dir, exist_ok=True)
    
    print(f"\n📁 New analysis: '{new_output_dir}'")
    
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
    
    # 🔥 GRAPH 1: REGIONAL REVENUE BATTLE (MOST IMPORTANT)
    plt.figure(figsize=(15, 10))
    
    # Total sales by region
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
    
    # Avg order value
    avg_order = region_sales / region_orders
    plt.subplot(2, 1, 2)
    bars = plt.bar(region_sales.index, avg_order.values, alpha=0.9, color='coral', edgecolor='darkred')
    plt.title('💰 AVERAGE ORDER VALUE BY REGION', fontweight='bold', fontsize=18, pad=20)
    plt.ylabel('Avg Order ($)')
    plt.xticks(rotation=0)
    
    # Value labels
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
    
    # Heatmap of key metrics
    plt.subplot(2, 2, 1)
    metrics_subset = cat_metrics[['RevenuePerOrder', 'ReturnRate']].T
    sns.heatmap(metrics_subset, annot=True, cmap='RdYlGn', fmt='.1f', cbar_kws={'label': 'Value'})
    plt.title('🔥 CATEGORY PERFORMANCE MATRIX\n(Green=Good, Red=Bad)', fontweight='bold', fontsize=14)
    
    # Bar chart ranking
    plt.subplot(2, 2, 2)
    top_categories = cat_metrics['TotalSales'].sort_values(ascending=False)[:6]
    top_categories.plot(kind='barh', color='teal', alpha=0.9)
    plt.title('🏅 TOP REVENUE GENERATORS')
    plt.xlabel('Total Sales ($)')
    
    plt.subplot(2, 2, 3)
    low_performers = cat_metrics.nsmallest(4, 'RevenuePerOrder')['RevenuePerOrder']
    low_performers.plot(kind='barh', color='orange', alpha=0.9)
    plt.title('⚠️ LOWEST AOV CATEGORIES')
    plt.xlabel('Avg Order ($)')
    
    plt.subplot(2, 2, 4)
    returns = cat_metrics['ReturnRate'].sort_values(ascending=False)
    returns.plot(kind='barh', color='red', alpha=0.8)
    plt.title('🚨 HIGHEST RETURN RISK')
    plt.xlabel('Return Rate')
    
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
    
    plt.subplot(2, 2, 1)
    plt.bar(x, channel_metrics['TotalSales'], alpha=0.9, color='steelblue')
    plt.title('💵 TOTAL REVENUE BY CHANNEL', fontweight='bold', fontsize=14)
    plt.ylabel('Total Sales ($)')
    plt.xticks(x, channel_metrics.index, rotation=0)
    
    plt.subplot(2, 2, 2)
    plt.bar(x, channel_metrics['AvgSatisfaction'], alpha=0.9, color='gold')
    plt.title('⭐ SATISFACTION BY CHANNEL', fontweight='bold', fontsize=14)
    plt.ylabel('Avg Score')
    plt.xticks(x, channel_metrics.index, rotation=0)
    
    plt.subplot(2, 2, 3)
    plt.bar(x, channel_metrics['ReturnRate'], alpha=0.9, color='red')
    plt.title('⚠️ RETURN RATE BY CHANNEL', fontweight='bold', fontsize=14)
    plt.ylabel('Return Rate')
    plt.xticks(x, channel_metrics.index, rotation=0)
    
    plt.subplot(2, 2, 4)
    plt.bar(x, channel_metrics['AvgSales'], alpha=0.9, color='green')
    plt.title('💰 AVERAGE SALE BY CHANNEL', fontweight='bold', fontsize=14)
    plt.ylabel('Avg Sale ($)')
    plt.xticks(x, channel_metrics.index, rotation=0)
    
    plt.tight_layout()
    plt.savefig(f'{new_output_dir}/3_channel_efficiency.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 3. Channel Efficiency")

    # 🔥 GRAPH 4: CUSTOMER LIFETIME VALUE
    plt.figure(figsize=(14, 10))
    
    # Customer type analysis
    cust_metrics = df.groupby('CustomerType').agg({
        'Sales': ['sum', 'mean', 'count'],
        'Quantity': 'sum',
        'SatisfactionScore': 'mean',
        'Return': 'mean'
    }).round(2)
    cust_metrics.columns = ['TotalSales', 'AvgSales', 'Orders', 'TotalQty', 'AvgSatisfaction', 'ReturnRate']
    cust_metrics['LifetimeValue'] = cust_metrics['TotalSales'] / cust_metrics['Orders']
    
    x_cust = np.arange(len(cust_metrics))
    
    plt.subplot(2, 1, 1)
    bars = plt.bar(x_cust, cust_metrics['LifetimeValue'], alpha=0.9, 
                   color=['gold' if t == 'VIP' else 'silver' for t in cust_metrics.index])
    plt.title('💎 CUSTOMER LIFETIME VALUE\n(Avg Revenue per Order)', fontweight='bold', fontsize=16, pad=20)
    plt.ylabel('Lifetime Value ($)')
    plt.xticks(x_cust, cust_metrics.index, rotation=0)
    
    for bar, val in zip(bars, cust_metrics['LifetimeValue']):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(cust_metrics['LifetimeValue'])*0.02,
                f'${val:,.0f}', ha='center', fontweight='bold')
    
    plt.subplot(2, 1, 2)
    satisfaction_returns = cust_metrics[['AvgSatisfaction', 'ReturnRate']].T
    sns.heatmap(satisfaction_returns, annot=True, cmap='RdYlGn', fmt='.2f', cbar_kws={'label': 'Score'})
    plt.title('📊 VIP vs REGULAR: Satisfaction & Returns', fontweight='bold', fontsize=16)
    
    plt.tight_layout()
    plt.savefig(f'{new_output_dir}/4_customer_lifetime.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 4. Customer Lifetime Value")

    # 🔥 GRAPH 5: PAYMENT METHOD INSIGHTS
    plt.figure(figsize=(14, 10))
    
    payment_metrics = df.groupby('PaymentMethod').agg({
        'Sales': ['sum', 'mean'],
        'Quantity': 'sum',
        'Return': 'mean'
    }).round(2)
    payment_metrics.columns = ['TotalSales', 'AvgSales', 'TotalQty', 'ReturnRate']
    
    x_pay = np.arange(len(payment_metrics))
    
    plt.subplot(2, 2, 1)
    plt.pie(payment_metrics['TotalSales'], labels=payment_metrics.index, autopct='%1.1f%%', startangle=90)
    plt.title('💳 PAYMENT METHOD MARKET SHARE')
    
    plt.subplot(2, 2, 2)
    plt.bar(x_pay, payment_metrics['AvgSales'], alpha=0.9, color='purple')
    plt.title('💰 AVERAGE SALE BY PAYMENT')
    plt.xticks(x_pay, payment_metrics.index, rotation=45)
    
    plt.subplot(2, 2, 3)
    plt.bar(x_pay, payment_metrics['ReturnRate'], alpha=0.9, color='red')
    plt.title('⚠️ RETURN RATE BY PAYMENT')
    plt.xticks(x_pay, payment_metrics.index, rotation=45)
    
    plt.subplot(2, 2, 4)
    sizes = payment_metrics['TotalSales']
    plt.scatter(sizes, payment_metrics['ReturnRate'], s=sizes.values/1000, alpha=0.7, c='orange')
    plt.title('🎯 SIZE vs RISK (Bubble Chart)')
    plt.xlabel('Total Sales')
    plt.ylabel('Return Rate')
    
    plt.tight_layout()
    plt.savefig(f'{new_output_dir}/5_payment_insights.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ 5. Payment Method Strategy")

    print(f"\n🎉 SMART BUSINESS ANALYTICS COMPLETE!")
    print(f"📁 Folder: '{new_output_dir}'")
    print("🔥 5 SENSIBLE, ACTIONABLE insights!")
    
    return new_output_dir