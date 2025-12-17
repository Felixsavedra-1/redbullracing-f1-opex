import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    """Load OPEX data from CSV."""
    return pd.read_csv(filepath, parse_dates=["Date"])


def calculate_variance(df: pd.DataFrame) -> pd.DataFrame:
    """Add absolute and percentage variance columns."""
    df = df.copy()
    df["Variance"] = df["Actual Amount"] - df["Budgeted Amount"]
    df["Variance %"] = (df["Variance"] / df["Budgeted Amount"]) * 100
    return df


def analyze_department_spending(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate spending and variance by department."""
    grouped = (
        df.groupby("Department", as_index=False)
        .agg(
            {
                "Budgeted Amount": "sum",
                "Actual Amount": "sum",
                "Variance": "sum",
            }
        )
    )
    grouped["Variance %"] = (grouped["Variance"] / grouped["Budgeted Amount"]) * 100
    return grouped.sort_values("Variance", ascending=False)


def identify_savings_opportunities(df: pd.DataFrame) -> list[dict]:
    """
    Flag large overspends and transactions that are duplicated on
    the same day for the same vendor and amount.
    """
    opportunities: list[dict] = []

    high_variance = df[(df["Variance %"] > 50) & (df["Variance"] > 5000)]
    if not high_variance.empty:
        opportunities.append(
            {
                "Type": "High Variance Outlier",
                "Count": len(high_variance),
                "Potential Savings": high_variance["Variance"].sum(),
                "Details": high_variance[
                    ["Date", "Department", "Description", "Variance"]
                ].to_dict("records"),
            }
        )

    duplicates = df[df.duplicated(subset=["Date", "Vendor", "Actual Amount"], keep=False)]
    if not duplicates.empty:
        opportunities.append(
            {
                "Type": "Potential Duplicate Payments",
                "Count": len(duplicates),
                "Potential Savings": duplicates["Actual Amount"].sum() / 2,
                "Details": duplicates[
                    ["Date", "Vendor", "Description", "Actual Amount"]
                ].to_dict("records"),
            }
        )

    return opportunities
