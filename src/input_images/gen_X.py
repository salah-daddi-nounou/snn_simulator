import numpy as np
#import cv2
import os
import matplotlib.pyplot as plt

# Number of images in the dataset
num_images = 3
# Size of each image
image_size = (5, 5)
# Directory to save the dataset
save_dir = 'generated_npy/'

# Create the save directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

for i in range(num_images):
    # Create a blank image
    image = np.zeros((image_size[0], image_size[1]), dtype=np.uint8)
    
    # Set the fixed position for the letter "X"
    x_pos = 1
    y_pos = 1
    
    # Set the different intensity values for the "X" pixels
    #pixel_values = np.random.randint(50, 256, size=5, dtype=np.uint8)
    pixel_values = 255*np.ones(5, dtype=np.uint8)
    
    # Draw the letter "X" on the image with varying intensities
    image[y_pos, x_pos] = pixel_values[0]
    image[y_pos + 1, x_pos + 1] = pixel_values[1]
    image[y_pos + 2, x_pos + 2] = pixel_values[2]
    image[y_pos, x_pos + 2] = pixel_values[3]
    image[y_pos + 2, x_pos] = pixel_values[4]
    
    # Save the image to disk
    #cv2.imwrite(f'{save_dir}/mnist_{i}.png', image)   to save a .png format image 
    np.save(f'{save_dir}/generated_{i}.npy', image)


#print("X image shape {} and siez {} ".format(np.shape(input_data), np.size(input_data) ))
