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
