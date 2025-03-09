import pyttsx3

try:
    engine = pyttsx3.init()
    engine.say("Hello, world!")
    engine.runAndWait()
    print("pyttsx3 initialized successfully")
except Exception as e:
    print(f"Error initializing pyttsx3: {e}")
