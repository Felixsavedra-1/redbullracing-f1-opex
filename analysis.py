import pandas as pd
import numpy as np

def load_data(filepath):
    """Loads the OPEX data from CSV."""
    return pd.read_csv(filepath, parse_dates=['Date'])

def calculate_variance(df):
    """Calculates variance and variance percentage."""
    df['Variance'] = df['Actual Amount'] - df['Budgeted Amount']
    df['Variance %'] = (df['Variance'] / df['Budgeted Amount']) * 100
    return df

def analyze_department_spending(df):
    """Aggregates spending by department."""
    dept_summary = df.groupby('Department').agg({
        'Budgeted Amount': 'sum',
        'Actual Amount': 'sum',
        'Variance': 'sum'
    }).reset_index()
    dept_summary['Variance %'] = (dept_summary['Variance'] / dept_summary['Budgeted Amount']) * 100
    return dept_summary.sort_values('Variance', ascending=False)

def identify_savings_opportunities(df):
    """Identifies potential savings opportunities."""
    opportunities = []
    
    # 1. High Variance Outliers (e.g., > 50% over budget and > $5000 variance)
    high_variance = df[(df['Variance %'] > 50) & (df['Variance'] > 5000)]
    if not high_variance.empty:
        opportunities.append({
            'Type': 'High Variance Outlier',
            'Count': len(high_variance),
            'Potential Savings': high_variance['Variance'].sum(),
            'Details': high_variance[['Date', 'Department', 'Description', 'Variance']].to_dict('records')
        })
        
    # 2. Potential Duplicates (Same amount, same vendor, same day)
    duplicates = df[df.duplicated(subset=['Date', 'Vendor', 'Actual Amount'], keep=False)]
    if not duplicates.empty:
         opportunities.append({
            'Type': 'Potential Duplicate Payments',
            'Count': len(duplicates),
            'Potential Savings': duplicates['Actual Amount'].sum() / 2, # Assuming one is valid
            'Details': duplicates[['Date', 'Vendor', 'Description', 'Actual Amount']].to_dict('records')
        })
         
    return opportunities

if __name__ == "__main__":
    df = load_data('opex_data.csv')
    df = calculate_variance(df)
    dept_summary = analyze_department_spending(df)
    print("Department Summary:")
    print(dept_summary)
    
    opportunities = identify_savings_opportunities(df)
    print("\nSavings Opportunities:")
    for opp in opportunities:
        print(f"- {opp['Type']}: ${opp['Potential Savings']:,.2f}")
