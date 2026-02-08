import random
from datetime import datetime, timedelta
from typing import Sequence

import pandas as pd


DEPARTMENTS: Sequence[str] = [
    "Aerodynamics",
    "Power Unit",
    "Chassis",
    "Logistics",
    "Strategy",
    "Vehicle Performance",
    "Marketing",
    "IT",
]

EXPENSE_TYPES: dict[str, list[str]] = {
    "Aerodynamics": ["Wind Tunnel Usage", "CFD License", "Composite Materials", "Prototyping"],
    "Power Unit": ["Engine Testing", "Fuel Analysis", "Hybrid System Components", "Dyno Operations"],
    "Chassis": ["Carbon Fiber", "Suspension Parts", "Crash Testing", "Machining"],
    "Logistics": ["Freight - Air", "Freight - Sea", "Travel & Accommodation", "Catering"],
    "Strategy": ["Simulation Software", "Data Feeds", "Consulting", "Compute Resources"],
    "Vehicle Performance": ["Telemetry Systems", "Trackside Equipment", "Sensor Calibration", "Driver Simulator"],
    "Marketing": ["Sponsorship Events", "Merchandise", "Digital Content", "Hospitality"],
    "IT": ["Server Infrastructure", "Cybersecurity", "Software Licenses", "Hardware Upgrades"],
}

VENDORS: Sequence[str] = [
    "Oracle",
    "Honda",
    "Siemens",
    "Hewlett Packard Enterprise",
    "AT&T",
    "Tag Heuer",
    "Mobil 1",
    "Pirelli",
    "DHL",
    "Ansys",
]


def generate_opex_data(
    num_records: int = 500,
    year: int = 2024,
    seed: int | None = 42,
) -> pd.DataFrame:
    """Simulate transactional OPEX data for a single calendar year."""
    if num_records < 3:
        raise ValueError("num_records must be at least 3 to inject demo anomalies.")

    rng = random.Random(seed)
    start_date = datetime(year, 1, 1)
    data: list[dict] = []

    for _ in range(num_records):
        dept = rng.choice(DEPARTMENTS)
        expense = rng.choice(EXPENSE_TYPES[dept])
        vendor = rng.choice(VENDORS)

        date = start_date + timedelta(days=rng.randint(0, 364))
        budget = round(rng.uniform(1_000, 100_000), 2)
        variance_factor = rng.normalvariate(1.0, 0.15)
        actual = round(max(0.0, budget * variance_factor), 2)

        data.append(
            {
                "Date": date,
                "Department": dept,
                "Expense Type": expense,
                "Vendor": vendor,
                "Description": f"{expense} invoice from {vendor}",
                "Budgeted Amount": budget,
                "Actual Amount": actual,
            }
        )

    df = pd.DataFrame(data)

    df.loc[0, "Department"] = "Logistics"
    df.loc[0, "Expense Type"] = "Freight - Air"
    df.loc[0, "Budgeted Amount"] = 50_000
    df.loc[0, "Actual Amount"] = 120_000
    df.loc[0, "Description"] = "Emergency Air Freight - Urgent Upgrade Package"

    df.loc[1] = df.loc[2].copy()
    df.loc[1, "Description"] = df.loc[2, "Description"] + " (DUPLICATE?)"

    return df


if __name__ == "__main__":
    frame = generate_opex_data()
    print(frame.head())
    frame.to_csv("opex_data.csv", index=False)
    print("Data written to opex_data.csv")
