"""
This module calculates and plots the Euclidean distance between the final weights of trained SNNs 
and the input images. The module provides functions to compute the distances for individual letters as well as average 
distances across multiple letters.

Functions:
    eucl_dist: Calculate and plot Euclidean distances for a specific letter.
    avg_eucl_dist: Calculate and plot average Euclidean distances across multiple letters.
    calculate_dist: Helper function to calculate Euclidean distances for a given letter.
    plot_distances: Helper function to plot the Euclidean distances.

Example Usage:
```python
eucl_dist(trained_letters_dict, 'I')
avg_eucl_dist(trained_letters_dict)
```
"""

import numpy as np
import os
import glob
import pickle
import matplotlib.pyplot as plt

'''
Input images are stored in binary formats (individually: .npy arrays, 
and collectively: .pkl dict) all files were generated at once. 
'''

'''
trained_letters_dict = {
    'C': "../../snn_sim_folders/dat_1218_1212_pross_414*",
    'I': "../../snn_sim_folders/dat_1218_1347_pross_25*",
    'O': "../../snn_sim_folders/dat_1218_1425_pross_119*",
#    'F': "../../snn_sim_folders/dat_1218_1507_pross_2*",
    'H': "../../snn_sim_folders/dat_1218_1713_pross_40*",
    'L': "../../snn_sim_folders/dat_1220_1034_pross_421*",
    'P': "../../snn_sim_folders/dat_1220_1117_pross_56*",
    'K': "../../snn_sim_folders/dat_1220_1146_pross_160*",
#    'O': "../../snn_sim_folders/dat_1220_1427_pross_104*",  #double
    'F': "../../snn_sim_folders/dat_1220_1459_pross_272*",  #double
    'T': "../../snn_sim_folders/dat_1220_1602_pross_67*",
    'U': "../../snn_sim_folders/dat_1220_1649_pross_155*",
}
'''

# 'C': "../../snn_sim_folders/dat_1222_*_pross_*_letC*"

trained_letters_dict = {
    'C': "../../snn_sim_folders/dat_1225_*_pross_*_letC*",
    'I': "../../snn_sim_folders/dat_1225_*_pross_*_letI*", 
    'O': "../../snn_sim_folders/dat_1225_*_pross_*_letO*",
    'F': "../../snn_sim_folders/dat_1225_*_pross_*_letF*",
    'H': "../../snn_sim_folders/dat_1225_*_pross_*_letH*",
    'L': "../../snn_sim_folders/dat_1225_*_pross_*_letL*",
    'P': "../../snn_sim_folders/dat_1225_*_pross_*_letP*",
    'K': "../../snn_sim_folders/dat_1225_*_pross_*_letK*",
    'T': "../../snn_sim_folders/dat_1225_*_pross_*_letT*",
#    'U': "../../snn_sim_folders/dat_1225_*_pross_*_letU*",
    'X': "../../snn_sim_folders/dat_1225_*_pross_*_letX*",
}

VR_std = [i / 100 for i in range(0, 25, 5)]
mtjs = [2, 4, 6, 8]

def eucl_dist(trained_letters_dict, specific_letter):
    """
    Calculate and plot Euclidean distances for a specific letter.

    Args:
        trained_letters_dict (dict): Dictionary containing base directories for trained letters.
        specific_letter (str): The letter to calculate distances for.
    """
    # Load the all_images dictionary from the pickle file
    all_images = "input_images/letter_imgs/all_images.pkl"
    with open(all_images, 'rb') as pickle_file:
        images = pickle.load(pickle_file)

    specific_letter_image = images[specific_letter]
    base_dir = trained_letters_dict.get(specific_letter)
    
    if base_dir:
        euclidean_distances = calculate_dist(base_dir, specific_letter_image)
        plot_distances(euclidean_distances, f'Euclidean Distance vs VR_std for Letter "{specific_letter}"')
    else:
        print(f"Base directory for letter '{specific_letter}' not found in the provided dictionary.")

