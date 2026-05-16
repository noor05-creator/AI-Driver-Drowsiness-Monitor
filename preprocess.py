import os
import cv2
import numpy as np

OPEN_DIR = "data/open"
CLOSED_DIR = "data/closed"
TARGET_SIZE = (24, 24)


def preprocess_folder(folder_path):
    """
    Resize all images in a folder to 24x24 grayscale.

    Args:
        folder_path (str): Path to the folder containing images.

    Returns:
        int: Number of images successfully processed.
    """
    count = 0
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img_resized = cv2.resize(img, TARGET_SIZE)
            cv2.imwrite(img_path, img_resized)
            count += 1
    return count


open_count = preprocess_folder(OPEN_DIR)
closed_count = preprocess_folder(CLOSED_DIR)

print(f"Processed {open_count} open eye images")
print(f"Processed {closed_count} closed eye images")
print(f"Total: {open_count + closed_count} images")

if open_count < 1000:
    print("WARNING: open eye images below 1000 minimum")
if closed_count < 1000:
    print("WARNING: closed eye images below 1000 minimum")