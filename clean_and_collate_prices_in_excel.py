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