def avg_eucl_dist(trained_letters_dict):
    """
    Calculate and plot average Euclidean distances across multiple letters.

    Args:
        trained_letters_dict (dict): Dictionary containing base directories for trained letters.
    """
    # Load the all_images dictionary from the pickle file
    all_images = "input_images/letter_imgs/all_images.pkl"
    with open(all_images, 'rb') as pickle_file:
        images = pickle.load(pickle_file)

    # Initialize a structure to hold the distances
    average_distances = {nc: {dev: [] for dev in VR_std} for nc in mtjs}
    
    for letter, base_dir in trained_letters_dict.items():
        specific_letter_image = images[letter]
        euclidean_distances = calculate_dist(base_dir, specific_letter_image)
        
        # Accumulate the distances for averaging
        for num_cells in mtjs:
            for dev in VR_std:
                average_distances[num_cells][dev] += euclidean_distances[num_cells][dev]

    # Average the distances across letters
    for num_cells in mtjs:
        for dev in VR_std:
            if average_distances[num_cells][dev]:
                average_distances[num_cells][dev] = np.mean(average_distances[num_cells][dev])
            else:
                average_distances[num_cells][dev] = None

    plot_distances(average_distances, 'Average Euclidean Distance vs VR_std Across Letters')

def calculate_dist(base_dir, letter_image):
    """
    Helper function to calculate Euclidean distances for a given letter.

    Args:
        base_dir (str): Base directory containing the trained folders.
        letter_image (numpy.ndarray): The image of the specific letter.

    Returns:
        dict: Dictionary containing Euclidean distances for each combination of num_cells and VR_std.
    """
    trained_folders = sorted(glob.glob(base_dir))
    euclidean_distances = {nc: {dev: [] for dev in VR_std} for nc in mtjs}

    for trained_folder in trained_folders:
        folder_name = os.path.basename(trained_folder)
        parts = folder_name.split('_')
        dev = float(parts[-2].replace('dev', ''))
        num_cells = int(parts[-1].replace('cells', ''))

        data_file = os.path.join(trained_folder, "results.txt")
        if os.path.exists(data_file):
            data = np.genfromtxt(data_file, delimiter="", skip_header=4)
            final_weights_flat = data[-1, 1:-1]
            euclidean_distance = np.linalg.norm(final_weights_flat/num_cells - (letter_image/255.0))
            euclidean_distances[num_cells][dev].append(euclidean_distance)
    
    return euclidean_distances

def plot_distances(euclidean_distances, title):
    """
    Helper function to plot the Euclidean distances.

    Args:
        euclidean_distances (dict): Dictionary containing Euclidean distances to plot.
        title (str): Title of the plot.
    """
    fig, axe1 = plt.subplots()
    for num_cells, dev_distances in euclidean_distances.items():
        devs = sorted(dev_distances.keys())
        distances = [np.mean(dev_distances[dev]) for dev in devs]
        axe1.plot(devs, distances, label=f'num_cells={num_cells}', marker='o')

    axe1.set_xlabel('VR_std')
    axe1.set_ylabel('Euclidean Distance')
    axe1.set_title(title)
    axe1.legend()

# To calculate for a single letter
eucl_dist(trained_letters_dict, 'I')
# eucl_dist(trained_letters_dict, 'C')
# eucl_dist(trained_letters_dict, 'K')
eucl_dist(trained_letters_dict, 'L')
# eucl_dist(trained_letters_dict, 'P')
# eucl_dist(trained_letters_dict, 'H')
eucl_dist(trained_letters_dict, 'O')
# eucl_dist(trained_letters_dict, 'F')
# eucl_dist(trained_letters_dict, 'T')
eucl_dist(trained_letters_dict, 'U')

# To calculate the average across multiple letters
avg_eucl_dist(trained_letters_dict)
plt.show()
