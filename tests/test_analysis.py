import unittest

import pandas as pd

import analysis


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


if __name__ == "__main__":
    unittest.main()
