import pandas as pd
import re

def parse_log_line(line):
    # Parse log line into type, timestamp, and message
    match = re.match(r"(Info|Error) - (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (.*)", line)
    if match:
        return match.groups()
    else:
        return None

def compare_logs(file1, file2, excel_file):
    df = pd.DataFrame(columns=['Line no from file 1', 'Log type from file 1', 'Log part from file 1',
                               'Line no from file 2', 'Log type from file 2', 'Log part from file 2',
                               'Log type match', 'Log part exact match', 'Log part approx match 1',
                               'Log part approx match 2', 'Data from file 1', 'Data from file 2'])

    # Read log files
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        logs1 = [line.strip() for line in f1 if line.strip() and line.startswith(('Info', 'Error'))]
        logs2 = [line.strip() for line in f2 if line.strip() and line.startswith(('Info', 'Error'))]

    # Print initial log counts
    print(f"Total logs in file 1: {len(logs1)}")
    print(f"Total logs in file 2: {len(logs2)}")

    # Compare logs
    for i, log1 in enumerate(logs1):
        parsed_log1 = parse_log_line(log1)
        if parsed_log1:
            for j, log2 in enumerate(logs2):
                parsed_log2 = parse_log_line(log2)
                if parsed_log2:
                    df = df.append({
                        'Line no from file 1': i+1,
                        'Log type from file 1': parsed_log1[0],
                        'Log part from file 1': parsed_log1[2],
                        'Line no from file 2': j+1,
                        'Log type from file 2': parsed_log2[0],
                        'Log part from file 2': parsed_log2[2],
                        'Log type match': parsed_log1[0] == parsed_log2[0],
                        'Log part exact match': parsed_log1[2] == parsed_log2[2],
                        # Implement approximate match logic here (e.g., using fuzzywuzzy)
                        'Log part approx match 1': ...,
                        'Log part approx match 2': ...,
                        'Data from file 1': ...,
                        'Data from file 2': ...
                    }, ignore_index=True)

    # Write to Excel
    df.to_excel(excel_file, index=False)

# Example usage
compare_logs('log1.txt', 'log2.txt', 'excel_file.xlsx')
