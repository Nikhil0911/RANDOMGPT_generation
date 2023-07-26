import os
import tkinter as tk
from tkinter import filedialog

class InputFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Matrix Tool")
        self.pack()

        self.file1 = None
        self.file2 = None
        self.folder = None

        self.create_widgets()

    def create_widgets(self):
        file1_label = tk.Label(self, text="Select File 1:")
        file1_label.pack()
        self.file1_btn = tk.Button(self, text="Choose File 1", command=self.select_file1)
        self.file1_btn.pack()

        file2_label = tk.Label(self, text="Select File 2:")
        file2_label.pack()
        self.file2_btn = tk.Button(self, text="Choose File 2", command=self.select_file2)
        self.file2_btn.pack()

        folder_label = tk.Label(self, text="Select Folder:")
        folder_label.pack()
        self.folder_btn = tk.Button(self, text="Choose Folder", command=self.select_folder)
        self.folder_btn.pack()

        self.run_btn = tk.Button(self, text="Run", command=self.open_matrix_frame)
        self.run_btn.pack()

    def select_file1(self):
        self.file1 = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])

    def select_file2(self):
        self.file2 = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])

    def select_folder(self):
        self.folder = filedialog.askdirectory()

    def open_matrix_frame(self):
        if self.file1 and self.file2 and self.folder:
            self.master.withdraw()  # Hide the current frame
            matrix_window = tk.Toplevel(self.master)  # Create a new top-level window
            matrix_frame = MatrixFrame(matrix_window, self.file1, self.file2, self.folder)
        else:
            tk.messagebox.showwarning("Input Error", "Please select File 1, File 2, and Folder first!")

class MatrixFrame(tk.Frame):
    def __init__(self, master, file1, file2, folder):
        super().__init__(master)
        self.master = master
        self.master.title("Matrix Frame")
        self.pack()

        self.file1 = file1
        self.file2 = file2
        self.folder = folder
        self.matrix_data = [[0, 0], [0, 0]]

        self.create_widgets()

    def create_widgets(self):
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

        self.matrix_label = tk.Label(self, text="Matrix:")
        self.matrix_label.pack()
        self.matrix_display = tk.Label(self, text="")
        self.matrix_display.pack()

        self.populate_dropdowns()

    def populate_dropdowns(self):
        # For this example, we'll populate the dropdowns with sample data.
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
    root = tk.Tk()
    input_frame = InputFrame(root)
    root.mainloop()
