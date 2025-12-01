import pandas as pd
import xlsxwriter

def create_excel_report(df, dept_summary, opportunities, output_file='opex_analysis_report.xlsx'):
    """
    Creates an Excel report with advanced functions and formatting.
    """
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    workbook = writer.book
    
    # Formats
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
    currency_fmt = workbook.add_format({'num_format': '$#,##0.00'})
    percent_fmt = workbook.add_format({'num_format': '0.00%'})
    red_fmt = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    green_fmt = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
    
    # --- Sheet 1: Executive Summary ---
    dept_summary.to_excel(writer, sheet_name='Executive Summary', index=False, startrow=1)
    worksheet = writer.sheets['Executive Summary']
    
    worksheet.write(0, 0, "Departmental OPEX Overview", workbook.add_format({'bold': True, 'font_size': 14}))
    
    # Apply formats to summary table
    worksheet.set_column('A:A', 20) # Dept
    worksheet.set_column('B:C', 15, currency_fmt) # Budget, Actual
    worksheet.set_column('D:D', 15, currency_fmt) # Variance
    worksheet.set_column('E:E', 12, percent_fmt) # Variance %
    
    # Conditional Formatting for Variance %
    # Red if variance > 10%, Green if variance < 0%
    worksheet.conditional_format('E3:E12', {
        'type': 'cell',
        'criteria': '>',
        'value': 0.1,
        'format': red_fmt
    })
    worksheet.conditional_format('E3:E12', {
        'type': 'cell',
        'criteria': '<',
        'value': 0,
        'format': green_fmt
    })
    
    # Add a chart
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({
        'name':       'Actual Amount',
        'categories': ['Executive Summary', 2, 0, 10, 0], # A3:A11
        'values':     ['Executive Summary', 2, 2, 10, 2], # C3:C11
    })
    chart.set_title({'name': 'Actual Spend by Department'})
    worksheet.insert_chart('G2', chart)

    # --- Sheet 2: Savings Opportunities ---
    worksheet_opp = workbook.add_worksheet('Savings Opportunities')
    worksheet_opp.write(0, 0, "Identified Cost Savings Opportunities", workbook.add_format({'bold': True, 'font_size': 14}))
    
    row = 2
    for opp in opportunities:
        worksheet_opp.write(row, 0, f"Type: {opp['Type']}", workbook.add_format({'bold': True}))
        worksheet_opp.write(row, 1, f"Potential Savings: ${opp['Potential Savings']:,.2f}", red_fmt)
        row += 1
        
        # Create a small dataframe for the details to write easily
        if opp['Details']:
            details_df = pd.DataFrame(opp['Details'])
            # Write headers
            for col_num, value in enumerate(details_df.columns.values):
                worksheet_opp.write(row, col_num, value, header_fmt)
            
            # Write data
            for i, record in enumerate(opp['Details']):
                for col_num, col_name in enumerate(details_df.columns):
                    worksheet_opp.write(row + 1 + i, col_num, record[col_name])
            
            row += len(details_df) + 2

    worksheet_opp.set_column('A:A', 20)
    worksheet_opp.set_column('B:B', 20)
    worksheet_opp.set_column('C:C', 40) # Description
    worksheet_opp.set_column('D:D', 15, currency_fmt)

    # --- Sheet 3: Detailed Data ---
    df.to_excel(writer, sheet_name='Detailed Data', index=False)
    worksheet_data = writer.sheets['Detailed Data']
    worksheet_data.set_column('A:A', 12) # Date
    worksheet_data.set_column('B:C', 20) # Dept, Expense
    worksheet_data.set_column('D:D', 20) # Vendor
    worksheet_data.set_column('E:E', 40) # Description
    worksheet_data.set_column('F:G', 15, currency_fmt) # Budget, Actual
    worksheet_data.set_column('H:H', 15, currency_fmt) # Variance
    worksheet_data.set_column('I:I', 12, percent_fmt) # Variance %

    writer.close()
    print(f"Report generated: {output_file}")
