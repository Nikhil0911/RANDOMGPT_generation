import tkinter as tk

class IncrementFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.counter = 0
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Counter: 0")
        self.label.pack(pady=10)

        self.button = tk.Button(self, text="Increment", command=self.increment_counter)
        self.button.pack()

    def increment_counter(self):
        self.counter += 1
        self.label.config(text=f"Counter: {self.counter}")

class DisplayFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Counter: 0")
        self.label.pack(pady=10)

    def update_counter(self, counter):
        self.label.config(text=f"Counter: {counter}")

if __name__ == "__main__":
    app = tk.Tk()
    app.title("Multiple Frames Example")

    increment_frame = IncrementFrame(app)
    increment_frame.pack(pady=20)

    display_frame = DisplayFrame(app)
    display_frame.pack()

    # Function to update the display frame with the current counter value
    def update_display_frame_counter():
        display_frame.update_counter(increment_frame.counter)

    # Create a button to update the display frame with the current counter value
    update_button = tk.Button(app, text="Update Display", command=update_display_frame_counter)
    update_button.pack(pady=10)

    app.mainloop()
