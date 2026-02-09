"""Core analysis routines for the OPEX dataset."""

from __future__ import annotations

from typing import cast

import pandas as pd
from pandas import Series


HIGH_VARIANCE_PCT = 0.5
HIGH_VARIANCE_AMOUNT = 5000
DUPLICATE_KEYS = ("Date", "Vendor", "Actual Amount")


def _safe_divide(numerator: Series, denominator: Series) -> Series:
    """Divide with zero protection, returning 0 when denominator is 0."""
    safe_denominator = denominator.replace(0, pd.NA)
    return (numerator / safe_denominator).fillna(0)


def load_data(filepath: str) -> pd.DataFrame:
    """Load OPEX data from CSV."""
    return pd.read_csv(filepath, parse_dates=["Date"])


def calculate_variance(df: pd.DataFrame) -> pd.DataFrame:
    """Add absolute and percentage variance columns."""
    df = df.copy()
    df["Variance"] = df["Actual Amount"] - df["Budgeted Amount"]
    df["Variance %"] = _safe_divide(
        cast(Series, df["Variance"]),
        cast(Series, df["Budgeted Amount"]),
    )
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
    grouped["Variance %"] = _safe_divide(
        cast(Series, grouped["Variance"]),
        cast(Series, grouped["Budgeted Amount"]),
    )
    return grouped.sort_values("Variance", ascending=False)


def identify_savings_opportunities(df: pd.DataFrame) -> list[dict[str, object]]:
    """
    Flag large overspends and transactions that are duplicated on
    the same day for the same vendor and amount.
    """
    opportunities: list[dict[str, object]] = []

    high_variance = df[
        (df["Variance %"] > HIGH_VARIANCE_PCT)
        & (df["Variance"] > HIGH_VARIANCE_AMOUNT)
    ]
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

    duplicates = df[df.duplicated(subset=list(DUPLICATE_KEYS), keep=False)]
    if not duplicates.empty:
        grouped_dups = duplicates.groupby(list(DUPLICATE_KEYS))["Actual Amount"]
        # Savings are all but one payment per duplicate group.
        potential_savings = (grouped_dups.sum() - grouped_dups.max()).sum()
        opportunities.append(
            {
                "Type": "Potential Duplicate Payments",
                "Count": len(duplicates),
                "Potential Savings": potential_savings,
                "Details": duplicates[
                    ["Date", "Vendor", "Description", "Actual Amount"]
                ].to_dict("records"),
            }
        )

    return opportunities
