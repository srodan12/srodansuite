import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

# Function to split the image into a grid
def split_image(image_path, rows, cols, output_dir):
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Calculate the size of each piece
        img_width, img_height = img.size
        piece_width = img_width // cols
        piece_height = img_height // rows
        
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Split the image into pieces
        n = 0  # Initialize slice number starting from 0
        for row in range(rows):
            for col in range(cols):
                left = col * piece_width
                top = row * piece_height
                right = (col + 1) * piece_width
                bottom = (row + 1) * piece_height
                
                # Crop the image to the piece and save it
                piece = img.crop((left, top, right, bottom))
                piece_path = os.path.join(output_dir, f'piece_{n}.png')
                piece.save(piece_path)
                n += 1  # Increment the slice number
                
        messagebox.showinfo("Success", "Image splitting completed!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to select an image file
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        image_path_entry.delete(0, tk.END)
        image_path_entry.insert(0, file_path)

# Function to select an output directory
def select_output_dir():
    dir_path = filedialog.askdirectory()
    if dir_path:
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, dir_path)

# Function to trigger the image splitting process
def process_image():
    image_path = image_path_entry.get()
    rows = int(rows_entry.get())
    cols = int(cols_entry.get())
    output_dir = output_dir_entry.get()
    
    if not os.path.exists(image_path):
        messagebox.showerror("Error", "Please select a valid image.")
        return

    if rows <= 0 or cols <= 0:
        messagebox.showerror("Error", "Rows and columns must be positive integers.")
        return

    if not os.path.exists(output_dir):
        messagebox.showerror("Error", "Please select a valid output directory.")
        return
    
    split_image(image_path, rows, cols, output_dir)

# Create the main window
root = tk.Tk()
root.title("Image Splitter")

# Create UI elements
image_path_label = tk.Label(root, text="Image Path:")
image_path_label.grid(row=0, column=0, padx=10, pady=10)

image_path_entry = tk.Entry(root, width=50)
image_path_entry.grid(row=0, column=1, padx=10, pady=10)

image_browse_button = tk.Button(root, text="Browse", command=select_image)
image_browse_button.grid(row=0, column=2, padx=10, pady=10)

rows_label = tk.Label(root, text="Rows:")
rows_label.grid(row=1, column=0, padx=10, pady=10)

rows_entry = tk.Entry(root, width=10)
rows_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

cols_label = tk.Label(root, text="Columns:")
cols_label.grid(row=2, column=0, padx=10, pady=10)

cols_entry = tk.Entry(root, width=10)
cols_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

output_dir_label = tk.Label(root, text="Output Directory:")
output_dir_label.grid(row=3, column=0, padx=10, pady=10)

output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.grid(row=3, column=1, padx=10, pady=10)

output_browse_button = tk.Button(root, text="Browse", command=select_output_dir)
output_browse_button.grid(row=3, column=2, padx=10, pady=10)

process_button = tk.Button(root, text="Split Image", command=process_image)
process_button.grid(row=4, column=1, padx=10, pady=20)

# Start the Tkinter event loop
root.mainloop()
