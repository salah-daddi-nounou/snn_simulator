"""
This script extracts specific images from the MNIST dataset and saves them as .npy files.
The script loads MNIST images from the idx3-ubyte format and saves selected images in a specified directory.

Functions:
    load_idx3_ubyte: Loads MNIST images from a given idx3-ubyte file.
"""

import numpy as np
import os
import matplotlib.pyplot as plt 

def load_idx3_ubyte(idx3_ubyte_file):
    """
    Load MNIST data from the given file path.

    Args:
        idx3_ubyte_file (str): Path to the idx3-ubyte file containing MNIST images.

    Returns:
        np.ndarray: Array of shape (num_images, rows, cols) containing the MNIST images.
    """
    with open(idx3_ubyte_file, 'rb') as f:
        magic, num_images, rows, cols = np.frombuffer(f.read(16), dtype=np.dtype('>i4'))
        assert magic == 2051, 'Invalid magic number'
        images = np.frombuffer(f.read(), dtype=np.uint8).reshape(num_images, rows, cols)
    return images

# Path to the MNIST dataset files
train_images_path = './mnist_data/train-images.idx3-ubyte'

# Load the training images
train_images = load_idx3_ubyte(train_images_path)

# Directory to save the .npy files
save_dir = 'mnist_npy/'

# Create the save directory if it doesn't exist
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Select specific images to save
# For example, save the 0th, 10th, and 100th images
selected_indices = [0, 10, 100]

for idx in selected_indices:
    np.save(f'{save_dir}image_{idx}.npy', train_images[idx])

"""
print(train_images[10])
plt.imshow(train_images[10], cmap ='gray')
plt.colorbar()
plt.show()
"""
