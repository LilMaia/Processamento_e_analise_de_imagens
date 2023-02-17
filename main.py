import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps

zoom_level = 0
zoom_size = 400

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("TIFF files", "*.tiff")])
    if file_path:
        try:
            global image
            image = Image.open(file_path)
            global image_resized
            image_resized = image.resize((600, 600), Image.Resampling.LANCZOS)
            update_image(image_resized)
        except Exception as e:
            messagebox.showerror("Error", "Failed to open image: {}".format(e))

def update_image(image):
    global image_label, image_tk
    image_tk = ImageTk.PhotoImage(image)
    image_label.config(image=image_tk)

def zoom_in():
    global zoom_level
    zoom_level += 1
    update_zoomed_image()

def zoom_out():
    global zoom_level
    zoom_level = max(0, zoom_level - 1)
    update_zoomed_image()

def update_zoomed_image():
    global zoom_level, zoom_size, image, image_resized, image_label, image_tk
    zoomed_image = image.resize((int(image.width * (1 + zoom_level * 0.1)), int(image.height * (1 + zoom_level * 0.1))), Image.Resampling.LANCZOS)
    x = max(0, image_label.winfo_width()//2 - zoom_size//2)
    y = max(0, image_label.winfo_height()//2 - zoom_size//2)
    cropped_image = zoomed_image.crop((x, y, x + zoom_size, y + zoom_size))
    image_tk = ImageTk.PhotoImage(cropped_image)
    image_label.config(image=image_tk)

def adjust_contrast(min_value, max_value):
    global image, image_resized
    if image.mode not in ('L', 'P'):
        image = image.convert('L')
    image = ImageOps.autocontrast(image, cutoff=(min_value, max_value))
    update_image(image)

root = tk.Tk()
root.title("Image Viewer")

image_label = tk.Label(root)
image_label.pack()

open_button = tk.Button(root, text="Open", command=open_image)
open_button.pack()

zoom_in_button = tk.Button(root, text="Zoom In", command=zoom_in)
zoom_in_button.pack()

zoom_out_button = tk.Button(root, text="Zoom Out", command=zoom_out)
zoom_out_button.pack()

min_value_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Min Value")
min_value_slider.pack()

max_value_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Max Value")
max_value_slider.pack()

adjust_button = tk.Button(root, text="Adjust Contrast", command=lambda: adjust_contrast(min_value_slider.get(), max_value_slider.get()))
adjust_button.pack()

root.mainloop()