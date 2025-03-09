import os
import numpy as np
from tkinter import Tk, Label, Button, Entry, Text, filedialog, END
from PIL import Image

def text_to_images(text, output_folder):
    hex_data = text.encode('utf-8').hex()
    pixel_count = 512 * 512
    chunk_size = pixel_count * 3 * 2  # 512x512 pixels, 3 colors, 2 hex digits per color

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
        
        image_data = np.array(image_data, dtype=np.uint8).reshape((512, 512, 3))
        image = Image.fromarray(image_data, 'RGB')
        image.save(os.path.join(output_folder, f'image_{i // chunk_size}.png'))
    
    print(f'Images saved to {output_folder}')

def browse_output_folder():
    foldername = filedialog.askdirectory(title="Select Output Folder")
    output_folder_entry.delete(0, 'end')
    output_folder_entry.insert(0, foldername)

def convert():
    text = text_entry.get("1.0", END)
    output_folder = output_folder_entry.get()
    if text and output_folder:
        text_to_images(text, output_folder)
        result_label.config(text="Conversion Complete!", fg="green")
    else:
        result_label.config(text="Please enter text and select an output folder.", fg="red")

# GUI Setup
root = Tk()
root.title("Text to 512x512 Images Converter")

Label(root, text="Enter Text:").grid(row=0, column=0, padx=10, pady=10)
text_entry = Text(root, width=50, height=10)
text_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

Label(root, text="Select Output Folder:").grid(row=2, column=0, padx=10, pady=10)
output_folder_entry = Entry(root, width=50)
output_folder_entry.grid(row=2, column=1, padx=10, pady=10)
Button(root, text="Browse", command=browse_output_folder).grid(row=2, column=2, padx=10, pady=10)

Button(root, text="Convert", command=convert).grid(row=3, column=0, columnspan=3, pady=20)

result_label = Label(root, text="")
result_label.grid(row=4, column=0, columnspan=3)

root.mainloop()
