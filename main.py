import pandas as pd
import altair as alt

from constants import *

# Set up workbook
xl = pd.ExcelFile(path_xl, engine='openpyxl')

# Get sheet names
sheets = xl.sheet_names

# Read in all sheets into dict
xl_df = {}
for sheet in sheets:

    # Get df from sheet
    xlsht = pd.read_excel(path_xl, sheet_name=sheet, engine='openpyxl')

    # Subset columns
    xlsht = xlsht[cols]
    xlsht[numeric_cols] = xlsht[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # Subset rows
    xlsht = xlsht.iloc[:28]

    # Read in sheet
    xl_df.update({sheet:xlsht})



def get_points_lines(df):
    # Odds ratios
    points = alt.Chart(df).mark_point().encode(
            x = alt.X('Odds_ratio:Q'),
            y = alt.Y('Precursor:N')
        )

    lines = points.mark_errorbar().encode(
        x= 'lower .95:Q',
        x2 = 'upper .95:Q',
        y = 'Precursor'

    )
    return (points+lines)


chart1 = get_points_lines(xl_df[sheets[0]])
chart2 = get_points_lines(xl_df[sheets[1]])
# chart3 = get_points_lines(xl_df[sheets[2]])
(chart1|chart2).show()
# (chart1|chart2|chart3).show()
