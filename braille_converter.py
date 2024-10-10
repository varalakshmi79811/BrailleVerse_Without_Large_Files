import speech_recognition as sr
import pytesseract
from PIL import Image
import tkinter as tk
from tkinter import filedialog

# Braille dictionary for mapping English letters to Braille Unicode
braille_dict = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵',
    ' ': ' ', '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖',
    '0': '⠴', '1': '⠂', '2': '⠆', '3': '⠒', '4': '⠲',
    '5': '⠢', '6': '⠖', '7': '⠶', '8': '⠦', '9': '⠔'
}

# Function to convert text to Braille
def text_to_braille(text):
    braille_text = ''.join(braille_dict.get(char, ' ') for char in text.lower())
    return braille_text

# Function to record speech from the microphone and convert it to text
def record_speech_from_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Ready to record. Please speak...")
        audio_data = recognizer.listen(source)
        print("Recording complete. Processing...")

    try:
        text = recognizer.recognize_google(audio_data)
        print(f"Transcription: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    return None

# Function to perform Image-to-Text (OCR) using Tesseract
def image_to_text(image_path):
    try:
        img = Image.open(image_path)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(img)
        if text.strip():
            return text
        else:
            print("No text found in the image.")
            return None
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# Function to open a file dialog to select an image
def upload_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    return file_path

# Main function to handle input types and convert them to Braille
def process_input_and_convert_to_braille(audio_input=False, image_upload=False, text_input=False):
    final_text = ""

    if audio_input:
        print("Processing speech input...")
        final_text = record_speech_from_microphone()

    if image_upload:
        print("Select an image to upload...")
        image_path = upload_image()
        if image_path:
            print(f"Processing image input from {image_path}...")
            final_text = image_to_text(image_path)

    if text_input:
        final_text = input("Please enter the text: ")

    if final_text:
        braille_output = text_to_braille(final_text)
        print(f"Braille Output: {braille_output}")
        return braille_output
    else:
        print("No valid input provided.")
        return None

if __name__ == "__main__":
    choice = input("Choose an option:\n1. Record Speech\n2. Upload Image\n3. Enter Text\nEnter 1, 2, or 3: ")

    if choice == '1':
        process_input_and_convert_to_braille(audio_input=True)
    elif choice == '2':
        process_input_and_convert_to_braille(image_upload=True)
    elif choice == '3':
        process_input_and_convert_to_braille(text_input=True)
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
