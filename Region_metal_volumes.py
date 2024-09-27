import os
import pandas as pd

def process_region_data(region_path, metal_col, amount_col, thresholds):
    # Read the data
    df = pd.read_csv(region_path)  # Assuming CSV files, you can modify if needed
    
    # Dictionary to store results for this region
    results = {}

    # Loop through each metal and calculate max and alert count
    for metal in thresholds.keys():
        # Filter data for the current metal
        metal_data = df[df[metal_col] == metal]
        
        # Calculate max amount traded for this metal
        max_amount = metal_data[amount_col].max()
        
        # Calculate the alert count (number of trades crossing the threshold)
        threshold = thresholds[metal]
        alert_count = (metal_data[amount_col] > threshold).sum()
        
        # Store results in the dictionary
        results[metal] = {
            'Max Amount': max_amount,
            'Threshold': threshold,
            'Alert Count': alert_count
        }

    return results


def process_all_regions(region_paths, metal_col, amount_col, thresholds, output_file):
    # Data structure to store results for all regions
    region_results = {}
    global_results = {metal: {'Max Amount': 0, 'Alert Count': 0} for metal in thresholds.keys()}

    # Process each region
    for region, path in region_paths.items():
        region_data = process_region_data(path, metal_col, amount_col, thresholds)
        region_results[region] = region_data
        
        # Update global results by aggregating max and alert count
        for metal in thresholds.keys():
            global_results[metal]['Max Amount'] = max(global_results[metal]['Max Amount'], region_data[metal]['Max Amount'])
            global_results[metal]['Alert Count'] += region_data[metal]['Alert Count']

    # Prepare DataFrame for region-wise results
    region_df = pd.DataFrame({
        (region, 'Max Amount'): {metal: region_results[region][metal]['Max Amount'] for metal in thresholds.keys()}
        for region in region_paths.keys()
    })

    for region in region_paths.keys():
        region_df[(region, 'Threshold')] = [region_results[region][metal]['Threshold'] for metal in thresholds.keys()]
        region_df[(region, 'Alert Count')] = [region_results[region][metal]['Alert Count'] for metal in thresholds.keys()]

    # Prepare DataFrame for global results
    global_df = pd.DataFrame({
        ('Global', 'Max Amount'): {metal: global_results[metal]['Max Amount'] for metal in thresholds.keys()},
        ('Global', 'Alert Count'): {metal: global_results[metal]['Alert Count'] for metal in thresholds.keys()}
    })

    # Combine region-wise results and global results
    combined_df = pd.concat([region_df, global_df], axis=1)

    # Write to Excel
    with pd.ExcelWriter(output_file) as writer:
        combined_df.to_excel(writer, sheet_name='Metal Trading Analysis')

    print(f"Data saved to {output_file}")


# Example usage
region_paths = {
    'Region1': '/path/to/region1_data.csv',
    'Region2': '/path/to/region2_data.csv',
    # Add more regions as needed
}

thresholds = {
    'Gold': 50000,
    'Silver': 30000,
    'Copper': 20000,
    'Platinum': 15000,
    'Palladium': 10000
}

process_all_regions(region_paths, 'Metal', 'Amount', thresholds, 'metal_trading_analysis.xlsx')
