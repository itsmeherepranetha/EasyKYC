import cv2
import numpy as np
import os
import logging
from utils import read_yaml, file_exists

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir,"ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")


config_path = "config.yaml"
config = read_yaml(config_path)

artifacts = config['artifacts']
intermediate_dir_path = artifacts['INTERMEDIATE_DIR']
contour_file_name = artifacts['CONTOUR_FILE']

def read_image(image_path, is_uploaded=False):
    if is_uploaded:
        try:
            # Read image using OpenCV, if uploaded
            image_bytes = image_path.read()
            # image_array = np.frombuffer(image_bytes, np.uint8) # converts the bytes object into a NumPy array.
            # img = cv2.imdecode(image_array, cv2.IMREAD_COLOR) #  decodes the NumPy array into an image format that OpenCV can process
            img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                logging.info("Failed to read image: {}".format(image_path))
                raise Exception("Failed to read image: {}".format(image_path))
            return img
        except Exception as e:
            logging.info(f"Error reading image: {e}")
            print("Error reading image:", e)
            return None
    else:
        try:
            img = cv2.imread(image_path)
            if img is None:
                logging.info("Failed to read image: {}".format(image_path))
                raise Exception("Failed to read image: {}".format(image_path))
            return img
        except Exception as e:
            logging.info(f"Error reading image: {e}")
            print("Error reading image:", e)
            return None

  

def extract_id_card(img):
   
    #extracts the id card portion only , using countour detection

    # Convert image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    blur = cv2.GaussianBlur(gray_img, (5, 5), 0)

    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    #morphing
    kernel = np.ones((3, 3), np.uint8)
    morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    #edges
    edges=cv2.Canny(morphed,35,40)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Select the largest contour (assuming the ID card is the largest object)
    largest_contour = None
    largest_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > largest_area:
            largest_contour = cnt
            largest_area = area

    # If no large contour is found, assume no ID card is present
    if not largest_contour.any():
        return None

    # Get bounding rectangle of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    logging.info(f"contours are found at, {(x, y, w, h)}")

    current_wd = os.getcwd()
    filename = os.path.join(current_wd,intermediate_dir_path, contour_file_name)
    contour_id = gray_img[y:y+h, x:x+w]
    is_exists = file_exists(filename)
    if is_exists:
        # Remove the existing file
        os.remove(filename)

    cv2.imwrite(filename, contour_id)

    return contour_id, filename


def save_image(image, filename, path="."):
  
  #saves an image to a given file path

  # Construct the full path
  full_path = os.path.join(path, filename)
  is_exists = file_exists(full_path)
  if is_exists:
        # Remove the existing file
        os.remove(full_path)

  # Save the image using cv2.imwrite
  cv2.imwrite(full_path, image)

  logging.info(f"Image saved successfully: {full_path}")
  return full_path