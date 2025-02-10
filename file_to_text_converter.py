import fitz  # PyMuPDF
import os
from groq import Groq
import requests
import time
import logging

# Configure logging
logging.basicConfig(filename='process_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set the GROQ API Key
os.environ["GROQ_API_KEY"] = "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"

# Base URL for image upload
baseurl = "https://mayur.mydigicardmanager.com/upload"

def extract_pdf_content(pdf_path, images_output_dir):
    pdf_document = fitz.open(pdf_path)
    extracted_text = ""
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        extracted_text += f"\n--- Page {page_number + 1} ---\n"
        extracted_text += page.get_text()

        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"{pdf_name}_page_{page_number + 1}_img_{img_index + 1}.{image_ext}"
            image_path = os.path.join(images_output_dir, image_filename)

            try:
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                uploaded_url = upload_image(image_path)
                ocr_text = get_ocr_text(uploaded_url, image_filename)
                extracted_text += f"\n<<START_IMAGE:{image_filename}>>\n{ocr_text}\n<<END_IMAGE:{image_filename}>>\n"
            except Exception as e:
                logging.error(f"Error processing image {image_filename}: {e}")

    return extracted_text

def upload_image(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            response = requests.post(baseurl, files={'file': img_file})
        
        if response.status_code == 200:
            return response.json().get('url')
        else:
            logging.error(f"Failed to upload {image_path}: {response.status_code}")
            return ""
    except Exception as e:
        logging.error(f"Exception during image upload {image_path}: {e}")
        return ""

def get_ocr_text(image_url, image_filename):
    try:
        client = Groq()
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""Act as an OCR assistant. Analyze the provided image named {image_filename} and:
1. Recognize all visible text in the image as accurately as possible.
2. Maintain the original structure and formatting of the text.
3. If any words or phrases are unclear, indicate this with [unclear] in your transcription.
Provide only the transcription without any additional comments."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            temperature=1,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error during OCR for {image_filename}: {e}")
        return "[OCR Error]"

def process_folder(folder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            images_output_dir = os.path.join(output_folder, "images")
            if not os.path.exists(images_output_dir):
                os.makedirs(images_output_dir)

            output_text_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_text.txt")

            try:
                extracted_text = extract_pdf_content(pdf_path, images_output_dir)
                with open(output_text_path, "w", encoding="utf-8") as text_file:
                    text_file.write(extracted_text)
                logging.info(f"Processed: {pdf_path}")
            except Exception as e:
                logging.error(f"Error processing {pdf_path}: {e}")

# Example Usage
input_folder = "input_folder"
output_folder = "processed_output"

process_folder(input_folder, output_folder)
