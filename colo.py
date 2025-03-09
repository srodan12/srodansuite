import os
from tkinter import Tk, filedialog, messagebox
from PIL import Image
import re

# Function to extract the hex color from the image
def get_hex_color(image_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            r, g, b = img.getpixel((0, 0))  # Get the color of the first pixel
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            return hex_color
    except Exception as e:
        print(f"Error with image {image_path}: {e}")
        return None

# Function to extract number from the filename for sorting
def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(0)) if match else 0

# Function to open folder and process all images
def process_images():
    folder_selected = filedialog.askdirectory()
    if not folder_selected:
        messagebox.showwarning("Folder Selection", "No folder selected.")
        return

    # Get all image filenames and sort them by numerical order
    image_files = [f for f in os.listdir(folder_selected) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    image_files.sort(key=extract_number)

    hex_colors = []
    for filename in image_files:
        image_path = os.path.join(folder_selected, filename)
        hex_color = get_hex_color(image_path)
        if hex_color:
            hex_colors.append(hex_color)

    if not hex_colors:
        messagebox.showwarning("No Images", "No valid images found.")
        return

    save_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if save_file:
        with open(save_file, 'w') as f:
            for color in hex_colors:
                f.write(color + '\n')

        messagebox.showinfo("Success", f"Hex colors saved to {save_file}")

# Tkinter UI setup
root = Tk()
root.withdraw()  # Hide the root window
messagebox.showinfo("Instructions", "Please select the folder with images.")

process_images()
