# ocr_module.py

from google.cloud import vision
import io
import os

def detect_text(image_content, credentials_path):
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=image_content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Check if any text was detected
    if texts:
        # The first item in the text annotations is the complete detected text
        full_text = texts[0].description
        print("Detected text:")
        print(full_text)
        return full_text
    else:
        print("No text detected.")
        return None
