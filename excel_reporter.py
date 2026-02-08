import pandas as pd


def create_excel_report(
    df: pd.DataFrame,
    dept_summary: pd.DataFrame,
    opportunities: list[dict],
    output_file: str = "opex_analysis_report.xlsx",
) -> None:
    """Write an Excel workbook summarizing department spend and flagged items."""
    try:
        import xlsxwriter  # noqa: F401  # used indirectly by pandas ExcelWriter
    except ImportError:
        print(
            "Excel report skipped: missing optional dependency 'xlsxwriter'. "
            "Install it to generate opex_analysis_report.xlsx."
        )
        return

    if dept_summary.empty:
        print("Excel report skipped: department summary is empty.")
        return

    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        workbook = writer.book

        header_fmt = workbook.add_format({"bold": True, "bg_color": "#D3D3D3", "border": 1})
        currency_fmt = workbook.add_format({"num_format": "$#,##0.00"})
        percent_fmt = workbook.add_format({"num_format": "0.00%"})
        red_fmt = workbook.add_format({"bg_color": "#FFC7CE", "font_color": "#9C0006"})
        green_fmt = workbook.add_format({"bg_color": "#C6EFCE", "font_color": "#006100"})

        dept_summary.to_excel(writer, sheet_name="Executive Summary", index=False, startrow=1)
        worksheet = writer.sheets["Executive Summary"]

        worksheet.write(
            0,
            0,
            "Departmental OPEX Overview",
            workbook.add_format({"bold": True, "font_size": 14}),
        )

        worksheet.set_column("A:A", 20)
        worksheet.set_column("B:C", 15, currency_fmt)
        worksheet.set_column("D:D", 15, currency_fmt)
        worksheet.set_column("E:E", 12, percent_fmt)
        worksheet.set_row(1, None, header_fmt)
        worksheet.freeze_panes(2, 0)

        first_data_row = 3
        last_data_row = first_data_row + len(dept_summary) - 1
        variance_range = f"E{first_data_row}:E{last_data_row}"
        worksheet.conditional_format(
            variance_range,
            {
                "type": "cell",
                "criteria": ">",
                "value": 0.1,
                "format": red_fmt,
            },
        )
        worksheet.conditional_format(
            variance_range,
            {
                "type": "cell",
                "criteria": "<",
                "value": 0,
                "format": green_fmt,
            },
        )

        chart = workbook.add_chart({"type": "column"})
        first_row = 2
        last_row = first_row + len(dept_summary) - 1
        chart.add_series(
            {
                "name": "Actual Amount",
                "categories": ["Executive Summary", first_row, 0, last_row, 0],
                "values": ["Executive Summary", first_row, 2, last_row, 2],
            }
        )
        chart.set_title({"name": "Actual Spend by Department"})
        worksheet.insert_chart("G2", chart)

        worksheet_opp = workbook.add_worksheet("Savings Opportunities")
        worksheet_opp.write(
            0,
            0,
            "Identified Cost Savings Opportunities",
            workbook.add_format({"bold": True, "font_size": 14}),
        )

        row = 2
        for opp in opportunities:
            worksheet_opp.write(row, 0, f"Type: {opp['Type']}", workbook.add_format({"bold": True}))
            worksheet_opp.write(
                row,
                1,
                f"Potential Savings: ${opp['Potential Savings']:,.2f}",
                red_fmt,
            )
            row += 1

            details = opp.get("Details") or []
            if details:
                details_df = pd.DataFrame(details)
                for col_num, value in enumerate(details_df.columns.values):
                    worksheet_opp.write(row, col_num, value, header_fmt)

                for i, record in enumerate(details):
                    for col_num, col_name in enumerate(details_df.columns):
                        worksheet_opp.write(row + 1 + i, col_num, record[col_name])

                row += len(details_df) + 2

        worksheet_opp.set_column("A:A", 20)
        worksheet_opp.set_column("B:B", 20)
        worksheet_opp.set_column("C:C", 40)
        worksheet_opp.set_column("D:D", 15, currency_fmt)

        df.to_excel(writer, sheet_name="Detailed Data", index=False)
        worksheet_data = writer.sheets["Detailed Data"]
        worksheet_data.set_column("A:A", 12)
        worksheet_data.set_column("B:C", 20)
        worksheet_data.set_column("D:D", 20)
        worksheet_data.set_column("E:E", 40)
        worksheet_data.set_column("F:G", 15, currency_fmt)
        worksheet_data.set_column("H:H", 15, currency_fmt)
        worksheet_data.set_column("I:I", 12, percent_fmt)
        worksheet_data.freeze_panes(1, 0)

    print(f"Report generated: {output_file}")
