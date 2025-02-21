import numpy as np
from PIL import Image

def decode_text_from_image(image_path):
    """Extracts hidden text from an image using LSB steganography."""
    image = Image.open(image_path).convert("RGB")
    encoded_image = np.array(image)
    binary_secret_text = ""
    
    for row in encoded_image:
        for pixel in row:
            for i in range(3):  # RGB channels
                binary_secret_text += str(pixel[i] & 1)
    
    binary_chars = [binary_secret_text[i:i+8] for i in range(0, len(binary_secret_text), 8)]
    extracted_text = ""
    
    for binary_char in binary_chars:
        char = chr(int(binary_char, 2))
        if extracted_text.endswith("@@@@@@"):  # Stop at end marker
            extracted_text = extracted_text[:-6]  # Remove marker
            break
        extracted_text += char

    return extracted_text
