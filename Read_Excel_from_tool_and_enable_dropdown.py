import tkinter as tk
from tkinter import filedialog
import pandas as pd

class ExcelReaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Excel Reader")

        self.frame = tk.Frame(self.master, padx=20, pady=20)
        self.frame.pack()

        self.browse_button = tk.Button(self.frame, text="Browse Excel File", command=self.browse_file)
        self.browse_button.pack()

        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Select an option")
        self.dropdown_menu = tk.OptionMenu(self.frame, self.dropdown_var, "Select an option")
        self.dropdown_menu.pack()
        self.dropdown_menu.config(state="disabled")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            df = pd.read_excel(file_path)
            self.enable_dropdown(df)

    def enable_dropdown(self, df):
        unique_values = df.iloc[:, 0].unique().tolist()
        self.dropdown_menu['menu'].delete(0, 'end')
        for value in unique_values:
            self.dropdown_menu['menu'].add_command(label=value, command=tk._setit(self.dropdown_var, value))
        self.dropdown_menu.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelReaderApp(root)
    root.mainloop()
