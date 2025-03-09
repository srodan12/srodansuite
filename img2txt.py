import os
import numpy as np
from tkinter import Tk, Label, Button, Entry, filedialog, Text, END
from PIL import Image

def image_to_text(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    data = np.array(img).flatten()
    hex_data = ''.join([f'{value:02x}' for value in data])
    
    # Convert hex to text
    bytes_data = bytes.fromhex(hex_data)
    text = bytes_data.decode('utf-8', errors='replace')  # Replace errors with a placeholder character
    return text

def browse_image():
    filename = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    image_entry.delete(0, 'end')
    image_entry.insert(0, filename)

def save_text(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

def browse_output_file():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    output_entry.delete(0, 'end')
    output_entry.insert(0, filename)

def convert():
    image_path = image_entry.get()
    output_file = output_entry.get()
    if image_path and output_file:
        text = image_to_text(image_path)
        save_text(text, output_file)
        result_label.config(text="Conversion Complete!", fg="green")
    else:
        result_label.config(text="Please select both input image and output file.", fg="red")

# GUI Setup
root = Tk()
root.title("Image to Text Converter")

Label(root, text="Select Image File:").grid(row=0, column=0, padx=10, pady=10)
image_entry = Entry(root, width=50)
image_entry.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Browse", command=browse_image).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="Save Text File As:").grid(row=1, column=0, padx=10, pady=10)
output_entry = Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Browse", command=browse_output_file).grid(row=1, column=2, padx=10, pady=10)

Button(root, text="Convert", command=convert).grid(row=2, column=0, columnspan=3, pady=20)

result_label = Label(root, text="")
result_label.grid(row=3, column=0, columnspan=3)

root.mainloop()
