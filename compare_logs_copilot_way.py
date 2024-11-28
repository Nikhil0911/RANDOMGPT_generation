import pandas as pd
import re

def clean_logs(log_file):
    with open(log_file, 'r') as file:
        logs = file.readlines()
        
    cleaned_logs = []
    for line in logs:
        line = line.strip()
        if line and (line.startswith('Info') or line.startswith('Error')):
            cleaned_logs.append(line)
    
    return cleaned_logs

def compare_logs(logs1, logs2):
    comparisons = []
    
    for i, log1 in enumerate(logs1):
        for j, log2 in enumerate(logs2):
            log_part1 = log1.split(' - ')[2]
            log_part2 = log2.split(' - ')[2]
            
            data_shape1 = re.search(r'\(\d{1,}, \d{1,}\)', log_part1)
            data_shape2 = re.search(r'\(\d{1,}, \d{1,}\)', log_part2)
            
            comparisons.append({
                'Line no from file 1': i+1,
                'Log type from file 1': log1.split(' - ')[0],
                'Log part from file 1': log_part1,
                'Line no from file 2': j+1,
                'Log type from file 2': log2.split(' - ')[0],
                'Log part from file 2': log_part2,
                'Log type match': log1.split(' - ')[0] == log2.split(' - ')[0],
                'Log part exact match': log_part1 == log_part2,
                'Log part approx match 1': log_part1 in logs2,
                'Log part approx match 2': log_part2 in logs1,
                'Data from file 1': data_shape1.group(0) if data_shape1 else '',
                'Data from file 2': data_shape2.group(0) if data_shape2 else ''
            })
    
    return comparisons

def print_summary(logs1, logs2, cleaned_logs1, cleaned_logs2):
    print(f"Total logs in file 1: {len(logs1)}")
    print(f"Logs removed from file 1 (non-info/error and blank lines): {len(logs1) - len(cleaned_logs1)}")
    print(f"Total logs in file 2: {len(logs2)}")
    print(f"Logs removed from file 2 (non-info/error and blank lines): {len(logs2) - len(cleaned_logs2)}")

def save_to_excel(comparisons, output_file):
    df = pd.DataFrame(comparisons)
    df.to_excel(output_file, index=False)

def main(file1, file2, output_file):
    logs1 = clean_logs(file1)
    logs2 = clean_logs(file2)
    
    comparisons = compare_logs(logs1, logs2)
    
    save_to_excel(comparisons, output_file)
    print_summary(logs1, logs2, logs1, logs2)
    print(f"Comparisons saved to {output_file}")

# Usage
file1 = 'path_to_file1.log'
file2 = 'path_to_file2.log'
output_file = 'comparison_results.xlsx'
main(file1, file2, output_file)
