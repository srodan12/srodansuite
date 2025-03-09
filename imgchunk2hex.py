import os
from PIL import Image

# Function to convert hex color to RGB
def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Function to create image from hex data
def create_image_from_hex(hex_data, image_number, output_dir):
    image_size = 512
    img = Image.new('RGB', (image_size, image_size))
    pixels = img.load()

    for i in range(image_size):
        for j in range(image_size):
            start_index = (i * image_size + j) * 6
            hex_color = hex_data[start_index: start_index + 6]
            if len(hex_color) == 6:  # Ensure we have enough data for one pixel
                rgb_color = hex_to_rgb(hex_color)
                pixels[j, i] = rgb_color

    output_path = os.path.join(output_dir, f'image_{image_number}.png')
    img.save(output_path)
    print(f'Saved {output_path}')

# Function to process all chunks in a directory
def process_chunks(input_dir, output_dir):
    chunk_files = sorted([f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))])
    
    for i, chunk_file in enumerate(chunk_files):
        chunk_path = os.path.join(input_dir, chunk_file)
        with open(chunk_path, 'rb') as f:
            hex_data = f.read().hex()
        
        create_image_from_hex(hex_data, i, output_dir)

# Main function
def main():
    input_dir = "E:\\imageuschunks"
    output_dir = "E:\\output_images"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    process_chunks(input_dir, output_dir)

if __name__ == "__main__":
    main()
