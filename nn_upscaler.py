import os
from tkinter import Tk, Button, Label, filedialog, messagebox, simpledialog
from PIL import Image

def nearest_neighbor_upscale(img, scale_factor):
    original_width, original_height = img.size
    new_width = original_width * scale_factor
    new_height = original_height * scale_factor

    return img.resize((new_width, new_height), Image.NEAREST)

def upscale_folder(folder_path, scale_factor):
    output_folder = os.path.join(folder_path, 'upscaled')
    os.makedirs(output_folder, exist_ok=True)

    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(supported_formats):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)
            upscaled_img = nearest_neighbor_upscale(img, scale_factor)

            output_path = os.path.join(output_folder, filename)
            upscaled_img.save(output_path)

def select_and_upscale():
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return

    scale_factor = simpledialog.askinteger("Input", "Enter upscale factor:", minvalue=1, maxvalue=20)
    if not scale_factor:
        messagebox.showerror("Error", "Upscale factor not provided.")
        return

    try:
        upscale_folder(folder_path, scale_factor)
        messagebox.showinfo("Success", f"Images upscaled successfully!\nOutput folder: {os.path.join(folder_path, 'upscaled')}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# GUI Setup
app = Tk()
app.title('Batch Nearest Neighbor Upscaler')
app.geometry('350x150')

label = Label(app, text='Choose a folder to batch upscale', pady=20)
label.pack()

button = Button(app, text='Select Folder and Upscale', command=select_and_upscale)
button.pack()

app.mainloop()
