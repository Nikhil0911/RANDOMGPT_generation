import os
import pandas as pd

def process_region_test_data(region_test_path, metal_col, amount_col, new_thresholds):
    # Read the test data
    df = pd.read_csv(region_test_path)  # Assuming CSV files, adjust if needed
    
    # Dictionary to store results for this region
    results = {}

    # Loop through each metal and calculate alert count based on the new threshold
    for metal in new_thresholds.keys():
        # Filter data for the current metal
        metal_data = df[df[metal_col] == metal]
        
        # Calculate the alert count (number of trades crossing the new threshold)
        new_threshold = new_thresholds[metal]
        alert_count = (metal_data[amount_col] > new_threshold).sum()
        
        # Store results in the dictionary
        results[metal] = {
            'New Threshold': new_threshold,
            'Alert Count': alert_count
        }

    return results


def process_all_regions_test(region_paths, metal_col, amount_col, new_thresholds, output_file):
    # Data structure to store results for all regions
    test_region_results = {}
    global_test_results = {metal: {'Alert Count': 0} for metal in new_thresholds.keys()}

    # Process each region for test data
    for region, path in region_paths.items():
        test_region_data = process_region_test_data(path, metal_col, amount_col, new_thresholds)
        test_region_results[region] = test_region_data
        
        # Update global results by aggregating alert count
        for metal in new_thresholds.keys():
            global_test_results[metal]['Alert Count'] += test_region_data[metal]['Alert Count']

    # Prepare DataFrame for region-wise test results
    test_region_df = pd.DataFrame({
        (region, 'New Threshold'): {metal: test_region_results[region][metal]['New Threshold'] for metal in new_thresholds.keys()}
        for region in region_paths.keys()
    })

    for region in region_paths.keys():
        test_region_df[(region, 'Alert Count')] = [test_region_results[region][metal]['Alert Count'] for metal in new_thresholds.keys()]

    # Prepare DataFrame for global test results
    global_test_df = pd.DataFrame({
        ('Global', 'Alert Count'): {metal: global_test_results[metal]['Alert Count'] for metal in new_thresholds.keys()}
    })

    # Combine region-wise results and global test results
    combined_test_df = pd.concat([test_region_df, global_test_df], axis=1)

    # Write to Excel
    with pd.ExcelWriter(output_file) as writer:
        combined_test_df.to_excel(writer, sheet_name='Test Data Alert Counts')

    print(f"Test data alert counts saved to {output_file}")


# Example usage for test data
test_region_paths = {
    'Region1': '/path/to/region1/test_data.csv',
    'Region2': '/path/to/region2/test_data.csv',
    # Add more regions as needed
}

# Example of dynamically calculated thresholds using a statistical method
# You can replace this with your actual statistical threshold calculation logic
new_thresholds = {
    'Gold': 55000,    # Calculated threshold for Gold
    'Silver': 35000,  # Calculated threshold for Silver
    'Copper': 25000,  # Calculated threshold for Copper
    'Platinum': 18000, # Calculated threshold for Platinum
    'Palladium': 12000 # Calculated threshold for Palladium
}

process_all_regions_test(test_region_paths, 'Metal', 'Amount', new_thresholds, 'test_data_alert_counts.xlsx')
