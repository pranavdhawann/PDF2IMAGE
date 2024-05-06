import os
from pdf2image import convert_from_path
from PIL import Image

input_folder = ''  # Provide the path to the folder containing PDF files
output_folder = ''  # Provide the path to the folder where the output images will be saved

def convert_pdf_to_image(pdf_path, output_path):
    """Converts a PDF file to a series of images."""
    images = convert_from_path(pdf_path)

    for i, image in enumerate(images):
        image.save(os.path.join(output_path, f'output_image_{i}.jpg'), 'JPEG')

def resize_image(src_img, size=(64, 64), bg_color="white"):
    """Resizes an image and centers it on a new background."""
    src_img.thumbnail(size, Image.LANCZOS)

    new_image = Image.new("RGB", size, bg_color)
    new_image.paste(src_img, (int((size[0] - src_img.size[0]) / 2), int((size[1] - src_img.size[1]) / 2)))

    return new_image

def process_pdfs(input_folder, output_folder):
    """Processes all PDF files in the input folder."""
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_output_folder = os.path.join(output_folder, os.path.splitext(pdf_file)[0])

        os.makedirs(pdf_output_folder, exist_ok=True)

        # Convert PDF to images
        convert_pdf_to_image(pdf_path, pdf_output_folder)

        image_files = os.listdir(pdf_output_folder)

        # Set the required dimensions for resizing images
        size = (1447, 2048)  # Width, Height
        background_color = "white"

        # Resize images and save them
        for file_idx in range(len(image_files)):
            img = Image.open(os.path.join(pdf_output_folder, image_files[file_idx]))
            resized_img = resize_image(img, size, background_color)
            resized_img.save(os.path.join(pdf_output_folder, f"resized_{image_files[file_idx]}"))

        # Remove original images
        for file in image_files:
            os.remove(os.path.join(pdf_output_folder, file))

# Execute the PDF processing function
process_pdfs(input_folder, output_folder)
