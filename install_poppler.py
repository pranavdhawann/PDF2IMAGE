#!/usr/bin/env python3
"""
Poppler installation script for Windows
Downloads and sets up poppler binaries for pdf2image
"""

import os
import sys
import zipfile
import urllib.request
import platform

def download_poppler():
    """Download and extract poppler for Windows"""
    if platform.system() != "Windows":
        print("This script is for Windows only.")
        return False
    
    poppler_url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.08.0-0/Release-23.08.0-0.zip"
    poppler_dir = "poppler"
    poppler_zip = "poppler.zip"
    
    print("Downloading poppler binaries...")
    try:
        urllib.request.urlretrieve(poppler_url, poppler_zip)
        print("Download completed!")
        
        print("Extracting poppler...")
        with zipfile.ZipFile(poppler_zip, 'r') as zip_ref:
            zip_ref.extractall(poppler_dir)
        
        # Clean up zip file
        os.remove(poppler_zip)
        
        print(f"Poppler installed successfully in {poppler_dir}/")
        print("You can now run the Flask app!")
        return True
        
    except Exception as e:
        print(f"Error installing poppler: {e}")
        return False

if __name__ == "__main__":
    download_poppler()
