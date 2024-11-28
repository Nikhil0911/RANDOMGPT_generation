import pandas as pd
import re

def clean_logs(file_path):
    logs = []
    removed_logs = 0
    with open(file_path, 'r') as file:
        for line_no, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue  # Remove blank lines
            if not re.match(r'^(?i)info|error', line):
                removed_logs += 1  # Count removed logs
                continue  # Remove lines not starting with info or error
            logs.append((line_no, line))
    return logs, removed_logs

def extract_log_parts(logs):
    log_parts = []
    for line_no, log in logs:
        log_type = log.split(' - ')[0].lower()  # info or error
        log_part = ' - '.join(log.split(' - ')[1:])  # everything after the log type
        log_parts.append((line_no, log_type, log_part))
    return log_parts

def find_matches(log_parts1, log_parts2):
    results = []
    for line_no1, log_type1, log_part1 in log_parts1:
        for line_no2, log_type2, log_part2 in log_parts2:
            exact_match = log_part1 == log_part2
            approx_match1 = log_part1 in log_part2
            approx_match2 = log_part2 in log_part1
            log_type_match = log_type1 == log_type2
            results.append((line_no1, log_type1, log_part1, line_no2, log_type2, log_part2,
                             log_type_match, exact_match, approx_match1, approx_match2))
    return results

def find_data_shapes(logs1, logs2):
    data_shapes1 = {re.search(r'\(\d+,\s*\d+\)', log[1]).group(0): log[1] for log in logs1 if re.search(r'\(\d+,\s*\d+\)', log[1])}
    data_shapes2 = {re.search(r'\(\d+,\s*\d+\)', log[1]).group(0): log[1] for log in logs2 if re.search(r'\(\d+,\s*\d+\)', log[1])}
    return data_shapes1, data_shapes2

def write_to_excel(results, data_shapes1, data_shapes2, output_file):
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_results = pd.DataFrame(results, columns=['Line no from file 1', 'Log type from file 1', 'Log part from file 1',
                                                    'Line no from file 2', 'Log type from file 2', 'Log part from file 2',
                                                    'Log type match', 'Log part exact match', 'Log part approx match 1',
                                                    'Log part approx match 2'])
        df_results.to_excel(writer, sheet_name='Log Comparisons', index=False)

        df_data_shapes1 = pd.DataFrame(data_shapes1.items(), columns=['Data shape from file 1', 'Log'])
        df_data_shapes2 = pd.DataFrame(data_shapes2.items(), columns=['Data shape from file 2', 'Log'])
        
        df_data_shapes1.to_excel(writer, sheet_name='Data Shapes from file 1', index=False)
        df_data_shapes2.to_excel(writer, sheet_name='Data Shapes from file 2', index=False)

def compare_logs(file1, file2, output_file):
    logs1, removed_logs1 = clean_logs(file1)
    logs2, removed_logs2 = clean_logs(file2)

    log_parts1 = extract_log_parts(logs1)
    log_parts2 = extract_log_parts(logs2)

    results = find_matches(log_parts1, log_parts2)

    data_shapes1, data_shapes2 = find_data_shapes(logs1, logs2)

    write_to_excel(results, data_shapes1, data_shapes2, output_file)

    print(f"Total logs in file 1: {len(logs1) + removed_logs1}")
    print(f"Logs removed from file 1: {removed_logs1}")
    print(f"Total logs in file 2: {len(logs2) + removed_logs2}")
    print(f"Logs removed from file 2: {removed_logs2}")
