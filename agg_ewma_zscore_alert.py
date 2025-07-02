import pandas as pd
import numpy as np

# Step 1: Example Data (replace with your actual data loading step)
data = {
    'Month': ['2024-01', '2024-01', '2024-01', '2024-02', '2024-02', '2024-03'],
    'Region': ['US', 'US', 'UK', 'US', 'UK', 'US'],
    'Asset': ['FX', 'FX', 'FX', 'FX', 'FX', 'FX'],
    'RuleSet': ['R1', 'R2', 'R1', 'R1', 'R1', 'R2'],
    'Alerts': [120, 80, 50, 150, 60, 110]
}
df = pd.DataFrame(data)

# Step 2: Convert Month to datetime
df['Month'] = pd.to_datetime(df['Month'])

# Step 3: Aggregate by Region, Asset, and Month (sum alerts)
agg_df = df.groupby(['Region', 'Asset', 'Month'])['Alerts'].sum().reset_index()

# Step 4: Define EWMA and Z-score function
alpha = 0.2  # Choose smoothing factor

def apply_ewma_zscore(group):
    group = group.sort_values('Month')  # Ensure proper time order
    group['EWMA_Alerts'] = group['Alerts'].ewm(alpha=alpha, adjust=False).mean()
    
    # Compute Z-score of EWMA
    mean_ewma = group['EWMA_Alerts'].mean()
    std_ewma = group['EWMA_Alerts'].std()
    group['Z_score'] = (group['EWMA_Alerts'] - mean_ewma) / std_ewma

    # Flag colors based on Z-score
    def flag_color(z):
        if abs(z) > 3:
            return 'Red'
        elif abs(z) > 2:
            return 'Yellow'
        else:
            return 'Green'

    group['Flag'] = group['Z_score'].apply(flag_color)
    return group

# Step 5: Apply the logic for each Region + Asset group
result_df = agg_df.groupby(['Region', 'Asset'], group_keys=False).apply(apply_ewma_zscore).reset_index(drop=True)

# Step 6: Save result to Excel with a sheet for each Region-Asset
output_file = 'ewma_alert_monitoring.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    for (region, asset), group in result_df.groupby(['Region', 'Asset']):
        sheet_name = f"{region}_{asset}"[:31]  # Excel sheet name max length = 31
        group.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"✅ Results saved to {output_file}")
