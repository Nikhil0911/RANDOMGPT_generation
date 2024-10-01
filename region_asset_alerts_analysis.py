import os
import pandas as pd

# Example threshold dictionaries
commodity_swaps_threshold = {'grade1': 500, 'grade2': 1000, 'grade3': 1500, 'grade4': 2000, 'grade5': 2500}
commodity_spot_forwards_threshold = {'grade1': 400, 'grade2': 900, 'grade3': 1400, 'grade4': 1900, 'grade5': 2400}

fx_swaps_threshold = {'grade1': 500, 'grade2': 1000}
fx_spot_fwdndf_threshold = {'grade1': 600, 'grade2': 1100, 'grade3': 1600}
fx_near_far_fuzzy_swaps_threshold = {'grade1': 700, 'grade2': 1200}

# Function to process data files
def process_file(file_path, thresholds, asset_class, asset_type):
    # Read the file based on its extension
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    
    # Keep only relevant columns
    df = df[['Amount', 'Grade']]
    
    results = []
    
    # Process each grade
    for grade, threshold in thresholds.items():
        grade_data = df[df['Grade'] == grade]
        total_data_points = len(grade_data)
        max_amount = grade_data['Amount'].max()
        current_alerts = len(grade_data[grade_data['Amount'] > threshold])
        
        # Placeholder for proposed thresholds, which we'll update later
        proposed_threshold = None
        proposed_alerts = None
        
        results.append({
            'Asset Class': asset_class,
            'Asset Type': asset_type,
            'Grade': grade,
            'Total data points': total_data_points,
            'Max score': max_amount,
            'Current threshold': threshold,
            'Current alerts': current_alerts,
            'Proposed threshold': proposed_threshold,
            'Proposed alerts': proposed_alerts
        })
    
    return results

# Function to get proposed thresholds from external Excel
def get_proposed_thresholds(file_path, region):
    df = pd.read_excel(file_path, sheet_name="Final-Thold")
    region_thresholds = df[df['Region'] == region].iloc[0].to_dict()
    return region_thresholds

# Main function to traverse folders and collect data
def collect_data(main_folder, regions, output_file):
    all_results = []
    
    for region in regions:
        region_folder = os.path.join(main_folder, region)
        
        for asset_class in ['Commodity', 'FX']:
            asset_folder = os.path.join(region_folder, asset_class)
            
            for asset_type in os.listdir(asset_folder):
                asset_type_folder = os.path.join(asset_folder, asset_type)
                
                # Determine the correct threshold dictionary
                if asset_class == 'Commodity':
                    if asset_type == 'Swaps':
                        thresholds = commodity_swaps_threshold
                    elif asset_type == 'Spot-Forwards':
                        thresholds = commodity_spot_forwards_threshold
                elif asset_class == 'FX':
                    if asset_type == 'Swaps':
                        thresholds = fx_swaps_threshold
                    elif asset_type in ['Near Swaps', 'Far Swaps', 'Fuzzy Swaps']:
                        thresholds = fx_near_far_fuzzy_swaps_threshold
                    elif asset_type in ['Spot', 'FwdNdf']:
                        thresholds = fx_spot_fwdndf_threshold
                
                # Process both train and test folders
                for data_split in ['train', 'test']:
                    data_folder = os.path.join(asset_type_folder, data_split)
                    for file_name in os.listdir(data_folder):
                        file_path = os.path.join(data_folder, file_name)
                        results = process_file(file_path, thresholds, asset_class, asset_type)
                        all_results.extend(results)
        
        # Load the proposed thresholds
        proposed_thresholds_file = 'path/to/proposed/thresholds.xlsx'  # Update this path
        proposed_thresholds = get_proposed_thresholds(proposed_thresholds_file, region)
        
        # Apply proposed thresholds and alerts in the result
        for result in all_results:
            grade = result['Grade']
            if grade in proposed_thresholds:
                proposed_threshold = proposed_thresholds[grade]
                result['Proposed threshold'] = proposed_threshold
                result['Proposed alerts'] = len(df[df['Grade'] == grade][df['Amount'] > proposed_threshold])
    
    # Save results to Excel
    df_results = pd.DataFrame(all_results)
    df_results.to_excel(output_file, index=False)

# Usage
main_folder = 'path/to/main/folder'
regions = ['US', 'UK', 'EU']  # Example regions
output_file = 'output_results.xlsx'
collect_data(main_folder, regions, output_file)
