import tkinter as tk

class CustomDropdown(tk.Toplevel):
    def __init__(self, master, options):
        super().__init__(master)
        self.master = master
        self.options = options

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entry_var)
        self.entry.pack()

        self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)  # Set the selectmode to MULTIPLE
        self.listbox.pack()

        for item in self.options:
            self.listbox.insert(tk.END, item)

        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

    def on_listbox_select(self, event):
        selected_indices = self.listbox.curselection()
        selected_items = [self.listbox.get(index) for index in selected_indices]
        self.entry_var.set(", ".join(selected_items))  # Show multiple selections in the entry widget

class DropdownApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Custom Dropdown Example")

        self.options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entry_var)
        self.entry.pack()

        self.show_button = tk.Button(self, text="Show Selected Item", command=self.show_selected_item)
        self.show_button.pack()

        self.create_dropdown_button = tk.Button(self, text="Open Dropdown", command=self.create_dropdown)
        self.create_dropdown_button.pack()

    def show_selected_item(self):
        selected_item = self.entry_var.get()
        print("Selected Items:", selected_item)

    def create_dropdown(self):
        dropdown = CustomDropdown(self, self.options)

if __name__ == "__main__":
    app = DropdownApp()
    app.mainloop()
