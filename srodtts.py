import os
import sys
import subprocess
import pyttsx3
import random
import pyaudio
import wave
import speech_recognition as sr
from pydub import AudioSegment
import numpy as np
import time
from threading import Thread
from warnings import warn

# Ensure all necessary dependencies are installed
def install_dependencies():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyttsx3', 'pyaudio', 'speechrecognition', 'pydub', 'numpy', 'pillow', 'pywin32'])

install_dependencies()

# Check if ffmpeg is installed and in PATH
def check_ffmpeg():
    try:
        subprocess.check_output(['ffmpeg', '-version'])
        print("ffmpeg is installed and in PATH")
    except subprocess.CalledProcessError:
        warn("Couldn't find ffmpeg. Please install ffmpeg and add it to your PATH", RuntimeWarning)
    except FileNotFoundError:
        warn("Couldn't find ffmpeg. Please install ffmpeg and add it to your PATH", RuntimeWarning)

check_ffmpeg()

# Initialize the TTS engine
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)  # Set the speech rate to a slower value
    voices = engine.getProperty('voices')
except Exception as e:
    print(f"Error initializing pyttsx3: {e}")
    sys.exit(1)

# Configure audio input and output
CHUNK = 256
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 24000

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the stream for input and output
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

def get_random_voice():
    return random.choice(voices)

def text_to_speech(word, voice):
    engine.setProperty('voice', voice.id)
    engine.save_to_file(word, 'temp.wav')
    engine.runAndWait()
    return AudioSegment.from_wav('temp.wav')

def add_noise(audio, noise_folder):
    if not noise_folder or not os.listdir(noise_folder):
        return audio  # Return original audio if no noise folder or no files in it
    
    noise_files = [os.path.join(noise_folder, f) for f in os.listdir(noise_folder) if f.endswith('.wav')]
    if not noise_files:
        return audio  # Return original audio if no .wav files in the noise folder

    noise = AudioSegment.from_wav(random.choice(noise_files))
    combined = audio.overlay(noise)
    return combined

def recognize_and_process(noise_folder):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        print("Listening...")
        with mic as source:
            audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")

            words = text.split()
            previous_voice = None
            combined_audio = AudioSegment.silent(duration=0)

            for word in words:
                voice = get_random_voice()
                while voice == previous_voice:
                    voice = get_random_voice()
                previous_voice = voice
                
                word_audio = text_to_speech(word, voice)
                combined_audio += word_audio
                combined_audio += AudioSegment.silent(duration=0)  # Add a pause between words

            final_audio = add_noise(combined_audio, noise_folder)
            play_audio(final_audio)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

def play_audio(audio_segment):
    raw_data = audio_segment.raw_data
    stream.write(raw_data)

# Usage example
noise_folder = ''  # Set to None or empty string to disable noise
recognize_and_process(noise_folder)
