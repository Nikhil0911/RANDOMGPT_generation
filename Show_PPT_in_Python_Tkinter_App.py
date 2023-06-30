import tkinter as tk
from tkinter import ttk
import win32com.client as win32

class PowerPointViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PowerPoint Viewer")
        
        self.ppt_file = None
        self.slides = None
        self.current_slide_index = 0
        
        self.create_widgets()
    
    def create_widgets(self):
        # File selection frame
        file_frame = ttk.Frame(self.root)
        file_frame.pack(pady=10)
        
        file_label = ttk.Label(file_frame, text="PowerPoint File:")
        file_label.pack(side="left")
        
        self.file_entry = ttk.Entry(file_frame, width=30)
        self.file_entry.pack(side="left")
        
        file_button = ttk.Button(file_frame, text="Browse", command=self.open_ppt_file)
        file_button.pack(side="left")
        
        # Slide navigation frame
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(pady=10)
        
        prev_button = ttk.Button(nav_frame, text="Previous", command=self.show_previous_slide)
        prev_button.pack(side="left")
        
        next_button = ttk.Button(nav_frame, text="Next", command=self.show_next_slide)
        next_button.pack(side="left")
        
        # Slide display frame
        self.slide_frame = ttk.Frame(self.root)
        self.slide_frame.pack(pady=10)
        
        self.slide_label = ttk.Label(self.slide_frame, text="")
        self.slide_label.pack()
    
    def open_ppt_file(self):
        self.ppt_file = tk.filedialog.askopenfilename(filetypes=[("PowerPoint Files", "*.pptx")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, self.ppt_file)
        
        if self.ppt_file:
            self.open_ppt_slides()
    
    def open_ppt_slides(self):
        ppt_app = win32.gencache.EnsureDispatch("PowerPoint.Application")
        presentation = ppt_app.Presentations.Open(self.ppt_file)
        self.slides = presentation.Slides
    
    def show_previous_slide(self):
        if self.slides and self.current_slide_index > 0:
            self.current_slide_index -= 1
            self.show_slide()
    
    def show_next_slide(self):
        if self.slides and self.current_slide_index < self.slides.Count - 1:
            self.current_slide_index += 1
            self.show_slide()
    
    def show_slide(self):
        if self.slides:
            slide = self.slides[self.current_slide_index + 1]
            slide.Export("temp.png", "PNG")  # Export slide as an image
            
            # Load the exported image and display it in the frame
            image = tk.PhotoImage(file="temp.png")
            self.slide_label.configure(image=image)
            self.slide_label.image = image
    
root = tk.Tk()
app = PowerPointViewer(root)
root.mainloop()
