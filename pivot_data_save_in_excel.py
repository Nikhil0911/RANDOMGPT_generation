import pandas as pd
import os

# Sample Data
data = {
    'Month': ['2024-01', '2024-01', '2024-01', '2024-02', '2024-02', '2024-03'],
    'Region': ['US', 'US', 'UK', 'US', 'UK', 'US'],
    'Asset': ['FX', 'FX', 'FX', 'FX', 'FX', 'FX'],
    'RuleSet': ['R1', 'R2', 'R1', 'R1', 'R1', 'R2'],
    'Alerts': [120, 80, 50, 150, 60, 110]
}
df = pd.DataFrame(data)
df['Month'] = pd.to_datetime(df['Month'])

# Step 1: Group data by Region & Asset
grouped = df.groupby(['Region', 'Asset'])

# Step 2: Process each Region + Asset combination
for (region, asset), group_df in grouped:
    # Create pivot table: rows = Month, columns = RuleSet, values = sum of Alerts
    pivot = group_df.pivot_table(index='Month', columns='RuleSet', values='Alerts', aggfunc='sum', fill_value=0)
    
    # Output file path
    file_name = f"{region}_{asset}_Alerts_Pivot.xlsx"
    
    # Write to Excel
    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        pivot.to_excel(writer, sheet_name='Summary')

        # Optional: Create individual sheets per RuleSet if needed
        for ruleset, ruleset_df in group_df.groupby('RuleSet'):
            ruleset_pivot = ruleset_df.pivot_table(index='Month', values='Alerts', aggfunc='sum')
            ruleset_pivot.to_excel(writer, sheet_name=f"{ruleset}")

    print(f"✅ Saved file: {file_name}")
