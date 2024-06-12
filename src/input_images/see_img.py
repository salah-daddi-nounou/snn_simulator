"""
This script loads and displays an image stored in a .npy file. It uses matplotlib 
to visualize the image and print its size and shape.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Path to the input .npy file
input_path = "letter_imgs/generated_H.npy"
#input_path = "./mnist_npy/image_10.npy"

def load_and_display_image(input_path):
    """
    Load an image from a .npy file and display it using matplotlib.

    Args:
        input_path (str): Path to the .npy file containing the image.
    """
    image = np.load(input_path)
    print(f"size is: {np.size(image)} and shape is {np.shape(image)} ")

    plt.imshow(image, cmap='gray')
    plt.colorbar()
    plt.show()

# Load and display the image
load_and_display_image(input_path)

