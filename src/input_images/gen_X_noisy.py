import numpy as np
import cv2
import os

# Number of images in the dataset
num_images = 10
# Size of each image
image_size = (5, 5)
# Directory to save the dataset
save_dir = 'dataset/'

# Create the save directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

for i in range(num_images):
    # Create a blank image with random background noise
    image = np.random.randint(0, 150, size=(image_size[0], image_size[1]), dtype=np.uint8)
    
    # Generate a random position for the letter "X"
    x_pos = 1#np.random.randint(0, image_size[1] - 2)
    y_pos = 1#np.random.randint(0, image_size[0] - 2)
    
    # Draw the letter "X" on the image
    image[y_pos, x_pos] = 255
    image[y_pos + 1, x_pos + 1] = 255
    image[y_pos + 2, x_pos + 2] = 255
    image[y_pos, x_pos + 2] = 255
    image[y_pos + 1, x_pos + 1] = 255
    image[y_pos + 2, x_pos] = 255
    
    # Save the image to disk
    cv2.imwrite(f'{save_dir}/{i}.png', image)

