# F1 Red Bull OPEX - Financial Analysis & Cost Optimization

## Project Overview
This project models Operating Expenses (OPEX) for Oracle Red Bull Racing, utilizing Python and advanced Excel functions to identify cost savings opportunities. It simulates financial data for various departments (Aerodynamics, Power Unit, Logistics, etc.) and performs variance analysis to highlight areas for budget optimization.

## Features
- **Synthetic Data Generation**: Creates realistic financial transaction data for an F1 team.
- **Automated Analysis**: Calculates Budget vs. Actual variances and aggregates spending by department.
- **Cost Optimization**: Identifies specific savings opportunities such as high-variance outliers and potential duplicate payments.
- **Advanced Excel Reporting**: Exports findings to an interactive Excel dashboard with:
    - Conditional Formatting (e.g., highlighting over-budget items).
    - Dynamic Charts.
    - Summary Pivot-like tables.

## Methodology
- **Variance Analysis**: Compute absolute and percentage variance between actuals and budget by transaction.
- **Department Rollup**: Aggregate budget, actuals, and variance by department for leadership-level visibility.
- **Opportunity Detection**:
  - **High-Variance Outliers**: Large overspends based on both percentage and absolute thresholds.
  - **Potential Duplicate Payments**: Same date, vendor, and amount occurring multiple times.
- **Reporting**: Surface insights in an Excel dashboard with conditional formatting and charts.

## Project Structure
- `main.py`: Orchestrates the entire workflow.
- `data_generator.py`: Generates the synthetic `opex_data.csv`.
- `analysis.py`: Contains logic for variance analysis and opportunity identification.
- `excel_reporter.py`: Handles the creation of the formatted Excel report using `xlsxwriter`.

## How to Run
1. **Setup Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Analysis**:
   ```bash
   python3 main.py
   ```

3. **View Report**:
   - Open `opex_analysis_report.xlsx` to see the results.
   - If `xlsxwriter` isn't installed, the script will skip Excel output and print a message.

## Tests
Run the analysis tests with:
```bash
python3 -m unittest discover -s tests
```

## CLI Options
You can control data volume and reproducibility:
```bash
python3 main.py --records 1000 --year 2025 --seed 123 --csv-path opex_data.csv --report-path opex_analysis_report.xlsx
```

## Technologies Used
- Python
- Pandas
- XlsxWriter (optional for Excel output)
