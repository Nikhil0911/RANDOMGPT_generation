import pandas as pd

# Sample data
data = {
    'A': ['A1', 'A1', 'A2', 'A2'],
    'B': ['B1', 'B1', 'B2', 'B2'],
    'C': ['C1', 'C1', 'C2', 'C2'],
    'P_T': ['X', 'Y', 'X', 'Y'],
    27: [10, 20, 30, 40],
    28: [15, 25, 35, 45],
    29: [12, 22, 32, 42],
    30: [14, 24, 34, 44],
    31: [11, 21, 31, 41]
}

df = pd.DataFrame(data)

# Melt the DataFrame
df_melted = df.melt(id_vars=['A', 'B', 'C', 'P_T'], var_name='Dates', value_name='Values')

# Pivot the table to separate X and Y values
df_pivoted = df_melted.pivot_table(index=['A', 'B', 'C', 'Dates'], columns='P_T', values='Values').reset_index()

# Rename columns for clarity
df_pivoted.columns.name = None  # Remove the column index name
df_pivoted.rename(columns={'X': 'X', 'Y': 'Y'}, inplace=True)

# Display the transformed DataFrame
import ace_tools as tools
tools.display_dataframe_to_user(name="Transformed DataFrame", dataframe=df_pivoted)
