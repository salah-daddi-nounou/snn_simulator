import numpy as np
import os
import glob
import pickle
import matplotlib.pyplot as plt

# Load the all_images dictionary from the pickle file
all_images = "input_images/letter_imgs/all_images.pkl"
with open(all_images, 'rb') as pickle_file:
    images = pickle.load(pickle_file)

# Choose a specific letter's image
#specific_letter = 'I'  # Change to your desired letter
#specific_letter = 'O'  # Change to your desired letter
specific_letter = 'F'  # Change to your desired letter

specific_letter_image = images[specific_letter]

# Base directory of trained networks
#base_dir = "../../snn_sim_folders/dat_1218_1347_pross_25*"  # Adjust this pattern to match your folders
#base_dir = "../../snn_sim_folders/dat_1218_1425_pross_119*"  # Adjust this pattern to match your folders
base_dir = "../../snn_sim_folders/dat_1218_1507_pross_2*"  # Adjust this pattern to match your folders

# Retrieve and sort the list of trained network folders
trained_folders = sorted(glob.glob(base_dir))

# Initialize a structure to hold the distances
euclidean_distances = {}

# Loop through each folder, calculate Euclidean distance, and store it
for trained_folder in trained_folders:
    # Extract dev and num_cells from the folder name
    folder_name = os.path.basename(trained_folder)
    parts = folder_name.split('_')
    dev = float(parts[-2].replace('dev', ''))
    num_cells = int(parts[-1].replace('cells', ''))

    # Initialize nested dictionary if necessary
    if num_cells not in euclidean_distances:
        euclidean_distances[num_cells] = {}
    if dev not in euclidean_distances[num_cells]:
        euclidean_distances[num_cells][dev] = []

    # Load the network data
    data_file = os.path.join(trained_folder, "results.txt")
    if os.path.exists(data_file):
        data = np.genfromtxt(data_file, delimiter="", skip_header=4)
        final_weights_flat = data[-1, 1:-1]

        # Calculate Euclidean distance
        euclidean_distance = np.linalg.norm(final_weights_flat/num_cells - (specific_letter_image/255.0))

        # Store the distance
        euclidean_distances[num_cells][dev].append(euclidean_distance)

# Plotting
for num_cells, dev_distances in euclidean_distances.items():
    devs = sorted(dev_distances.keys())
    distances = [dev_distances[dev][0] for dev in devs]  # Assuming one value per dev

    plt.plot(devs, distances, label=f'num_cells={num_cells}', marker='o')

plt.xlabel('Deviation')
plt.ylabel('Euclidean Distance')
plt.title(f'Euclidean Distance vs Deviation for Letter "{specific_letter}"')
plt.legend()
plt.show()

