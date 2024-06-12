"""
This script generates binary images of letters, saves them in both .npy and .pkl formats, 
and stores them in a specified directory. Each letter is represented by specific pixel 
positions in a 5x5 image grid. Images are saved individually as .npy arrays, 
and collectively as .pkl dict. all images are generated at once. 
"""

import numpy as np
import os
from matplotlib import pyplot as plt
import pickle

# Define image size and letter colors
image_size = (5, 5)
background_color = 0  # Black
letter_color = 255  # White

# Define the letters and their positions
letters = {
    "I": [(2, 1), (2, 2), (2, 3)],
    "O": [(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)],
    "X": [(1, 1), (3, 1), (2, 2), (1, 3), (3, 3)],
    "C": [(1, 1), (2, 1), (3, 1), (1, 2), (1, 3), (2, 3), (3, 3)],
    "F": [(1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (3, 0), (2, 2), (3, 2)],
    "H": [(1, 1), (3, 1), (2, 2), (1, 3), (3, 3), (1, 2), (3, 2)],
    "K": [(1, 1), (3, 1), (1, 2), (1, 3), (3, 3), (2, 2)],
    "L": [(1, 0), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3)],
    "P": [(1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 2), (3, 0),(3, 2), (3, 1)],
    "T": [(1, 0), (2, 0), (3, 0), (2, 1), (2, 2), (2, 3)],
    "U": [(1, 0), (1, 1), (1, 2), (1, 3), (3, 0), (3, 1), (3, 2), (3, 3), (2, 3)],
    "Y": [(1, 1), (3, 1), (2, 2), (2, 3)],
}

# Create a directory to save the images if it doesn't exist
save_dir = "letter_imgs/"
os.makedirs(save_dir, exist_ok=True)

letter_pixel_values = {}

def create_letter_image(letter, positions):
    """
    Create and save an image of a specified letter.

    Args:
        letter (str): The letter to create an image for.
        positions (list of tuples): The pixel positions of the letter in the image.
    """
    image = np.full((image_size[0], image_size[1]), background_color, dtype=np.uint8)

    for x, y in positions:
        image[y, x] = letter_color
        letter_pixel_values[letter] = image.flatten()

    # Save the image
    # plt.imsave(f'{save_dir}/generated_{letter}.png', image, format="png") # PNG 
    np.save(f'{save_dir}/generated_{letter}.npy', image)                  # npy

# Generate and save images for each letter
for letter, positions in letters.items():
    create_letter_image(letter, positions)

# Save the dictionary of all images to a pickle file
file_path = f"{save_dir}/all_images.pkl"
with open(file_path, 'wb') as pickle_file:
    pickle.dump(letter_pixel_values, pickle_file)

print(f"Images generated and saved in the {save_dir} folder.")
