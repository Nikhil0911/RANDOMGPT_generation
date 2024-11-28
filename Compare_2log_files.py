import pandas as pd
import re

def parse_logs(file_path):
    """Parse and filter logs from a file."""
    logs = []
    removed_counts = {"blank_lines": 0, "invalid_logs": 0}
    
    with open(file_path, "r") as file:
        for line_num, line in enumerate(file, start=1):
            # Remove blank lines
            if not line.strip():
                removed_counts["blank_lines"] += 1
                continue
            
            # Match valid logs starting with 'info' or 'error'
            match = re.match(r"^(info|error)\s*-\s*([\d\-:\s]*)-\s*(.*)", line.strip(), re.IGNORECASE)
            if not match:
                removed_counts["invalid_logs"] += 1
                continue
            
            log_type, date, log_part = match.groups()
            logs.append({"line_no": line_num, "log_type": log_type.lower(), "log_part": log_part.strip()})
    
    return logs, removed_counts

def compare_logs(file1_logs, file2_logs):
    """Perform comparisons between two log lists."""
    comparisons = []
    
    def find_data_shape(log):
        """Extract data shape in the form (rows, columns)."""
        match = re.search(r"\(\d+,\s*\d+\)", log)
        return match.group() if match else None

    # Helper for comparisons
    def find_match(log_part, logs, check_type=True):
        for log in logs:
            # Exact match
            if log_part == log["log_part"]:
                return log, True, True
            # Approximate match
            elif log_part in log["log_part"]:
                return log, False, True if not check_type else log_part == log["log_part"]
        return None, False, False

    # Compare file1 logs in file2
    for log1 in file1_logs:
        log2, type_match, part_match = find_match(log1["log_part"], file2_logs)
        data_shape_match = find_data_shape(log1["log_part"]) in [find_data_shape(l["log_part"]) for l in file2_logs]
        comparisons.append({
            "line_no_1": log1["line_no"],
            "log_type_1": log1["log_type"],
            "log_part_1": log1["log_part"],
            "line_no_2": log2["line_no"] if log2 else None,
            "log_type_2": log2["log_type"] if log2 else None,
            "log_part_2": log2["log_part"] if log2 else None,
            "log_type_match": type_match,
            "log_part_exact_match": part_match,
            "log_part_approx_match_1": log2 is not None,
            "log_part_approx_match_2": False,  # Will fill in second pass
            "data_from_file_1": find_data_shape(log1["log_part"]),
            "data_from_file_2": data_shape_match
        })

    # Compare file2 logs in file1 (second pass for approx_match_2)
    for log2 in file2_logs:
        log1, _, _ = find_match(log2["log_part"], file1_logs, check_type=False)
        for comp in comparisons:
            if comp["line_no_1"] == (log1["line_no"] if log1 else None):
                comp["log_part_approx_match_2"] = True
                break
    
    return comparisons

def write_to_excel(comparisons, output_file):
    """Write comparisons to an Excel file."""
    df = pd.DataFrame(comparisons)
    df.to_excel(output_file, index=False, sheet_name="Log Comparisons")

def print_summary(file_path, total_logs, removed_counts):
    """Print log statistics."""
    print(f"File: {file_path}")
    print(f"Total logs: {total_logs}")
    print(f"Removed blank lines: {removed_counts['blank_lines']}")
    print(f"Removed invalid logs: {removed_counts['invalid_logs']}")
    print(f"Remaining logs: {total_logs - sum(removed_counts.values())}\n")

# Main Execution
file1_path = "log_file_1.txt"
file2_path = "log_file_2.txt"
output_file = "log_comparison.xlsx"

# Parse both log files
file1_logs, file1_removed = parse_logs(file1_path)
file2_logs, file2_removed = parse_logs(file2_path)

# Print summaries
print_summary(file1_path, len(file1_logs) + sum(file1_removed.values()), file1_removed)
print_summary(file2_path, len(file2_logs) + sum(file2_removed.values()), file2_removed)

# Compare logs
comparisons = compare_logs(file1_logs, file2_logs)

# Write results to Excel
write_to_excel(comparisons, output_file)

print(f"Comparison completed and saved to {output_file}")
#---

