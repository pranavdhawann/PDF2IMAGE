// Global variables
let uploadedFile = null;
let conversionResults = null;

// DOM elements
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const filePreview = document.getElementById('file-preview');
const fileName = document.getElementById('file-name');
const removeFileBtn = document.getElementById('remove-file');
const conversionOptions = document.getElementById('conversion-options');
const convertBtn = document.getElementById('convert-btn');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const imagesGrid = document.getElementById('images-grid');
const downloadAllZipBtn = document.getElementById('download-all-zip');
const errorMessage = document.getElementById('error-message');
const errorText = document.getElementById('error-text');
const themeToggle = document.getElementById('theme-toggle');

// Theme toggle functionality
themeToggle.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
    localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
});

// Initialize theme
if (localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
}

// File upload handling
uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
removeFileBtn.addEventListener('click', removeFile);

// Conversion handling
convertBtn.addEventListener('click', convertFile);
downloadAllZipBtn.addEventListener('click', downloadAllZip);

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('border-primary', 'bg-blue-50', 'dark:bg-blue-900/20');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('border-primary', 'bg-blue-50', 'dark:bg-blue-900/20');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('border-primary', 'bg-blue-50', 'dark:bg-blue-900/20');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    if (!file.type.includes('pdf')) {
        showError('Please select a valid PDF file.');
        return;
    }
    
    if (file.size > 20 * 1024 * 1024) {
        showError('File size must be less than 20MB.');
        return;
    }
    
    uploadedFile = file;
    fileName.textContent = file.name;
    filePreview.classList.remove('hidden');
    conversionOptions.classList.remove('hidden');
    hideError();
}

function removeFile() {
    uploadedFile = null;
    fileInput.value = '';
    filePreview.classList.add('hidden');
    conversionOptions.classList.add('hidden');
    results.classList.add('hidden');
    hideError();
}

async function convertFile() {
    if (!uploadedFile) {
        showError('Please select a file first.');
        return;
    }
    
    // Show loading state
    loading.classList.remove('hidden');
    results.classList.add('hidden');
    hideError();
    
    try {
        // Upload file
        const formData = new FormData();
        formData.append('file', uploadedFile);
        
        const uploadResponse = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const uploadResult = await uploadResponse.json();
        
        if (!uploadResult.success) {
            throw new Error(uploadResult.error || 'Upload failed');
        }
        
        // Convert file
        const convertData = {
            filename: uploadResult.filename,
            format: document.getElementById('output-format').value,
            dpi: parseInt(document.getElementById('dpi').value),
            zip: document.getElementById('zip-files').checked
        };
        
        const convertResponse = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(convertData)
        });
        
        const convertResult = await convertResponse.json();
        
        if (!convertResult.success) {
            throw new Error(convertResult.error || 'Conversion failed');
        }
        
        // Store results and display
        conversionResults = convertResult;
        displayResults(convertResult);
        
    } catch (error) {
        showError(error.message);
    } finally {
        loading.classList.add('hidden');
    }
}

function displayResults(result) {
    imagesGrid.innerHTML = '';
    
    // Show download all zip button if zip was created
    if (result.zip_file) {
        downloadAllZipBtn.onclick = () => downloadFile(result.zip_file);
        downloadAllZipBtn.classList.remove('hidden');
    } else {
        downloadAllZipBtn.classList.add('hidden');
    }
    
    // Display individual images
    result.files.forEach((filename, index) => {
        const imageCard = createImageCard(filename, index + 1);
        imagesGrid.appendChild(imageCard);
    });
    
    results.classList.remove('hidden');
    
    // Smooth scroll to results
    results.scrollIntoView({ behavior: 'smooth' });
}

function createImageCard(filename, pageNumber) {
    const card = document.createElement('div');
    card.className = 'bg-gray-50 dark:bg-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow';
    
    card.innerHTML = `
        <div class="aspect-[3/4] bg-white dark:bg-gray-600 rounded-lg mb-3 flex items-center justify-center">
            <div class="text-center">
                <svg class="mx-auto h-12 w-12 text-gray-400 mb-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"></path>
                </svg>
                <p class="text-sm text-gray-500 dark:text-gray-400">Page ${pageNumber}</p>
            </div>
        </div>
        <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-gray-900 dark:text-white">${filename}</span>
            <button onclick="downloadFile('${filename}')" class="bg-primary hover:bg-blue-700 text-white text-xs font-medium py-1.5 px-3 rounded transition-colors duration-200">
                <svg class="w-3 h-3 mr-1 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                Download
            </button>
        </div>
    `;
    
    return card;
}

function downloadFile(filename) {
    const link = document.createElement('a');
    link.href = `/download/${filename}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function downloadAllZip() {
    if (conversionResults && conversionResults.zip_file) {
        downloadFile(conversionResults.zip_file);
    }
}

function showError(message) {
    errorText.textContent = message;
    errorMessage.classList.remove('hidden');
    
    // Auto-hide error after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    errorMessage.classList.add('hidden');
}

// Add smooth transitions to all interactive elements
document.addEventListener('DOMContentLoaded', () => {
    // Add transition classes to buttons and interactive elements
    const interactiveElements = document.querySelectorAll('button, input, select, .cursor-pointer');
    interactiveElements.forEach(el => {
        if (!el.classList.contains('transition-colors') && !el.classList.contains('transition-shadow')) {
            el.classList.add('transition-colors', 'duration-200');
        }
    });
});
