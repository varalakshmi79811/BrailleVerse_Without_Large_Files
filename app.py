import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
import speech_recognition as sr
import pytesseract
from PIL import Image
from gtts import gTTS


# Initialize Flask app
app = Flask(__name__)

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
    return ''.join(braille_dict.get(char, char) for char in text.lower())

# Function to record speech from the microphone and convert it to text
def record_speech():
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
        return "Could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results; {e}"

# Function to perform Image-to-Text (OCR) using Tesseract
def image_to_text(image_path):
    try:
        print(f"Processing image: {image_path}")
        img = Image.open(image_path)
        # If Tesseract is not in your PATH, uncomment the following line and provide the correct path
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(img)
        print(f"Extracted text: {text}")
        return text.strip() if text.strip() else None
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# Function to save Braille output to a file
def save_output_to_file(braille_output):
    with open("braille_output.txt", "w", encoding="utf-8") as file:
        file.write(braille_output)
    print("Braille output saved to braille_output.txt")

# Function to speak the text using gTTS
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts_file = "output.mp3"
    tts.save(tts_file)
    os.system(f"start {tts_file}")  # For Windows; use 'open' for macOS

# Flask Routes

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/image.jpg')
def serve_image():
    return send_from_directory('/Users/varalakshmi/Downloads/BrailleVscode/templates/image.jpg', 'image.jpg')



@app.route('/text', methods=['GET', 'POST'])
def text_input_post():
    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            return jsonify({'error': 'No text provided.'}), 400
        
        braille = text_to_braille(text)
        response = {'braille': braille, 'text': text}
        return jsonify(response)
    return render_template('text.html')

@app.route('/speech', methods=['GET', 'POST'])
def speech_input():
    if request.method == 'POST':
        speech_text = record_speech()
        if speech_text:
            braille = text_to_braille(speech_text)
            response = {'braille': braille, 'text': speech_text}
            return jsonify(response)
        return jsonify({'error': 'Could not process speech'}), 400
    return render_template('speech.html')

@app.route('/image', methods=['GET', 'POST'])
def image_input():
    if request.method == 'POST':
        image = request.files.get('image')
        if not image:
            return jsonify({'error': 'No image uploaded'}), 400

        # Ensure the 'uploads' directory exists
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        # Save the uploaded image
        image_path = os.path.join('uploads', image.filename)
        image.save(image_path)

        # Extract text from the image
        text = image_to_text(image_path)
        if text:
            braille = text_to_braille(text)
            response = {'braille': braille, 'text': text}
            return jsonify(response)
        else:
            return jsonify({'error': 'Could not extract text from image'}), 400

    return render_template('image.html')

@app.route('/go_back')
def go_back():
    return render_template('index.html')

@app.route('/text-input')
def text_input():
    return render_template('text.html')

# Main execution
if __name__ == '__main__':
    app.run(debug=True)

