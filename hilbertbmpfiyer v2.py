import os
import numpy as np
import logging
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from hilbertcurve.hilbertcurve import HilbertCurve

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_binary_file(file_path):
    logging.info(f"Reading binary file from {file_path}")
    with open(file_path, 'rb') as file:
        data = file.read()
    logging.info(f"Finished reading {len(data)} bytes from file")
    return data

def convert_to_rgb(data):
    logging.info("Converting binary data to RGB pixels")
    pixels = []
    for i in range(0, len(data) - 2, 3):
        r, g, b = data[i], data[i + 1], data[i + 2]
        if (r, g, b) != (0, 0, 0):  # Skip black pixels
            pixels.append((r, g, b))
    logging.info(f"Converted to {len(pixels)} RGB pixels after removing black pixels")
    return pixels

def create_hilbert_curve(order, dimensions):
    logging.info(f"Generating Hilbert curve of order {order}")
    curve = HilbertCurve(order, dimensions)
    total_points = 2 ** (order * dimensions)
    logging.info(f"Total points in Hilbert curve: {total_points}")
    return [curve.point_from_distance(i) for i in range(total_points)]

def create_image(pixels, order):
    logging.info(f"Creating image with Hilbert curve order {order}")
    curve_points = create_hilbert_curve(order, 2)
    grid_size = int(len(curve_points) ** 0.5)
    logging.info(f"Image grid size: {grid_size}x{grid_size}")

    image = Image.new('RGB', (grid_size, grid_size))
    pixel_map = image.load()

    for i, (x, y) in enumerate(curve_points):
        if i < len(pixels):
            pixel_map[x, y] = pixels[i]
        else:
            pixel_map[x, y] = (0, 0, 0)  # Fill remaining with black

    logging.info("Image creation complete")
    return image

def select_file_and_save():
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        logging.info(f"File selected: {file_path}")
        binary_data = read_binary_file(file_path)

        # Convert binary data to RGB pixels and remove 000000 instances
        pixels = convert_to_rgb(binary_data)

        # Determine Hilbert curve order based on the number of pixels
        order = int(np.ceil(np.log2(np.sqrt(len(pixels)))))
        logging.info(f"Calculated Hilbert curve order: {order}")

        # Create and save the image
        image = create_image(pixels, order)
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP files", "*.bmp")])
        if save_path:
            image.save(save_path, format="BMP")
            logging.info(f"Image saved to {save_path}")
            messagebox.showinfo("Success", f"Image saved as {save_path}")
        else:
            logging.warning("Save operation was canceled.")
            messagebox.showwarning("Canceled", "Save operation was canceled.")
    else:
        logging.warning("File selection was canceled.")
        messagebox.showwarning("Canceled", "File selection was canceled.")

def main():
    root = tk.Tk()
    root.title("Binary to Hilbert Curve BMP Converter")

    tk.Label(root, text="Convert a binary file to a BMP image using a Hilbert curve").pack(pady=10)

    tk.Button(root, text="Select File and Save as BMP", command=select_file_and_save).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
