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

## Technologies Used
- Python
- Pandas
- XlsxWriter (optional for Excel output)
- NumPy
