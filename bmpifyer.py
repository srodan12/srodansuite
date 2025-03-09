import os
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from hilbertcurve.hilbertcurve import HilbertCurve

def read_binary_file(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    return data

def convert_to_rgb(data):
    pixels = []
    for i in range(0, len(data) - 2, 3):
        r, g, b = data[i], data[i + 1], data[i + 2]
        if (r, g, b) != (0, 0, 0):  # Skip black pixels
            pixels.append((r, g, b))
    return pixels

def create_hilbert_curve(order, dimensions):
    curve = HilbertCurve(order, dimensions)
    total_points = 2 ** (order * dimensions)
    return [curve.point_from_distance(i) for i in range(total_points)]

def create_image(pixels, order):
    curve_points = create_hilbert_curve(order, 2)
    grid_size = int(len(curve_points) ** 0.5)

    image = Image.new('RGB', (grid_size, grid_size))
    pixel_map = image.load()

    for i, (x, y) in enumerate(curve_points):
        if i < len(pixels):
            pixel_map[x, y] = pixels[i]
        else:
            pixel_map[x, y] = (0, 0, 0)  # Fill remaining with black

    return image

def select_file_and_save():
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        binary_data = read_binary_file(file_path)

        # Convert binary data to RGB pixels and remove 000000 instances
        pixels = convert_to_rgb(binary_data)

        # Determine Hilbert curve order based on the number of pixels
        order = int(np.ceil(np.log2(np.sqrt(len(pixels)))))

        # Create and save the image
        image = create_image(pixels, order)
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP files", "*.bmp")])
        if save_path:
            image.save(save_path, format="BMP")
            messagebox.showinfo("Success", f"Image saved as {save_path}")
        else:
            messagebox.showwarning("Canceled", "Save operation was canceled.")
    else:
        messagebox.showwarning("Canceled", "File selection was canceled.")

def main():
    root = tk.Tk()
    root.title("Binary to Hilbert Curve BMP Converter")

    tk.Label(root, text="Convert a binary file to a BMP image using a Hilbert curve").pack(pady=10)

    tk.Button(root, text="Select File and Save as BMP", command=select_file_and_save).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
