import os
import numpy as np
from tkinter import Tk, Label, Button, Entry, filedialog
from PIL import Image

def file_to_images(file_path, output_folder, width, height):
    with open(file_path, 'rb') as file:
        data = file.read()

    hex_data = data.hex()
    pixel_count = width * height
    chunk_size = pixel_count * 3 * 2  # width x height pixels, 3 colors, 2 hex digits per color

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(0, len(hex_data), chunk_size):
        chunk = hex_data[i:i + chunk_size]
        if len(chunk) < chunk_size:
            chunk += '0' * (chunk_size - len(chunk))  # Pad with black pixels

        image_data = []
        for j in range(0, len(chunk), 6):
            r = int(chunk[j:j + 2], 16)
            g = int(chunk[j + 2:j + 4], 16)
            b = int(chunk[j + 4:j + 6], 16)
            image_data.append((r, g, b))

        image_data = np.array(image_data, dtype=np.uint8).reshape((height, width, 3))
        image = Image.fromarray(image_data, 'RGB')
        image.save(os.path.join(output_folder, f'image_{i // chunk_size}.png'))

    print(f'Images saved to {output_folder}')

def browse_file():
    filename = filedialog.askopenfilename(title="Select File")
    file_entry.delete(0, 'end')
    file_entry.insert(0, filename)

def browse_output_folder():
    foldername = filedialog.askdirectory(title="Select Output Folder")
    output_folder_entry.delete(0, 'end')
    output_folder_entry.insert(0, foldername)

def convert():
    file_path = file_entry.get()
    output_folder = output_folder_entry.get()
    try:
        width = int(width_entry.get())
        height = int(height_entry.get())
    except ValueError:
        result_label.config(text="Width and Height must be integers.", fg="red")
        return

    if file_path and output_folder and width > 0 and height > 0:
        file_to_images(file_path, output_folder, width, height)
        result_label.config(text="Conversion Complete!", fg="green")
    else:
        result_label.config(text="Please provide valid input file, output folder, and dimensions.", fg="red")

# GUI Setup
root = Tk()
root.title("File to Images Converter")

Label(root, text="Select File:").grid(row=0, column=0, padx=10, pady=5)
file_entry = Entry(root, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=5)
Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=10, pady=5)

Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=5)
output_folder_entry = Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=5)
Button(root, text="Browse", command=browse_output_folder).grid(row=1, column=2, padx=10, pady=5)

Label(root, text="Width:").grid(row=2, column=0, padx=10, pady=5)
width_entry = Entry(root, width=20)
width_entry.insert(0, "256")
width_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

Label(root, text="Height:").grid(row=3, column=0, padx=10, pady=5)
height_entry = Entry(root, width=20)
height_entry.insert(0, "256")
height_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

Button(root, text="Convert", command=convert).grid(row=4, column=0, columnspan=3, pady=15)

result_label = Label(root, text="")
result_label.grid(row=5, column=0, columnspan=3, pady=5)

root.mainloop()
