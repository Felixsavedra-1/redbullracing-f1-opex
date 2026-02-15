import unittest
from tempfile import NamedTemporaryFile

import pandas as pd

import analysis
import data_generator


class AnalysisTests(unittest.TestCase):
    def _sample_df(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "Date": "2025-01-05",
                    "Department": "Aero",
                    "Vendor": "Vendor A",
                    "Description": "Parts",
                    "Budgeted Amount": 10000,
                    "Actual Amount": 17000,
                },
                {
                    "Date": "2025-01-05",
                    "Department": "Aero",
                    "Vendor": "Vendor A",
                    "Description": "Parts",
                    "Budgeted Amount": 10000,
                    "Actual Amount": 17000,
                },
                {
                    "Date": "2025-01-06",
                    "Department": "Logistics",
                    "Vendor": "Vendor B",
                    "Description": "Shipping",
                    "Budgeted Amount": 20000,
                    "Actual Amount": 19000,
                },
            ]
        )

    def test_calculate_variance_adds_columns(self) -> None:
        df = self._sample_df()
        result = analysis.calculate_variance(df)
        self.assertIn("Variance", result.columns)
        self.assertIn("Variance %", result.columns)
        self.assertEqual(result.loc[0, "Variance"], 7000)
        self.assertAlmostEqual(result.loc[0, "Variance %"], 0.7)

    def test_analyze_department_spending_rollup(self) -> None:
        df = analysis.calculate_variance(self._sample_df())
        result = analysis.analyze_department_spending(df)
        aero = result[result["Department"] == "Aero"].iloc[0]
        self.assertEqual(aero["Budgeted Amount"], 20000)
        self.assertEqual(aero["Actual Amount"], 34000)
        self.assertEqual(aero["Variance"], 14000)
        self.assertAlmostEqual(aero["Variance %"], 0.7)

    def test_identify_savings_opportunities(self) -> None:
        df = analysis.calculate_variance(self._sample_df())
        opportunities = analysis.identify_savings_opportunities(df)
        types = {item["Type"] for item in opportunities}
        self.assertIn("High Variance Outlier", types)
        self.assertIn("Potential Duplicate Payments", types)

    def test_unbudgeted_overspend_is_flagged(self) -> None:
        df = pd.DataFrame(
            [
                {
                    "Date": "2025-01-07",
                    "Department": "IT",
                    "Vendor": "Vendor C",
                    "Description": "Emergency purchase",
                    "Budgeted Amount": 0,
                    "Actual Amount": 12000,
                }
            ]
        )
        df = analysis.calculate_variance(df)
        opportunities = analysis.identify_savings_opportunities(df)
        self.assertIn("High Variance Outlier", {item["Type"] for item in opportunities})

    def test_load_data_parses_date_type(self) -> None:
        df = self._sample_df()
        with NamedTemporaryFile(mode="w", suffix=".csv", delete=True) as tmp:
            df.to_csv(tmp.name, index=False)
            loaded = analysis.load_data(tmp.name)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(loaded["Date"]))

    def test_leap_year_generation_can_reach_dec_31(self) -> None:
        df = data_generator.generate_opex_data(num_records=20000, year=2024, seed=42)
        dates = pd.to_datetime(df["Date"])
        self.assertEqual(dates.max(), pd.Timestamp("2024-12-31"))


if __name__ == "__main__":
    unittest.main()
