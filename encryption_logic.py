import numpy as np
from PIL import Image

def encode_text_into_image(image_path, secret_text, output_path):
    """Encodes a secret text into an image using LSB steganography."""
    image = Image.open(image_path).convert("RGB")
    encoded_image = np.array(image)
    secret_text += "@@@@@@"  # Unique end marker to detect stopping point
    binary_secret_text = ''.join(format(ord(char), '08b') for char in secret_text)
    
    data_index = 0
    binary_length = len(binary_secret_text)
    
    for row in encoded_image:
        for pixel in row:
            for i in range(3):  # RGB channels
                if data_index < binary_length:
                    pixel[i] = (pixel[i] & 254) | int(binary_secret_text[data_index])
                    data_index += 1
                else:
                    break
    
    encoded_image = Image.fromarray(encoded_image)
    encoded_image.save(output_path)
    return output_path
