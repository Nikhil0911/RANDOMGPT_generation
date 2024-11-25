import pandas as pd

def compare_logs(file1_path, file2_path, output_excel):
    # Read log files
    with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
        logs1 = f1.readlines()
        logs2 = f2.readlines()
    
    # Data for Excel
    comparison_data = []
    
    # Create a mapping of line numbers for File 1 logs for quick lookup
    file1_map = {line.strip(): idx + 1 for idx, line in enumerate(logs1)}

    for idx2, line2 in enumerate(logs2):
        log2 = line2.strip()
        exact_match = "No"
        approx_match = "No"
        approx_line_numbers = []
        difference = ""
        
        # Exact match check
        if idx2 < len(logs1) and logs1[idx2].strip() == log2:
            exact_match = "Yes"
        
        # Approximate match check
        if log2 in file1_map:
            approx_match = "Yes"
            approx_line_numbers.append(file1_map[log2])
        
        # Highlighting difference
        if approx_match == "Yes" and exact_match == "No":
            diff_lines = [logs1[ln - 1].strip() for ln in approx_line_numbers]
            difference = " | ".join(diff_lines)
        
        # Record the comparison
        comparison_data.append({
            "File 1 Line No.": idx2 + 1 if idx2 < len(logs1) else "",
            "Log from File 1": logs1[idx2].strip() if idx2 < len(logs1) else "",
            "File 2 Line No.": idx2 + 1,
            "Log from File 2": log2,
            "Exact Match": exact_match,
            "Approx Match": approx_match,
            "Approx Line No.": ", ".join(map(str, approx_line_numbers)),
            "Difference": difference
        })

    # Convert to DataFrame
    df = pd.DataFrame(comparison_data)
    
    # Save to Excel
    df.to_excel(output_excel, index=False)
    print(f"Comparison saved to {output_excel}")

# Example usage
compare_logs("file1.log", "file2.log", "log_comparison.xlsx")

#------------------------------

import pandas as pd
import re

def extract_log_details(log_line):
    """
    Extract log type (Info/Error) and log message (excluding date) from a log line.
    Format: Info/Error - Date - Log
    """
    parts = log_line.split(" - ", 2)
    if len(parts) == 3:
        log_type = parts[0].strip()
        log_message = parts[2].strip()  # Exclude the date (middle part)
        return log_type, log_message
    return "", log_line.strip()

def is_valid_log(log_message):
    """
    Check if a log message is valid (non-empty and contains at least one alphabetic character).
    """
    return bool(log_message.strip()) and any(char.isalpha() for char in log_message)

def compare_logs(file1_path, file2_path, output_excel):
    # Read log files
    with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
        logs1 = f1.readlines()
        logs2 = f2.readlines()
    
    # Data for Excel
    comparison_data = []
    
    # Create a mapping of valid log messages from File 1 (ignoring dates) for quick lookup
    file1_map = {}
    for idx, line in enumerate(logs1):
        log_type, log_message = extract_log_details(line)
        if is_valid_log(log_message):
            file1_map[log_message] = idx + 1  # Store line number

    for idx2, line2 in enumerate(logs2):
        log_type2, log2_message = extract_log_details(line2)
        if not is_valid_log(log2_message):
            continue  # Skip invalid lines

        exact_match = "No"
        approx_match = "No"
        approx_line_numbers = []
        difference = ""
        
        # Extract log type and message from File 1 for the same line (if it exists)
        if idx2 < len(logs1):
            log_type1, log1_message = extract_log_details(logs1[idx2])
        else:
            log_type1, log1_message = "", ""

        # Skip invalid lines in File 1
        if not is_valid_log(log1_message):
            log_type1, log1_message = "", ""

        # Exact match check
        if log2_message == log1_message and idx2 < len(logs1):
            exact_match = "Yes"
        
        # Approximate match check
        if log2_message in file1_map:
            approx_match = "Yes"
            approx_line_numbers.append(file1_map[log2_message])
        
        # Highlighting differences for approximate matches
        if approx_match == "Yes" and exact_match == "No":
            diff_lines = [logs1[ln - 1].strip() for ln in approx_line_numbers]
            difference = " | ".join(diff_lines)
        
        # Log type match check
        log_type_match = "Yes" if log_type1 == log_type2 else "No"
        
        # Record the comparison
        comparison_data.append({
            "File 1 Line No.": idx2 + 1 if idx2 < len(logs1) else "",
            "Log Type from File 1": log_type1,
            "Log from File 1": log1_message,
            "File 2 Line No.": idx2 + 1,
            "Log Type from File 2": log_type2,
            "Log from File 2": log2_message,
            "Exact Match": exact_match,
            "Approx Match": approx_match,
            "Approx Line No.": ", ".join(map(str, approx_line_numbers)),
            "Difference": difference,
            "Log Type Match": log_type_match
        })

    # Convert to DataFrame
    df = pd.DataFrame(comparison_data)
    
    # Save to Excel
    df.to_excel(output_excel, index=False)
    print(f"Comparison saved to {output_excel}")

# Example usage
compare_logs("file1.log", "file2.log", "log_comparison_filtered.xlsx")
 

