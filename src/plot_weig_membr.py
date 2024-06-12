"""
This script processes and plots simulation results for an SNN.
It loads data from a specified results file, plots the weights history, the output 
neuron membrane potential, and compares initial and final weights.

Functions:
    parse_arguments: Parse command-line arguments.
    load_data: from results.txt, organized as :  time | synapse1 | synapse2 | ... | membrane_out_neuron.
    plot_weights_history: Plot the weights history.
    plot_membrane_potential: Plot the output neuron membrane potential.
    plot_weights_comparison: Plot initial and final weights comparison.
    main: Main function to orchestrate loading data and plotting results.

Example Usage:
```
>> python plot_weig_membr.py simulations_folder_name
```
"""
                   
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os
import sys
import argparse

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Plot simulation results.")
    parser.add_argument("folder_name", help="Folder containing the simulation results.")
    return parser.parse_args()

def load_data(folder_name):
    """Load data from the results file."""
    file_path = os.path.join(folder_name, "results.txt")
    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} does not exist.")
        sys.exit(1)
    return np.genfromtxt(file_path, delimiter="", skip_header=4)

def plot_weights_history(data):
    """Plot the weights history."""
    plt.figure(figsize=(5, 5))
    plt.plot(1e3 * data[:, 0], data[:, 1:-1])
    plt.title("Weights history")
    plt.xlabel("Time (ms)")
    plt.ylabel("Weight state")
    plt.grid(True)

def plot_membrane_potential(data):
    """Plot the output neuron membrane potential."""
    plt.figure(figsize=(5, 5))
    plt.plot(1e3 * data[:, 0], 1e3 * data[:, -1], color="green")
    plt.title("Output neuron membrane potential")
    plt.xlabel("Time (ms)")
    plt.ylabel("Mem potential (mV)")
    plt.grid(True)

def plot_weights_comparison(init_weights_img, final_weights_img):
    """Plot initial and final weights comparison."""
    fig, (axe1, axe2) = plt.subplots(1, 2, figsize=(8, 4))

    im1 = axe1.imshow(init_weights_img, cmap='gray')
    axe1.set_title("Initial Weights")
    axe1.axis('off')
    cbar1 = plt.colorbar(im1, ax=axe1)
    cbar1.locator = MaxNLocator(integer=True)
    cbar1.update_ticks()

    im2 = axe2.imshow(final_weights_img, cmap='gray')
    axe2.set_title("Trained Weights")
    axe2.axis('off')
    cbar2 = plt.colorbar(im2, ax=axe2)
    cbar2.locator = MaxNLocator(integer=True)
    cbar2.update_ticks()

    plt.tight_layout()
    return fig

def main():
    """Main function to orchestrate loading data and plotting results."""
    args = parse_arguments()
    data = load_data(args.folder_name)

    init_weights_flat = data[0, 1:-1]
    init_weights_img = init_weights_flat.reshape((5, 5))

    final_weights_flat = data[-1, 1:-1]
    final_weights_img = final_weights_flat.reshape((5, 5))

    # Update matplotlib global parameters for font
    plt.rcParams.update({'font.size': 14, 'font.family': 'serif'})

    plot_weights_history(data)
    plot_membrane_potential(data)
    fig = plot_weights_comparison(init_weights_img, final_weights_img)

    # Save figure to home directory if needed
    # plt.savefig(os.path.join(os.path.expanduser("~"), os.path.basename(args.folder_name) + ".pdf"), format='pdf')

    plt.show()

if __name__ == "__main__":
    main()
