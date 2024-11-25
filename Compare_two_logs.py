import pandas as pd

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

def is_valid_log(log_line):
    """
    Check if a log line is valid:
    1. Starts with 'Info' or 'Error' (case-insensitive).
    2. Contains a log message with at least one alphabetic character.
    """
    if not log_line.strip():
        return False  # Empty line
    log_type, log_message = extract_log_details(log_line)
    if log_type.lower() not in ["info", "error"]:
        return False  # Invalid log type
    if not any(char.isalpha() for char in log_message):
        return False  # Log message without alphabets
    return True

def compare_logs(file1_path, file2_path, output_excel):
    # Read log files
    with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
        logs1 = f1.readlines()
        logs2 = f2.readlines()
    
    total_lines_file1 = len(logs1)
    total_lines_file2 = len(logs2)
    
    # Filter valid logs
    valid_logs1 = [line.strip() for line in logs1 if is_valid_log(line)]
    valid_logs2 = [line.strip() for line in logs2 if is_valid_log(line)]

    valid_lines_file1 = len(valid_logs1)
    valid_lines_file2 = len(valid_logs2)
    
    # Data for Excel
    comparison_data = []
    
    # Create a mapping of valid log messages from File 1 and File 2 for quick lookup
    file1_map = {}
    file2_map = {}

    for idx, line in enumerate(valid_logs1):
        log_type, log_message = extract_log_details(line)
        file1_map[log_message] = idx + 1  # Store line number
    
    for idx, line in enumerate(valid_logs2):
        log_type, log_message = extract_log_details(line)
        file2_map[log_message] = idx + 1  # Store line number

    # Process File 2 logs for comparison
    for idx2, line2 in enumerate(valid_logs2):
        log_type2, log2_message = extract_log_details(line2)
        exact_match = "No"
        approx_match1 = "No"
        approx_line_numbers1 = []
        difference = ""

        # Find corresponding valid File 1 log for the same line number
        if idx2 < len(valid_logs1):
            log_type1, log1_message = extract_log_details(valid_logs1[idx2])
        else:
            log_type1, log1_message = "", ""

        # Exact match check
        if log2_message == log1_message and idx2 < len(valid_logs1):
            exact_match = "Yes"
        
        # Approximate match 1 check (File 2 log in File 1)
        if log2_message in file1_map:
            approx_match1 = "Yes"
            approx_line_numbers1.append(file1_map[log2_message])
        
        # Highlighting differences for approximate matches
        if approx_match1 == "Yes" and exact_match == "No":
            diff_lines = [valid_logs1[ln - 1] for ln in approx_line_numbers1]
            difference = " | ".join(diff_lines)
        
        # Log type match check
        log_type_match = "Yes" if log_type1.lower() == log_type2.lower() else "No"

        # Approximate match 2 check (File 1 log in File 2)
        approx_match2 = "Yes" if log1_message in file2_map else "No"
        
        # Record the comparison
        comparison_data.append({
            "File 1 Line No.": file1_map.get(log2_message, ""),  # Line number from File 1 if approx matched
            "Log Type from File 1": log_type1,
            "Log from File 1": log1_message,
            "File 2 Line No.": idx2 + 1,
            "Log Type from File 2": log_type2,
            "Log from File 2": log2_message,
            "Exact Match": exact_match,
            "Approx Match 1 (File 2 in File 1)": approx_match1,
            "Approx Line No. (File 1)": ", ".join(map(str, approx_line_numbers1)),
            "Difference": difference,
            "Log Type Match": log_type_match,
            "Approx Match 2 (File 1 in File 2)": approx_match2
        })

    # Print line counts
    print(f"Total lines in File 1: {total_lines_file1}")
    print(f"Valid lines in File 1: {valid_lines_file1}")
    print(f"Total lines in File 2: {total_lines_file2}")
    print(f"Valid lines in File 2: {valid_lines_file2}")

    # Convert to DataFrame
    df = pd.DataFrame(comparison_data)
    
    # Save to Excel
    df.to_excel(output_excel, index=False)
    print(f"Comparison saved to {output_excel}")

# Example usage
compare_logs("file1.log", "file2.log", "log_comparison_filtered.xlsx")
