import data_generator
import analysis
import excel_reporter
import os

def main():
    print("Starting F1 Red Bull OPEX Analysis...")
    
    # 1. Generate Data
    print("Generating synthetic data...")
    df = data_generator.generate_opex_data()
    csv_path = 'opex_data.csv'
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")
    
    # 2. Analyze Data
    print("Analyzing data...")
    df = analysis.load_data(csv_path)
    df = analysis.calculate_variance(df)
    dept_summary = analysis.analyze_department_spending(df)
    opportunities = analysis.identify_savings_opportunities(df)
    
    # 3. Generate Report
    print("Generating Excel report...")
    excel_reporter.create_excel_report(df, dept_summary, opportunities)
    print("Analysis complete. Report generated.")

if __name__ == "__main__":
    main()
