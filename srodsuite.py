#!/usr/bin/env python3
# suite.py
"""
A Tkinter-based suite that checks for required packages, installs any that are missing,
and presents a simple GUI to launch each of the provided scripts in a separate process.
"""

import sys
import subprocess

##############################################################################
# 1) Define the list of PIP packages we need (by their PyPI names).

REQUIRED_PACKAGES = [
    "Pillow",            # for 'PIL'
    "numpy",
    "hilbertcurve",
    "pydub",
    "beautifulsoup4",    # for 'bs4'
    "pandas",
    "pyttsx3",
    "pyaudio",
    "SpeechRecognition",
]

##############################################################################
# 2) Function to check/install missing packages.

def install_missing_packages():
    """
    For each package in REQUIRED_PACKAGES, try importing it.
    If it's not installed, pip-install it.
    """
    for pkg in REQUIRED_PACKAGES:
        # The import name can differ from the PyPI package name
        # For example, "Pillow" installs as "PIL", "beautifulsoup4" as "bs4", etc.
        if pkg == "Pillow":
            import_name = "PIL"
        elif pkg == "beautifulsoup4":
            import_name = "bs4"
        elif pkg == "SpeechRecognition":
            import_name = "speech_recognition"
        else:
            import_name = pkg

        try:
            __import__(import_name)
        except ImportError:
            print(f"Package '{pkg}' not found. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                print(f"Successfully installed {pkg}")
            except subprocess.CalledProcessError:
                print(f"Failed to install {pkg}. Please install it manually.")
        except Exception as e:
            print(f"Unexpected error while trying to import {import_name}: {e}")

##############################################################################
# 3) Install missing packages before proceeding.

install_missing_packages()

##############################################################################
# 4) Now that packages are installed, do normal imports.

import tkinter as tk
import os
from functools import partial

##############################################################################
# 5) List the scripts you want to launch. (Adjust as needed.)

SCRIPTS = [
    "audioChunker.py",
    "audioChunkstoCollage by hashorder.py",
    "bmpifyer.py",
    "colo.py",
    "cuttr.py",
    "data2hex.py",
    "data2hexv2.py",
    "datas2raw.py",
    "dither.py",
    "file2pngnamer.py",
    "hex2aud.py",
    "hex2txt.py",
    "hilbertbmpfiyer v2.py",
    "hilberttest.py",
    "img2txt.py",
    "multifileimg.py",
    "srodtts.py",
    "srodttsgui.py",
    "srodttsguiotherrr.py",
    "stegano.py",
    "nn_upscaler.py",
]

##############################################################################
# 6) A helper function to launch a given script in a new process.

def launch_script(script_name):
    """Launch a script in a separate Python process."""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(script_path):
        print(f"Script not found: {script_path}")
        return
    # Open a new process
    subprocess.Popen([sys.executable, script_path])

##############################################################################
# 7) Build the main GUI.

def create_main_window():
    window = tk.Tk()
    window.title("My Python Suite")

    label = tk.Label(window, text="Select a script to launch:")
    label.pack(pady=10)

    for script_name in SCRIPTS:
        btn = tk.Button(
            window,
            text=script_name,
            width=40,
            command=partial(launch_script, script_name)
        )
        btn.pack(pady=2)

    # Optionally, add a quit button
    quit_btn = tk.Button(window, text="Quit", command=window.destroy)
    quit_btn.pack(pady=10)

    return window

##############################################################################
# 8) Run the GUI if this file is the main entry point.

if __name__ == "__main__":
    root = create_main_window()
    root.mainloop()
