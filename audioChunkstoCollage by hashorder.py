import os
import hashlib
from pydub import AudioSegment
from tkinter import filedialog, Tk
import random

def get_audio_files(folder):
    audio_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".wav") or f.endswith(".mp3")]
    return audio_files

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def select_random_files_until_max_duration(audio_files, max_duration_ms=60000):
    selected_files = []
    total_duration = 0

    while total_duration < max_duration_ms and audio_files:
        file = random.choice(audio_files)
        audio_files.remove(file)
        audio = AudioSegment.from_file(file)
        file_duration = len(audio)
        
        if total_duration + file_duration > max_duration_ms:
            file_duration = max_duration_ms - total_duration
            audio = audio[:file_duration]
        
        selected_files.append((file, audio))
        total_duration += file_duration
    
    return [file for file, _ in selected_files]

def merge_audio_files(audio_files, output_path, max_duration_ms=60000):
    combined = AudioSegment.empty()
    for file in audio_files:
        audio = AudioSegment.from_file(file)
        if len(combined) + len(audio) > max_duration_ms:
            remaining_duration = max_duration_ms - len(combined)
            combined += audio[:remaining_duration]
            break
        combined += audio
    combined.export(output_path, format="wav")
    print(f"Exported merged audio to {output_path}")

def main():
    # Hide the root Tkinter window
    root = Tk()
    root.withdraw()
    
    # Select the folder containing audio samples
    folder = filedialog.askdirectory(title="Select the folder containing audio samples")
    
    if not folder:
        print("No folder selected.")
        return
    
    # Get audio files from the folder
    audio_files = get_audio_files(folder)
    
    # Select random files until total duration reaches 1 minute
    selected_files = select_random_files_until_max_duration(audio_files)
    
    # Calculate SHA-256 hashes and sort files by hash
    selected_files.sort(key=lambda f: calculate_sha256(f))
    
    # Merge sorted audio files
    output_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")], title="Save merged audio as")
    
    if output_path:
        merge_audio_files(selected_files, output_path)
    else:
        print("No output file specified.")

if __name__ == "__main__":
    main()
