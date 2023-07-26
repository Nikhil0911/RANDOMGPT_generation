import os
import tkinter as tk
from tkinter import filedialog

class MatrixToolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Matrix Tool")
        self.geometry("400x300")

        self.file1 = None
        self.file2 = None
        self.folder = None
        self.matrix_data = [[0, 0], [0, 0]]

        self.create_widgets()

    def create_widgets(self):
        # File 1 input
        file1_label = tk.Label(self, text="Select File 1:")
        file1_label.pack()
        self.file1_btn = tk.Button(self, text="Choose File 1", command=self.select_file1)
        self.file1_btn.pack()

        # File 2 input
        file2_label = tk.Label(self, text="Select File 2:")
        file2_label.pack()
        self.file2_btn = tk.Button(self, text="Choose File 2", command=self.select_file2)
        self.file2_btn.pack()

        # Folder input
        folder_label = tk.Label(self, text="Select Folder:")
        folder_label.pack()
        self.folder_btn = tk.Button(self, text="Choose Folder", command=self.select_folder)
        self.folder_btn.pack()

        # Run button
        self.run_btn = tk.Button(self, text="Run", command=self.run_tool)
        self.run_btn.pack()

        # Dropdowns
        self.dropdown1 = tk.StringVar(self)
        self.dropdown2 = tk.StringVar(self)
        self.dropdown3 = tk.StringVar(self)

        self.dropdown1_label = tk.Label(self, text="Dropdown 1:")
        self.dropdown1_label.pack()
        self.dropdown1_menu = tk.OptionMenu(self, self.dropdown1, "")
        self.dropdown1_menu.pack()
        self.dropdown1_menu.config(state=tk.DISABLED)

        self.dropdown2_label = tk.Label(self, text="Dropdown 2:")
        self.dropdown2_label.pack()
        self.dropdown2_menu = tk.OptionMenu(self, self.dropdown2, "")
        self.dropdown2_menu.pack()
        self.dropdown2_menu.config(state=tk.DISABLED)

        self.dropdown3_label = tk.Label(self, text="Dropdown 3:")
        self.dropdown3_label.pack()
        self.dropdown3_menu = tk.OptionMenu(self, self.dropdown3, "")
        self.dropdown3_menu.pack()
        self.dropdown3_menu.config(state=tk.DISABLED)

        # Matrix display
        self.matrix_label = tk.Label(self, text="Matrix:")
        self.matrix_label.pack()
        self.matrix_display = tk.Label(self, text="")
        self.matrix_display.pack()

    def select_file1(self):
        self.file1 = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])

    def select_file2(self):
        self.file2 = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])

    def select_folder(self):
        self.folder = filedialog.askdirectory()

    def run_tool(self):
        # Perform some operations based on the selected files and folder
        # For this example, we'll just populate the dropdowns and matrix with sample data.
        self.dropdown1_menu.config(state=tk.NORMAL)
        self.dropdown1_menu["menu"].delete(0, "end")
        self.dropdown1_menu["menu"].add_command(label="Option 1", command=lambda: self.update_matrix(1, 1))
        self.dropdown1_menu["menu"].add_command(label="Option 2", command=lambda: self.update_matrix(1, 2))
        self.dropdown1_menu.config(state=tk.DISABLED)

        self.dropdown2_menu.config(state=tk.NORMAL)
        self.dropdown2_menu["menu"].delete(0, "end")
        self.dropdown2_menu["menu"].add_command(label="Option A", command=lambda: self.update_matrix(2, 1))
        self.dropdown2_menu["menu"].add_command(label="Option B", command=lambda: self.update_matrix(2, 2))
        self.dropdown2_menu.config(state=tk.DISABLED)

        self.dropdown3_menu.config(state=tk.NORMAL)
        self.dropdown3_menu["menu"].delete(0, "end")
        self.dropdown3_menu["menu"].add_command(label="Option X", command=lambda: self.update_matrix(3, 1))
        self.dropdown3_menu["menu"].add_command(label="Option Y", command=lambda: self.update_matrix(3, 2))
        self.dropdown3_menu.config(state=tk.DISABLED)

    def update_matrix(self, dropdown_num, option_num):
        self.matrix_data[dropdown_num-1][option_num-1] += 1
        self.matrix_display.config(text=str(self.matrix_data))

if __name__ == "__main__":
    app = MatrixToolApp()
    app.mainloop()
