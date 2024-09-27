import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_threshold_comparison(region_paths, metal_col, amount_col, current_thresholds, proposed_thresholds):
    # Data structure to store comparison results
    comparison_data = []

    # Process each region for comparison
    for region, path in region_paths.items():
        df = pd.read_csv(path)  # Load the train data

        # Loop through each metal and gather data
        for metal in current_thresholds.keys():
            # Filter data for the current metal
            metal_data = df[df[metal_col] == metal]
            
            # Calculate current and proposed alert counts
            current_threshold = current_thresholds[metal]
            proposed_threshold = proposed_thresholds[metal]
            current_alert_count = (metal_data[amount_col] > current_threshold).sum()
            proposed_alert_count = (metal_data[amount_col] > proposed_threshold).sum()

            # Append the data for visualization
            comparison_data.append({
                'Region': region,
                'Metal': metal,
                'Current Threshold': current_threshold,
                'Proposed Threshold': proposed_threshold,
                'Current Alert Count': current_alert_count,
                'Proposed Alert Count': proposed_alert_count,
                'Mean Amount': metal_data[amount_col].mean(),
                'Median Amount': metal_data[amount_col].median(),
                'Standard Deviation': metal_data[amount_col].std()
            })

    # Create DataFrame from comparison data
    comparison_df = pd.DataFrame(comparison_data)

    # Plot Threshold Comparison
    plt.figure(figsize=(12, 6))
    sns.barplot(data=comparison_df.melt(id_vars=['Region', 'Metal'], 
                                        value_vars=['Current Threshold', 'Proposed Threshold'], 
                                        var_name='Threshold Type', value_name='Threshold Value'),
                x='Metal', y='Threshold Value', hue='Threshold Type', ci=None)
    plt.title('Current vs Proposed Threshold Comparison')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plot Alert Count Comparison
    plt.figure(figsize=(12, 6))
    sns.barplot(data=comparison_df.melt(id_vars=['Region', 'Metal'], 
                                        value_vars=['Current Alert Count', 'Proposed Alert Count'], 
                                        var_name='Alert Type', value_name='Alert Count'),
                x='Metal', y='Alert Count', hue='Alert Type', ci=None)
    plt.title('Current vs Proposed Alert Count Comparison')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Display summary statistics for each metal and region
    summary_df = comparison_df[['Region', 'Metal', 'Mean Amount', 'Median Amount', 'Standard Deviation']]
    print("Summary Statistics by Region and Metal:")
    print(summary_df.to_string(index=False))


# Example usage
train_region_paths = {
    'Region1': '/path/to/region1/train_data.csv',
    'Region2': '/path/to/region2/train_data.csv',
    # Add more regions as needed
}

current_thresholds = {
    'Gold': 50000,
    'Silver': 30000,
    'Copper': 20000,
    'Platinum': 15000,
    'Palladium': 10000
}

# These are the proposed thresholds, which you have determined by statistical methods
proposed_thresholds = {
    'Gold': 55000,
    'Silver': 35000,
    'Copper': 25000,
    'Platinum': 18000,
    'Palladium': 12000
}

visualize_threshold_comparison(train_region_paths, 'Metal', 'Amount', current_thresholds, proposed_thresholds)
