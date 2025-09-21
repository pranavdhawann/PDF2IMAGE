# PDF to Image Converter

Convert your PDF files into images effortlessly with this Python script and modern Flask web application. Whether you're visualizing documents or preprocessing data for machine learning, this tool streamlines the process.

## 🚀 Flask Web App

A modern, responsive web interface for converting PDFs to images with drag-and-drop functionality, customizable options, and instant downloads.

### Features
- **Modern Web Interface**: Clean, responsive design with dark/light mode toggle
- **Drag & Drop Upload**: Easy file upload with visual feedback
- **Multiple Output Formats**: PNG and JPEG support
- **Customizable DPI**: Choose from 72, 150, or 300 DPI for optimal quality
- **Batch Download**: Download individual images or all as a ZIP file
- **Real-time Preview**: See conversion progress and results instantly
- **File Size Limit**: 20MB maximum file size for optimal performance

### Installation & Usage

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd PDF2IMAGE
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Poppler (Required for Windows)**
   ```bash
   python install_poppler.py
   ```
   Or manually:
   - Download poppler binaries from: https://github.com/oschwartz10612/poppler-windows/releases
   - Extract to project root as: `poppler/poppler-23.08.0/Library/bin/`
   - The Flask app will automatically detect and use the poppler path

4. **Run the Flask application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

### Web App Usage

1. **Upload PDF**: Drag and drop your PDF file or click to browse
2. **Configure Options**: 
   - Select output format (PNG/JPEG)
   - Choose DPI quality (72/150/300)
   - Optionally enable ZIP download for multiple pages
3. **Convert**: Click "Convert to Images" and wait for processing
4. **Download**: Download individual images or all as a ZIP file

### Screenshots

![PDF2IMAGE Web Interface](Screenshot%202025-09-21%20153844.png)

*Modern web interface with drag-and-drop upload area, conversion options, and results display*

---

## 📋 CLI Usage (Original Script)

The original command-line interface is still available for batch processing and automation.

### Features
- Converts PDF files into JPEG images
- Resizes images for uniformity and clarity
- Batch processing capability for efficiency
- Versatile integration into various workflows

### Usage
1. Place your PDF files in the input folder
2. Run the script
3. Retrieve resized images from the output folder

### Requirements
- Python 3.x
- `pdf2image` library
- `PIL` (Python Imaging Library)

### Installation
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Customize input and output folders in the script
4. Run the script: `python PDF_To_Image.py`

---

## 🛠️ Technical Details

### Dependencies
- **Flask**: Web framework for the application
- **pdf2image**: PDF to image conversion
- **Pillow**: Image processing and manipulation
- **Werkzeug**: WSGI utilities for Flask

### File Structure
```
PDF2IMAGE/
├── app.py                 # Flask application
├── PDF_To_Image.py       # Original CLI script
├── templates/
│   └── index.html        # Web interface template
├── static/
│   ├── css/
│   │   └── custom.css    # Custom styling
│   ├── js/
│   │   └── app.js        # Frontend JavaScript
│   ├── uploads/          # Temporary upload storage
│   └── outputs/          # Converted image storage
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### API Endpoints
- `GET /` - Main web interface
- `POST /upload` - Upload PDF file
- `POST /convert` - Convert PDF to images
- `GET /download/<filename>` - Download converted files
- `POST /cleanup` - Clean up temporary files

## 🎨 Design

The web application features a modern, ChatGPT-inspired interface with:
- **TailwindCSS** for responsive styling
- **Dark/Light mode** toggle
- **Smooth animations** and transitions
- **Mobile-responsive** design
- **Accessible** color schemes and interactions

*Web app built using Flask + TailwindCSS*

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Special thanks to the developers of `pdf2image`, `PIL`, `Flask`, and `TailwindCSS` libraries.

Feel free to contribute by submitting bug reports, feature requests, or pull requests!
