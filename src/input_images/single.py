import numpy as np
import os
from matplotlib import pyplot as plt
import pickle

# Define image size and letter colors
image_size = (1,1)
background_color = 0  # Black
letter_color = 0

# Define the letters and their positions
letters = {
    "single": [(0, 0)]
}

# Create a directory to save the images if it doesn't exist
save_dir = "letter_imgs/"
os.makedirs(save_dir, exist_ok=True)

letter_pixel_values = {}
# Function to create and save letter images
def create_letter_image(letter, positions):
    image = np.full((image_size[0], image_size[1]), background_color, dtype=np.uint8)

    for x, y in positions:
        image[y, x] = letter_color
        letter_pixel_values[letter] = image.flatten()

    # Save the image
    #plt.imsave(f'{save_dir}/generated_{letter}.png', image, format="png") # PNG 
    np.save(f'{save_dir}/generated_{letter}.npy', image)                  # npy

# Generate and save images for each letter
for letter, positions in letters.items():
    create_letter_image(letter, positions)
'''
# Save the dictionary of all images to a pickle file
file_path = f"{save_dir}/all_images.pkl"
with open(file_path, 'wb') as pickle_file:
        pickle.dump(letter_pixel_values, pickle_file)
'''
print(f"Images generated and saved in the {save_dir} folder.")
