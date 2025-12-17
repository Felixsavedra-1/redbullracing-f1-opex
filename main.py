import data_generator
import analysis
import excel_reporter


def main() -> None:
    print("Starting F1 Red Bull OPEX analysis.")

    print("Generating synthetic data...")
    df = data_generator.generate_opex_data()
    csv_path = "opex_data.csv"
    df.to_csv(csv_path, index=False)

    print("Running variance analysis...")
    df = analysis.load_data(csv_path)
    df = analysis.calculate_variance(df)
    dept_summary = analysis.analyze_department_spending(df)
    opportunities = analysis.identify_savings_opportunities(df)

    print("Building Excel report...")
    excel_reporter.create_excel_report(df, dept_summary, opportunities)
    print("Analysis complete.")


if __name__ == "__main__":
    main()
