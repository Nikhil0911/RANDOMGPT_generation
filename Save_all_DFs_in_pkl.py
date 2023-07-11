import pandas as pd

def read_excel_into_dfs(excel_file):
    # Read all sheets into a dictionary of DataFrames
    dfs = pd.read_excel(excel_file, sheet_name=None)

    # Save each DataFrame as a pickle file
    for sheet_name, df in dfs.items():
        pickle_file = f"{sheet_name}.pkl"
        df.to_pickle(pickle_file)
        print(f"Saved DataFrame '{sheet_name}' to {pickle_file}")

    return dfs

def load_df_from_pickle(pickle_file):
    # Load a DataFrame from a pickle file
    return pd.read_pickle(pickle_file)

# Read the Excel file into DataFrames and save as pickle files
excel_file = "path/to/your/excel_file.xlsx"
dataframes = read_excel_into_dfs(excel_file)

# Load a desired DataFrame from a pickle file
desired_df_name = "desired_sheet_name"
pickle_file = f"{desired_df_name}.pkl"
desired_df = load_df_from_pickle(pickle_file)
