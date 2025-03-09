import os
from tkinter import Tk, Label, Button, Entry, filedialog
from PIL import Image
import numpy as np
import wave

def image_to_audio(image_path, output_audio_path):
    # Load image
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    # Convert image data to numpy array
    data = np.array(img)
    
    # Flatten the data and normalize
    audio_data = data.flatten().astype(np.float32)
    audio_data = (audio_data - np.min(audio_data)) / (np.max(audio_data) - np.min(audio_data))  # Normalize to [0, 1]
    audio_data = (audio_data * 2 - 1) * 32767  # Scale to [-32767, 32767] for 16-bit audio
    
    # Convert to int16 format
    audio_data = audio_data.astype(np.int16)
    
    # Write to WAV file
    sample_rate = 44100  # 44.1kHz sample rate
    with wave.open(output_audio_path, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono audio
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    print(f'Audio saved to {output_audio_path}')

def browse_image():
    filename = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    image_entry.delete(0, 'end')
    image_entry.insert(0, filename)

def browse_output():
    filename = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
    output_entry.delete(0, 'end')
    output_entry.insert(0, filename)

def convert():
    image_path = image_entry.get()
    output_path = output_entry.get()
    if image_path and output_path:
        image_to_audio(image_path, output_path)
        result_label.config(text="Conversion Complete!", fg="green")
    else:
        result_label.config(text="Please select both input and output files.", fg="red")

# GUI Setup
root = Tk()
root.title("Image to Audio Converter")

Label(root, text="Select Image File:").grid(row=0, column=0, padx=10, pady=10)
image_entry = Entry(root, width=50)
image_entry.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Browse", command=browse_image).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="Save Audio File As:").grid(row=1, column=0, padx=10, pady=10)
output_entry = Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Browse", command=browse_output).grid(row=1, column=2, padx=10, pady=10)

Button(root, text="Convert", command=convert).grid(row=2, column=0, columnspan=3, pady=20)

result_label = Label(root, text="")
result_label.grid(row=3, column=0, columnspan=3)

root.mainloop()
