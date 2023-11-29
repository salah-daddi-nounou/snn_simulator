import numpy as np
import os
from matplotlib import pyplot as plt
import pickle

# Load the all_images dictionary from the pickle file
all_images = "input_images/letter_imgs/all_images.pkl"
with open(all_images, 'rb') as pickle_file:
        images = pickle.load(pickle_file)

# Choose and load a network trained to recgnize one image
trained = "../../snn_sim_folders/dat_1027_1243_pross_5424/"
data = np.genfromtxt(f"{trained}/results.txt", delimiter="", skip_header=4)
# data structure :    
#                    time | synapse1 | synapse2 | ... | membrane_out_neuron
final_weights_flat = data[-1, 1:-1]

# Dictionary to store dot products between all images and the trained network
dot_product_results = {}

# Calculate dot product for each entry in the dictionary
for letter, pixel_values in images.items():
        dot_product = np.dot(final_weights_flat, (pixel_values/255.0))  
        dot_product_results[letter] = dot_product

# Print the results
for letter, dot_product in dot_product_results.items():
    print(f"Dot Product for '{letter}': {dot_product}")

