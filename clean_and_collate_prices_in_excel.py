import pandas as pd

file_path = "your_excel_file.xlsx"
xls = pd.ExcelFile(file_path)

final_data = []

for sheet in xls.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet, header=None)

    for row in range(len(df)):
        cell = str(df.iloc[row, 0]).strip().lower()

        # Anchor on BarTp
        if cell == "bartp":
            try:
                ticker = df.iloc[row + 2, 0]
                header = str(df.iloc[row + 3, 0]).strip().lower()

                if header != "dates":
                    continue

                data = df.iloc[row + 4:, 0:3]
                data.columns = ["date", "open", "close"]
                data["ticker"] = ticker

                data = data.dropna(subset=["date"])
                final_data.append(data)

            except Exception:
                continue

final_df = pd.concat(final_data, ignore_index=True)
final_df = final_df[["ticker", "date", "open", "close"]]

final_df.to_excel("combined_output.xlsx", index=False)

#------------------------v2----------------------------

import pandas as pd

input_file = "your_input_file.xlsx"
output_file = "combined_output.xlsx"

xls = pd.ExcelFile(input_file)

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    for sheet in xls.sheet_names:
        df = pd.read_excel(input_file, sheet_name=sheet, header=None)
        nrows, ncols = df.shape

        sheet_data = []

        for r in range(nrows):
            for c in range(ncols):
                cell = str(df.iloc[r, c]).strip().lower()

                # Detect BarTp anywhere
                if cell == "bartp":
                    try:
                        ticker = df.iloc[r + 2, c]
                        header = str(df.iloc[r + 3, c]).strip().lower()

                        if header != "dates":
                            continue

                        block = df.iloc[r + 4:, c:c + 3]
                        block.columns = ["date", "open", "close"]
                        block["ticker"] = ticker

                        # Stop when date column ends
                        block = block.dropna(subset=["date"])

                        # Optional numeric safety
                        block = block[pd.to_numeric(block["open"], errors="coerce").notna()]

                        sheet_data.append(block)

                    except Exception:
                        continue

        if sheet_data:
            final_sheet_df = pd.concat(sheet_data, ignore_index=True)
            final_sheet_df = final_sheet_df[
                ["ticker", "date", "open", "close"]
            ]

            final_sheet_df.to_excel(
                writer,
                sheet_name=sheet,
                index=False
            )

