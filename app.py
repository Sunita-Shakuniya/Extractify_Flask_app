from flask import Flask, render_template, request
import cv2
import pytesseract
from googletrans import Translator
from gtts import gTTS
import os

# Set the Tesseract path if not set globally
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

# Function to perform text extraction using OCR
def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary_image_adaptive = cv2.adaptiveThreshold(gray_image, 250, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    _, binary_image = cv2.threshold(binary_image_adaptive, 150, 255, cv2.THRESH_BINARY)
    extracted_text = pytesseract.image_to_string(binary_image)
    return extracted_text

@app.route('/')
def index():
    extracted_text=None # Initialize extracted text
    return render_template('index.html',extracted_text=extracted_text)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            image_path = 'uploads/' + image.filename
            image.save(image_path)  # Save the uploaded image to the 'uploads' folder

            # Call the function for text extraction
            extracted_text = extract_text_from_image(image_path)
            # Render a template with the extracted text
            return render_template('index.html', extracted_text=extracted_text)
    return 'No image provided'
@app.route('/translate_hindi', methods=['POST'])
def translate_hindi():
    if 'text_to_translate' in request.form:
        text_to_translate = request.form['text_to_translate']
        translator = Translator()
        translated_text = translator.translate(text_to_translate, dest='hi').text
        return render_template('index.html', extracted_text=text_to_translate, translated_text=translated_text)

    return 'Translation to Hindi failed'

@app.route('/translate_audio', methods=['POST'])
def translate_audio():
    if 'text_to_translate' in request.form:
        text_to_translate = request.form['text_to_translate']
        translator = Translator()
        translated_text = translator.translate(text_to_translate, dest='hi').text
        
        # Generating audio from translated text in Hindi
        tts = gTTS(translated_text, lang='hi')
        audio_file_path = 'static/translated_audio.mp3'
        tts.save(audio_file_path)
        
        # Render the template with necessary data
        return render_template('index.html', extracted_text=text_to_translate, translated_text=translated_text, audio_file=audio_file_path)

    return 'Translation to Audio failed'




if __name__ =="__main__":
    app.run(debug=True,port=8000)