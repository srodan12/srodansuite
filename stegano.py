import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np

def encode_image(image_path, file_path, output_path):
    # Read the image
    img = Image.open(image_path)
    img = img.convert('RGB')
    data = np.array(img)

    # Read the file data
    with open(file_path, 'rb') as file:
        file_data = file.read()

    # Convert the file data to binary
    binary_data = ''.join([format(byte, '08b') for byte in file_data])

    # Add a delimiter to the binary data to indicate the end
    binary_data += '1111111111111110'  # 2-byte delimiter

    # Encode the binary data into the image
    data_flat = data.flatten()
    if len(binary_data) > len(data_flat):
        raise ValueError("File too large to encode in the image.")

    for i in range(len(binary_data)):
        data_flat[i] = (data_flat[i] & ~1) | int(binary_data[i])

    data = data_flat.reshape(data.shape)

    # Save the encoded image
    encoded_img = Image.fromarray(data)
    encoded_img.save(output_path)

def decode_image(image_path):
    # Read the image
    img = Image.open(image_path)
    img = img.convert('RGB')
    data = np.array(img)

    # Extract the binary data from the image
    data_flat = data.flatten()
    binary_data = ''
    for value in data_flat:
        binary_data += str(value & 1)

    # Split the binary data by the delimiter
    file_data_binary = binary_data.split('1111111111111110')[0]

    # Convert the binary data to bytes
    file_data = int(file_data_binary, 2).to_bytes((len(file_data_binary) + 7) // 8, byteorder='big')

    return file_data

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    return file_path

def save_file_dialog():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    return file_path

def encode():
    image_path = open_file_dialog()
    if not image_path:
        return
    file_path = open_file_dialog()
    if not file_path:
        return
    output_path = save_file_dialog()
    if not output_path:
        return

    try:
        encode_image(image_path, file_path, output_path)
        messagebox.showinfo("Success", "File encoded successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decode():
    image_path = open_file_dialog()
    if not image_path:
        return

    try:
        file_data = decode_image(image_path)
        output_path = save_file_dialog()
        if not output_path:
            return
        with open(output_path, 'wb') as file:
            file.write(file_data)
        messagebox.showinfo("Success", "File decoded successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the GUI
root = tk.Tk()
root.title("Steganography Encoder/Decoder")

encode_button = tk.Button(root, text="Encode", command=encode)
encode_button.pack(pady=10)

decode_button = tk.Button(root, text="Decode", command=decode)
decode_button.pack(pady=10)

root.mainloop()
