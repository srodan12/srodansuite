import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from hilbertcurve.hilbertcurve import HilbertCurve

def load_images(folder):
    images = []
    for file_name in sorted(os.listdir(folder)):
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(folder, file_name)
            image = Image.open(image_path)
            images.append(image)
    return images

def create_hilbert_curve(order, dimensions):
    curve = HilbertCurve(order, dimensions)
    total_points = 2 ** (order * dimensions)
    return [curve.point_from_distance(i) for i in range(total_points)]

def stitch_images(images, order):
    curve_points = create_hilbert_curve(order, 2)
    grid_size = int(len(curve_points) ** 0.5)
    image_size = images[0].size

    stitched_image = Image.new('RGB', (grid_size * image_size[0], grid_size * image_size[1]))

    previous_position = curve_points[0]
    stitched_image.paste(images[0], (previous_position[0] * image_size[0], previous_position[1] * image_size[1]))

    for i in range(1, len(images)):
        current_position = curve_points[i]

        # Determine the direction of movement on the Hilbert curve
        dx = current_position[0] - previous_position[0]
        dy = current_position[1] - previous_position[1]

        # Rotate the image based on the direction
        if dx == 0 and dy == 1:  # Moving down
            rotated_image = images[i]
        elif dx == 0 and dy == -1:  # Moving up
            rotated_image = images[i].rotate(180, expand=True)
        elif dx == 1 and dy == 0:  # Moving right
            rotated_image = images[i].rotate(90, expand=True)
        elif dx == -1 and dy == 0:  # Moving left
            rotated_image = images[i].rotate(270, expand=True)
        else:
            rotated_image = images[i]

        # Paste the rotated image
        stitched_image.paste(rotated_image, (current_position[0] * image_size[0], current_position[1] * image_size[1]))

        previous_position = current_position

    return stitched_image

def save_image(image, save_path):
    image.save(save_path)

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        images = load_images(folder_selected)
        if images:
            order = int(len(images) ** 0.5).bit_length()  # Calculate Hilbert order
            stitched_image = stitch_images(images, order)
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                save_image(stitched_image, save_path)
                messagebox.showinfo("Success", f"Image saved to {save_path}")
            else:
                messagebox.showwarning("Canceled", "Save operation was canceled.")
        else:
            messagebox.showwarning("No Images", "No images found in the selected folder.")
    else:
        messagebox.showwarning("Canceled", "Folder selection was canceled.")

def main():
    root = tk.Tk()
    root.title("Hilbert Curve Image Stitcher")

    tk.Label(root, text="Stitch images along a Hilbert curve").pack(pady=10)

    tk.Button(root, text="Select Folder and Stitch Images", command=select_folder).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
