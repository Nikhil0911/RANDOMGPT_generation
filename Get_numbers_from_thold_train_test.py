import pandas as pd

# Step 1: Read train and test datasets
train_df = pd.read_csv('train_data.csv')  # Replace with actual file path
test_df = pd.read_csv('test_data.csv')    # Replace with actual file path

# Step 2: Read current and proposed thresholds from Excel
thresholds = pd.read_excel('thresholds.xlsx', sheet_name=None)  # Load all sheets from Excel

# Assuming thresholds are stored in different sheets based on region and metal

# Step 3: Calculate alerts based on current and proposed thresholds
def calculate_alerts(df, current_thold, proposed_thold):
    alerts_current = df[df['amount'] > current_thold]
    alerts_proposed = df[df['amount'] > proposed_thold]
    return len(alerts_current), len(alerts_proposed)

# Step 4: Aggregate results
results = []

for region, metal in thresholds.keys():
    current_thold = thresholds[(region, metal)]['current_thold'].iloc[0]
    proposed_thold = thresholds[(region, metal)]['proposed_thold'].iloc[0]
    
    train_alerts_current, train_alerts_proposed = calculate_alerts(train_df, current_thold, proposed_thold)
    test_alerts_current, test_alerts_proposed = calculate_alerts(test_df, current_thold, proposed_thold)
    
    results.append({
        'Region': region,
        'Metal': metal,
        'Train Alerts Current Thold': train_alerts_current,
        'Train Alerts Proposed Thold': train_alerts_proposed,
        'Test Alerts Current Thold': test_alerts_current,
        'Test Alerts Proposed Thold': test_alerts_proposed
    })

# Step 5: Save results to Excel
output_df = pd.DataFrame(results)
output_df.to_excel('alerts_summary.xlsx', index=False)
