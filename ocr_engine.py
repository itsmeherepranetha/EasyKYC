import os
import easyocr
import logging
import cv2
import numpy as np

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir,"ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")


def extract_text(image_path, confidence_threshold=0.2):
    
    # Noise reduction
    blur = cv2.GaussianBlur(image_path, (5, 5), 0)

    # Adaptive thresholding
    thresh=cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    #could do some dilation , erosion and morphing and canny edge detection, but doesn't help much...

    logging.info("Text Extraction Started...")
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])
    
    try:
        logging.info("Inside Try-Catch...")
        # Read the image and extract text
        result = reader.readtext(thresh)
        filtered_text = "|"  # Initialize an empty string to store filtered text
        for text in result:
            bounding_box, recognized_text, confidence = text
            if confidence > confidence_threshold: # Filter the extracted text based on confidence score
                filtered_text += recognized_text + "|"  # Append filtered text with newline

        return filtered_text 
    except Exception as e:
        print("An error occurred during text extraction:", e)
        logging.info(f"An error occurred during text extraction: {e}")
        return ""
    