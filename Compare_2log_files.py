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
