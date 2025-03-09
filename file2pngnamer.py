import os
from PIL import Image

def convert_to_png(folder_path):
    # Get a list of all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Skip if it's already a .png file
        if filename.lower().endswith('.png'):
            print(f"Skipping {filename}, already a .png file.")
            continue
        
        # Try to open the file as an image
        try:
            with Image.open(file_path) as img:
                # Remove file extension and add .png
                png_filename = os.path.splitext(filename)[0] + '.png'
                png_path = os.path.join(folder_path, png_filename)
                
                # Save the image as .png
                img.save(png_path, 'PNG')
                print(f"Converted {filename} to {png_filename}")
                
                # Optionally, delete the original file
                 os.remove(file_path)
        
        except Exception as e:
            print(f"Could not convert {filename}: {e}")

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder: ")
    convert_to_png(folder_path)
