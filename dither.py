import numpy as np
from PIL import Image, ImageOps, ImageTk
import tkinter as tk
from tkinter import filedialog, Label, Button, OptionMenu, StringVar, Canvas, NW

# Define color palettes
palettes = {
    'CGA': [
        (0, 0, 0), (85, 85, 85), (170, 170, 170), (255, 255, 255), # Grayscale
        (0, 0, 170), (0, 170, 170), (170, 0, 170), (170, 170, 0), # Primary colors
        (0, 170, 0), (170, 0, 0), (170, 85, 0), (0, 85, 170), # Secondary colors
        (85, 0, 170), (85, 170, 0), (0, 170, 85), (85, 85, 85) # Tertiary colors
    ],
    'ZX Spectrum': [
        (0, 0, 0), (0, 0, 215), (215, 0, 0), (215, 0, 215),
        (0, 215, 0), (0, 215, 215), (215, 215, 0), (215, 215, 215),
        (0, 0, 0), (0, 0, 255), (255, 0, 0), (255, 0, 255),
        (0, 255, 0), (0, 255, 255), (255, 255, 0), (255, 255, 255)
    ],
    'NES': [
        (124, 124, 124), (0, 0, 252), (0, 0, 188), (68, 40, 188),
        (148, 0, 132), (168, 0, 32), (168, 16, 0), (136, 20, 0),
        (80, 48, 0), (0, 120, 0), (0, 104, 0), (0, 88, 0),
        (0, 64, 88), (0, 0, 0), (0, 0, 0), (0, 0, 0)
    ]
}

def apply_dithering(image, algorithm, palette):
    # Convert image to grayscale if necessary
    if image.mode != 'L':
        image = ImageOps.grayscale(image)

    if algorithm == 'Floyd-Steinberg':
        return floyd_steinberg_dithering(image, palette)
    elif algorithm == 'Ordered':
        return ordered_dithering(image, palette)
    elif algorithm == 'Atkinson':
        return atkinson_dithering(image, palette)
    else:
        return image

def floyd_steinberg_dithering(image, palette):
    img = np.array(image)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            old_pixel = img[y, x]
            new_pixel = find_closest_palette_color(old_pixel, palette)
            img[y, x] = new_pixel
            quant_error = old_pixel - new_pixel
            if x + 1 < img.shape[1]:
                img[y, x + 1] += quant_error * 7 / 16
            if y + 1 < img.shape[0]:
                if x - 1 >= 0:
                    img[y + 1, x - 1] += quant_error * 3 / 16
                img[y + 1, x] += quant_error * 5 / 16
                if x + 1 < img.shape[1]:
                    img[y + 1, x + 1] += quant_error * 1 / 16
    return Image.fromarray(img.astype('uint8'))

def ordered_dithering(image, palette):
    img = np.array(image)
    threshold_matrix = np.array([
        [8, 3, 4, 9],
        [6, 1, 2, 7],
        [4, 9, 8, 3],
        [2, 7, 6, 1]
    ]) / 10.0 * 255
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            old_pixel = img[y, x]
            new_pixel = find_closest_palette_color(old_pixel + threshold_matrix[y % 4, x % 4], palette)
            img[y, x] = new_pixel
    return Image.fromarray(img.astype('uint8'))

def atkinson_dithering(image, palette):
    img = np.array(image)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            old_pixel = img[y, x]
            new_pixel = find_closest_palette_color(old_pixel, palette)
            img[y, x] = new_pixel
            quant_error = old_pixel - new_pixel
            if x + 1 < img.shape[1]:
                img[y, x + 1] += quant_error * 1 / 8
            if x + 2 < img.shape[1]:
                img[y, x + 2] += quant_error * 1 / 8
            if y + 1 < img.shape[0]:
                if x - 1 >= 0:
                    img[y + 1, x - 1] += quant_error * 1 / 8
                img[y + 1, x] += quant_error * 1 / 8
                if x + 1 < img.shape[1]:
                    img[y + 1, x + 1] += quant_error * 1 / 8
            if y + 2 < img.shape[0]:
                img[y + 2, x] += quant_error * 1 / 8
    return Image.fromarray(img.astype('uint8'))

def find_closest_palette_color(old_pixel, palette):
    palette_array = np.array(palette)
    diff = np.abs(palette_array - old_pixel)
    distance = np.sum(diff, axis=1)
    return palette_array[np.argmin(distance)]

def upscale_nearest_neighbor(image, scale):
    small = np.array(image)
    h, w = small.shape[:2]
    large = np.zeros((h * scale, w * scale), dtype=small.dtype)
    for y in range(h):
        for x in range(w):
            large[y*scale:(y+1)*scale, x*scale:(x+1)*scale] = small[y, x]
    return Image.fromarray(large)

def open_image():
    filename = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if filename:
        original_image = Image.open(filename)
        image_label.config(text=f"Selected Image: {filename}")
        original_image.thumbnail((256, 256))
        tk_image = ImageTk.PhotoImage(original_image)
        image_canvas.create_image(0, 0, anchor=NW, image=tk_image)
        image_canvas.image = tk_image
        return original_image
    return None

def save_image(image):
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if filename:
        image.save(filename)
        result_label.config(text=f"Image saved to {filename}")

def apply_and_preview():
    selected_algorithm = algorithm_var.get()
    selected_palette = palette_var.get()
    if not selected_algorithm:
        result_label.config(text="Please select a dithering algorithm.")
        return

    image = open_image()
    if image is None:
        result_label.config(text="Please select an image file.")
        return

    dithered_image = apply_dithering(image, selected_algorithm, palettes[selected_palette])
    upscaled_image = upscale_nearest_neighbor(dithered_image, 4)
    preview_image(upscaled_image)
    save_image(upscaled_image)
    result_label.config(text="Conversion Complete!")

def preview_image(image):
    image.thumbnail((512, 512))
    tk_image = ImageTk.PhotoImage(image)
    preview_canvas.create_image(0, 0, anchor=NW, image=tk_image)
    preview_canvas.image = tk_image

# GUI Setup
root = tk.Tk()
root.title("Image Dithering and Upscaling")

Label(root, text="Select Dithering Algorithm:").grid(row=0, column=0, padx=10, pady=10)
algorithm_var = StringVar(root)
algorithms = ['Floyd-Steinberg', 'Ordered', 'Atkinson']
algorithm_menu = OptionMenu(root, algorithm_var, *algorithms)
algorithm_menu.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Select Color Palette:").grid(row=1, column=0, padx=10, pady=10)
palette_var = StringVar(root)
palette_menu = OptionMenu(root, palette_var, *palettes.keys())
palette_menu.grid(row=1, column=1, padx=10, pady=10)

Button(root, text="Select Image and Apply Dithering", command=apply_and_preview).grid(row=2, column=0, columnspan=2, pady=20)

image_label = Label(root, text="No image selected")
image_label.grid(row=3, column=0, columnspan=2)

image_canvas = Canvas(root, width=256, height=256)
image_canvas.grid(row=4, column=0, columnspan=2)

preview_canvas = Canvas(root, width=512, height=512)
preview_canvas.grid(row=5, column=0, columnspan=2)

result_label = Label(root, text="")
result_label.grid(row=6, column=0, columnspan=2)

root.mainloop()
