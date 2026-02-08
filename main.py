import argparse

import analysis
import data_generator
import excel_reporter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the F1 OPEX analysis pipeline.")
    parser.add_argument("--records", type=int, default=500, help="Number of records to generate.")
    parser.add_argument("--year", type=int, default=2024, help="Year to simulate.")
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible data generation.",
    )
    parser.add_argument(
        "--csv-path",
        default="opex_data.csv",
        help="Where to write the generated CSV.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("Starting F1 Red Bull OPEX analysis.")

    print("Generating synthetic data...")
    df = data_generator.generate_opex_data(
        num_records=args.records,
        year=args.year,
        seed=args.seed,
    )
    df.to_csv(args.csv_path, index=False)

    print("Running variance analysis...")
    df = analysis.load_data(args.csv_path)
    df = analysis.calculate_variance(df)
    dept_summary = analysis.analyze_department_spending(df)
    opportunities = analysis.identify_savings_opportunities(df)

    print("Building Excel report...")
    excel_reporter.create_excel_report(df, dept_summary, opportunities)
    print("Analysis complete.")


if __name__ == "__main__":
    main()
