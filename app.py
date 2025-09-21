import os
import zipfile
import tempfile
from flask import Flask, request, jsonify, render_template, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
from PIL import Image
import uuid
import shutil
import platform

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_pdf_to_images(pdf_path, output_format='PNG', dpi=150):
    """Convert PDF to images with specified format and DPI"""
    try:
        # Configure poppler path for Windows
        poppler_path = None
        if platform.system() == "Windows":
            # Try common poppler installation paths
            possible_paths = [
                os.path.join(os.getcwd(), "poppler", "poppler-23.08.0", "Library", "bin"),
                r"C:\poppler\bin",
                r"C:\Program Files\poppler\bin",
                r"C:\Program Files (x86)\poppler\bin",
                r"C:\tools\poppler\bin",
                os.path.join(os.getcwd(), "poppler", "bin")
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    poppler_path = path
                    print(f"Found poppler at: {path}")  # Debug print
                    break
        
        # Convert PDF to images
        if poppler_path:
            print(f"Using poppler path: {poppler_path}")
            images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
        else:
            print("No poppler path found, trying default...")
            images = convert_from_path(pdf_path, dpi=dpi)
        
        converted_files = []
        
        for i, image in enumerate(images):
            if output_format.upper() == 'JPEG':
                filename = f'page_{i+1}.jpg'
                image = image.convert('RGB')  # Convert to RGB for JPEG
            else:
                filename = f'page_{i+1}.png'
            
            filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
            image.save(filepath, output_format.upper())
            converted_files.append(filename)
        
        return converted_files, None
    except Exception as e:
        return None, str(e)

def create_zip_file(filenames, zip_filename):
    """Create a ZIP file containing all converted images"""
    zip_path = os.path.join(app.config['OUTPUT_FOLDER'], zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for filename in filenames:
            file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
            if os.path.exists(file_path):
                zipf.write(file_path, filename)
    
    return zip_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add unique identifier to avoid conflicts
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': unique_filename,
            'original_name': filename
        })
    
    return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400

@app.route('/convert', methods=['POST'])
def convert_pdf():
    data = request.get_json()
    filename = data.get('filename')
    output_format = data.get('format', 'PNG')
    dpi = int(data.get('dpi', 150))
    zip_files = data.get('zip', False)
    
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    # Clear previous outputs
    for file in os.listdir(app.config['OUTPUT_FOLDER']):
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # Convert PDF to images
    converted_files, error = convert_pdf_to_images(filepath, output_format, dpi)
    
    if error:
        return jsonify({'error': f'Conversion failed: {error}'}), 500
    
    if not converted_files:
        return jsonify({'error': 'No images were generated'}), 500
    
    result = {
        'success': True,
        'files': converted_files,
        'count': len(converted_files)
    }
    
    # Create ZIP file if requested
    if zip_files and len(converted_files) > 1:
        zip_filename = f'converted_images_{uuid.uuid4().hex[:8]}.zip'
        zip_path = create_zip_file(converted_files, zip_filename)
        result['zip_file'] = zip_filename
    
    return jsonify(result)

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(filepath, as_attachment=True)

@app.route('/cleanup', methods=['POST'])
def cleanup():
    """Clean up uploaded and output files"""
    try:
        # Clean uploads
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        # Clean outputs
        for file in os.listdir(app.config['OUTPUT_FOLDER']):
            file_path = os.path.join(app.config['OUTPUT_FOLDER'], file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