import pandas as pd
import re

def parse_logs(file_path):
    """Parse and filter logs from a file."""
    logs = []
    removed_counts = {"blank_lines": 0, "invalid_logs": 0}
    
    with open(file_path, "r") as file:
        for line_num, line in enumerate(file, start=1):
            # Remove blank lines
            if not line.strip():
                removed_counts["blank_lines"] += 1
                continue
            
            # Match valid logs starting with 'info' or 'error'
            match = re.match(r"^(info|error)\s*-\s*([\d\-:\s]*)-\s*(.*)", line.strip(), re.IGNORECASE)
            if not match:
                removed_counts["invalid_logs"] += 1
                continue
            
            log_type, date, log_part = match.groups()
            logs.append({"line_no": line_num, "log_type": log_type.lower(), "log_part": log_part.strip()})
    
    return logs, removed_counts

def compare_logs(file1_logs, file2_logs):
    """Perform comparisons between two log lists."""
    comparisons = []
    
    def find_data_shape(log):
        """Extract data shape in the form (rows, columns)."""
        match = re.search(r"\(\d+,\s*\d+\)", log)
        return match.group() if match else None

    # Compare file1 logs in file2
    for log1 in file1_logs:
        exact_match = None
        approx_match = None
        data_shape_match = False
        log1_data_shape = find_data_shape(log1["log_part"])

        for log2 in file2_logs:
            # Check for exact match
            if log1["log_part"] == log2["log_part"]:
                exact_match = log2
                break
            # Check for approximate match
            elif log1["log_part"] in log2["log_part"]:
                approx_match = log2

            # Check for data shape match
            if log1_data_shape == find_data_shape(log2["log_part"]):
                data_shape_match = True

        comparisons.append({
            "line_no_1": log1["line_no"],
            "log_type_1": log1["log_type"],
            "log_part_1": log1["log_part"],
            "line_no_2": exact_match["line_no"] if exact_match else (approx_match["line_no"] if approx_match else None),
            "log_type_2": exact_match["log_type"] if exact_match else (approx_match["log_type"] if approx_match else None),
            "log_part_2": exact_match["log_part"] if exact_match else (approx_match["log_part"] if approx_match else None),
            "log_type_match": exact_match["log_type"] == log1["log_type"] if exact_match else False,
            "log_part_exact_match": exact_match is not None,
            "log_part_approx_match_1": approx_match is not None,
            "log_part_approx_match_2": False,  # Will fill in the next step
            "data_from_file_1": log1_data_shape,
            "data_from_file_2": data_shape_match
        })

    # Compare file2 logs in file1 for approx_match_2
    for log2 in file2_logs:
        for comp in comparisons:
            if log2["log_part"] in comp["log_part_1"]:
                comp["log_part_approx_match_2"] = True
                break

    return comparisons

def write_to_excel(comparisons, output_file):
    """Write comparisons to an Excel file."""
    df = pd.DataFrame(comparisons)
    df.to_excel(output_file, index=False, sheet_name="Log Comparisons")

def print_summary(file_path, total_logs, removed_counts):
    """Print log statistics."""
    print(f"File: {file_path}")
    print(f"Total logs: {total_logs}")
    print(f"Removed blank lines: {removed_counts['blank_lines']}")
    print(f"Removed invalid logs: {removed_counts['invalid_logs']}")
    print(f"Remaining logs: {total_logs - sum(removed_counts.values())}\n")

# Main Execution
file1_path = "log_file_1.txt"
file2_path = "log_file_2.txt"
output_file = "log_comparison.xlsx"

# Parse both log files
file1_logs, file1_removed = parse_logs(file1_path)
file2_logs, file2_removed = parse_logs(file2_path)

# Print summaries
print_summary(file1_path, len(file1_logs) + sum(file1_removed.values()), file1_removed)
print_summary(file2_path, len(file2_logs) + sum(file2_removed.values()), file2_removed)

# Compare logs
comparisons = compare_logs(file1_logs, file2_logs)

# Write results to Excel
write_to_excel(comparisons, output_file)

print(f"Comparison completed and saved to {output_file}")

#----- old way -----

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
