import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python script_name.py simulations folder_name")
    sys.exit(1)

folder_name = sys.argv[1]

data = np.genfromtxt(f"{folder_name}/results.txt", delimiter="", skip_header=4)
# structure of data :    
#                    time | synapse1 | synapse2 | ... | membrane_out_neuron

init_weights_flat = data[0, 1:-1]
#init_weights_flat = data[-1, 1:26]
init_weights_img = init_weights_flat.reshape((5,5))

final_weights_flat = data[-1, 1:-1]
#final_weights_flat = data[-1, 26:51]
final_weights_img = final_weights_flat.reshape((5,5))

# Update matplotlib global parameters for font
plt.rcParams.update({'font.size': 14, 'font.family': 'serif'})

# Plot the weights history
fig, (axe1, axe2) = plt.subplots(2, 1, figsize=(5, 10))
axe1.plot(1e3*data[:, 0], data[:, 1:-1])
axe1.set_title("Weights history")
axe1.set_xlabel("time (ms)"); axe1.set_ylabel("Weight state")
axe1.grid(True)

# Plot output neuron membrane potential
axe2.plot(1e3*data[:, 0], 1e3*data[:, -1], color="green")
axe2.set_title("Output neuron membrane potential")
axe2.set_xlabel("time (ms)"); axe2.set_ylabel("mem potential (mV)")
axe2.grid(True)

fig2, (axe3, axe4) = plt.subplots(1, 2, figsize=(8, 4))
# Display the initial weights
im3 = axe3.imshow(init_weights_img, cmap='gray') #'gray_r'
axe3.set_title("Initial Weights")
axe3.axis('off')
cbar1 = plt.colorbar(im3, ax=axe3)
cbar1.locator = MaxNLocator(integer=True)
cbar1.update_ticks()

# Display the final trained weights
im4 = axe4.imshow(final_weights_img, cmap='gray')
axe4.set_title("Trained Weights")
axe4.axis('off')
cbar2 = plt.colorbar(im4, ax=axe4)
cbar2.locator = MaxNLocator(integer=True)
cbar2.update_ticks()

plt.tight_layout()
# save figure 2 in home directory 
#plt.savefig(os.path.join(os.path.expanduser("~"), os.path.basename(folder_name) + ".pdf"), format='pdf')

plt.show()

