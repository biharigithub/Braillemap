import os
import logging
from flask import Flask, render_template, request, jsonify, redirect
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract

# Utils
from utils.speech_processor import synthesize_speech

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "braillemap-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Braille Mappings (Simplified)
BRAILLE_MAP = {'a': '⠁', 'b': '⠃', 'c': '⠉', ' ': '⠀', '.': '⠲'}
HINDI_BRAILLE_MAP = {'अ': '⠁', 'आ': '⠜', ' ': '⠀', '।': '⠲'}

# Utility functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def text_to_braille(text, language='english'):
    result = ""
    mapping = BRAILLE_MAP if language == 'english' else HINDI_BRAILLE_MAP
    for char in text:
        result += mapping.get(char, char)
    return result

def extract_text_from_image(image_path, lang='eng'):
    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return pytesseract.image_to_string(image, lang=lang).strip()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text-to-braille')
def text_to_braille_page():
    return render_template('text_to_braille.html')

@app.route('/image-to-braille')
def image_to_braille_page():
    return render_template('image_to_braille.html')

@app.route('/api/convert-text', methods=['POST'])
def api_convert_text():
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', 'english')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    braille = text_to_braille(text, language)
    return jsonify({'braille_text': braille})

@app.route('/api/upload-image', methods=['POST'])
def api_upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    language = request.form.get('language', 'english')
    extracted_text = extract_text_from_image(filepath, 'hin' if language == 'hindi' else 'eng')
    braille = text_to_braille(extracted_text, language)
    return jsonify({'extracted_text': extracted_text, 'braille_text': braille})

# ✅ Text-to-Speech API (Android WebView compatible)
@app.route('/api/text-to-speech', methods=['POST'])
def api_text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', 'english')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    audio_url = synthesize_speech(text, language)
    if audio_url:
        return jsonify({'audio_url': audio_url})
    return jsonify({'error': 'TTS failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
