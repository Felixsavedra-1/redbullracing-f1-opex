import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_opex_data(num_records=500):
    """
    Generates synthetic OPEX data for Oracle Red Bull Racing.
    """
    departments = [
        'Aerodynamics', 'Power Unit', 'Chassis', 'Logistics', 
        'Strategy', 'Vehicle Performance', 'Marketing', 'IT'
    ]
    
    expense_types = {
        'Aerodynamics': ['Wind Tunnel Usage', 'CFD License', 'Composite Materials', 'Prototyping'],
        'Power Unit': ['Engine Testing', 'Fuel Analysis', 'Hybrid System Components', 'Dyno Operations'],
        'Chassis': ['Carbon Fiber', 'Suspension Parts', 'Crash Testing', 'Machining'],
        'Logistics': ['Freight - Air', 'Freight - Sea', 'Travel & Accommodation', 'Catering'],
        'Strategy': ['Simulation Software', 'Data Feeds', 'Consulting', 'Compute Resources'],
        'Vehicle Performance': ['Telemetry Systems', 'Trackside Equipment', 'Sensor Calibration', 'Driver Simulator'],
        'Marketing': ['Sponsorship Events', 'Merchandise', 'Digital Content', 'Hospitality'],
        'IT': ['Server Infrastructure', 'Cybersecurity', 'Software Licenses', 'Hardware Upgrades']
    }
    
    vendors = [
        'Oracle', 'Honda', 'Siemens', 'Hewlett Packard Enterprise', 
        'AT&T', 'Tag Heuer', 'Mobil 1', 'Pirelli', 'DHL', 'Ansys'
    ]
    
    data = []
    start_date = datetime(2024, 1, 1)
    
    for _ in range(num_records):
        dept = random.choice(departments)
        expense = random.choice(expense_types[dept])
        vendor = random.choice(vendors)
        
        # Random date within 2024
        date = start_date + timedelta(days=random.randint(0, 364))
        
        # Budgeted amount (random between 1k and 100k)
        budget = round(random.uniform(1000, 100000), 2)
        
        # Actual amount (Budget +/- 20% variance usually, sometimes more for outliers)
        variance_factor = random.normalvariate(1.0, 0.15) # Mean 1.0, SD 0.15
        actual = round(budget * variance_factor, 2)
        
        description = f"{expense} invoice from {vendor}"
        
        data.append({
            'Date': date,
            'Department': dept,
            'Expense Type': expense,
            'Vendor': vendor,
            'Description': description,
            'Budgeted Amount': budget,
            'Actual Amount': actual
        })
        
    df = pd.DataFrame(data)
    
    # Add some specific outliers for analysis
    # 1. High overspend in Logistics
    df.loc[0, 'Department'] = 'Logistics'
    df.loc[0, 'Expense Type'] = 'Freight - Air'
    df.loc[0, 'Budgeted Amount'] = 50000
    df.loc[0, 'Actual Amount'] = 120000 # Big overspend
    df.loc[0, 'Description'] = 'Emergency Air Freight - Urgent Upgrade Package'
    
    # 2. Duplicate payment potential
    df.loc[1] = df.loc[2].copy()
    df.loc[1, 'Description'] = df.loc[2, 'Description'] + " (DUPLICATE?)"
    
    return df

if __name__ == "__main__":
    df = generate_opex_data()
    print(df.head())
    df.to_csv('opex_data.csv', index=False)
    print("Data generated and saved to opex_data.csv")
