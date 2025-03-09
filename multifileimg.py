import os
from tkinter import filedialog, Tk, Button, Label
from PIL import Image

# Function to read hex data from multiple files
def read_hex_data(files):
    hex_data = ""
    for file in files:
        with open(file, 'rb') as f:
            hex_data += f.read().hex()
    return hex_data

# Function to convert hex data to RGB tuples
def hex_to_rgb(hex_data):
    rgb_data = []
    for i in range(0, len(hex_data), 6):
        hex_color = hex_data[i:i+6]
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            rgb_data.append((r, g, b))
    return rgb_data

# Function to create the largest possible square image from the RGB data
def create_largest_square_image(rgb_data):
    num_pixels = len(rgb_data)
    side_length = int(num_pixels**0.5)
    image_size = side_length * side_length
    rgb_data = rgb_data[:image_size]
    
    image = Image.new("RGB", (side_length, side_length))
    image.putdata(rgb_data)
    return image

# Function to handle the file selection and image creation
def create_image_from_files():
    files = filedialog.askopenfilenames(title="Select Files", filetypes=[("All Files", "*.*")])
    if files:
        hex_data = read_hex_data(files)
        rgb_data = hex_to_rgb(hex_data)
        image = create_largest_square_image(rgb_data)
        
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            image.save(output_path)
            status_label.config(text=f"Image saved: {output_path}")
        else:
            status_label.config(text="Image save cancelled.")
    else:
        status_label.config(text="No files selected.")

# Setup the GUI
root = Tk()
root.title("Hex Data to Image Converter")

select_button = Button(root, text="Select Files and Create Image", command=create_image_from_files)
select_button.pack(pady=20)

status_label = Label(root, text="")
status_label.pack(pady=10)

root.mainloop()
