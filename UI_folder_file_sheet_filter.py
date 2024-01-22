import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import openpyxl
import pandas as pd

class FileSelectorApp:
    def __init__(self, master):
        self.master = master
        master.title("File Selector App")

        # Create and place a label for the folder selection
        self.label = tk.Label(master, text="Select a folder:")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        # Create and place an entry widget for folder path
        self.folder_var = tk.StringVar()
        self.folder_entry = tk.Entry(master, textvariable=self.folder_var, width=30)
        self.folder_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create and place a button to select a folder
        self.select_folder_button = tk.Button(master, text="Select Folder", command=self.select_folder)
        self.select_folder_button.grid(row=0, column=2, padx=10, pady=10)

        # Create and place a dropdown menu for Excel files
        self.file_dropdown = ttk.Combobox(master, width=27)
        self.file_dropdown.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Set an initial value for the dropdown
        self.file_dropdown.set("Select a folder first")

        # Create and place a dropdown menu for sheets
        self.sheet_dropdown = ttk.Combobox(master, width=27)
        self.sheet_dropdown.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Set an initial value for the dropdown
        self.sheet_dropdown.set("Select an Excel file first")

        # Create and place a dropdown menu for region-based unique values
        self.region_dropdown = ttk.Combobox(master, width=27, state="readonly", multiple=True)
        self.region_dropdown.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # Create and place a dropdown menu for asset-based unique values
        self.asset_dropdown = ttk.Combobox(master, width=27, state="readonly", multiple=True)
        self.asset_dropdown.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Bind an event to the folder entry to trigger actions on folder selection
        self.folder_entry.bind("<FocusOut>", self.on_folder_selected)

        # Bind events to trigger actions on selection in other dropdowns
        self.file_dropdown.bind("<<ComboboxSelected>>", self.read_sheets)
        self.sheet_dropdown.bind("<<ComboboxSelected>>", self.retrieve_values)
        self.region_dropdown.bind("<<ComboboxSelected>>", self.filter_dataframe)

    def select_folder(self):
        folder_path = tk.filedialog.askdirectory()
        if folder_path:
            self.folder_var.set(folder_path)
            self.on_folder_selected(None)  # Trigger actions on folder selection

    def on_folder_selected(self, event):
        folder_path = self.folder_var.get()

        if os.path.exists(folder_path):
            # Filter only xlsx files
            file_list = [file for file in os.listdir(folder_path) if file.lower().endswith('.xlsx')]
            self.file_dropdown['values'] = file_list
        else:
            self.file_dropdown.set("Select a valid folder")

        # Reset other dropdowns
        self.sheet_dropdown.set("Select an Excel file first")
        self.region_dropdown.set("")
        self.asset_dropdown.set("")

    def read_sheets(self, event):
        selected_file = self.file_dropdown.get()
        folder_path = self.folder_var.get()
        file_path = os.path.join(folder_path, selected_file)

        if os.path.exists(file_path):
            try:
                workbook = openpyxl.load_workbook(file_path, read_only=True)
                sheet_names = workbook.sheetnames

                # Populate sheet dropdown with sheet names
                self.sheet_dropdown['values'] = sheet_names
                self.sheet_dropdown.set(sheet_names[0])  # Select the first sheet by default
            except Exception as e:
                messagebox.showerror("Error", f"Error reading sheets: {str(e)}")
        else:
            messagebox.showerror("Error", "Select a valid Excel file")

        # Reset other dropdowns
        self.region_dropdown.set("")
        self.asset_dropdown.set("")

    def retrieve_values(self, event):
        selected_sheet = self.sheet_dropdown.get()
        selected_file = self.file_dropdown.get()
        folder_path = self.folder_var.get()
        file_path = os.path.join(folder_path, selected_file)

        if os.path.exists(file_path) and selected_sheet:
            try:
                df = pd.read_excel(file_path, sheet_name=selected_sheet)
                region_field = "Region"  # Replace with the actual name of your region-based field
                unique_values = df[region_field].unique()

                # Populate region dropdown with unique values
                self.region_dropdown['values'] = unique_values
                self.region_dropdown.set(tuple(unique_values))  # Set as multiple selections
            except Exception as e:
                messagebox.showerror("Error", f"Error retrieving values: {str(e)}")
        else:
            messagebox.showerror("Error", "Select a valid sheet")

        # Reset other dropdowns
        self.asset_dropdown.set("")

    def filter_dataframe(self, event):
        selected_regions = self.region_dropdown.get()
        selected_sheet = self.sheet_dropdown.get()
        selected_file = self.file_dropdown.get()
        folder_path = self.folder_var.get()
        file_path = os.path.join(folder_path, selected_file)

        if os.path.exists(file_path) and selected_sheet and selected_regions:
            try:
                df = pd.read_excel(file_path, sheet_name=selected_sheet)
                region_field = "Region"  # Replace with the actual name of your region-based field

                # Filter DataFrame based on selected regions
                filtered_df = df[df[region_field].isin(selected_regions)]

                # Populate asset dropdown with unique values based on filtered DataFrame
                asset_field = "Asset"  # Replace with the actual name of your asset field
                unique_assets = filtered_df[asset_field].unique()
                self.asset_dropdown['values'] = unique_assets
                self.asset_dropdown.set(tuple(unique_assets))  # Set as multiple selections
            except Exception as e:
                messagebox.showerror("Error", f"Error filtering DataFrame: {str(e)}")
        else:
            messagebox.showerror("Error", "Select valid sheet and region(s)")

    def show_filtered_dataframe(self, df):
        # Create a new window to display the filtered DataFrame
        new_window = tk.Toplevel(self.master)
        new_window.title("Filtered DataFrame")

        # Create a scrolled text widget to display the DataFrame
        text_widget = scrolledtext.ScrolledText(new_window, width=80, height=20, wrap=tk.WORD)
        text_widget.pack(padx=10, pady=10)

        # Insert the DataFrame into the text widget
        text_widget.insert(tk.END, df.to_string(index=False))

# Create the main window
root = tk.Tk()

# Instantiate the FileSelectorApp class
app = FileSelectorApp(root)

# Run the Tkinter event loop
root.mainloop()
