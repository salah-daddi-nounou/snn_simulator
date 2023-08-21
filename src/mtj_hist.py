import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 2:
    print("Usage: python script_name.py folder_name")
    sys.exit(1)

folder_name = sys.argv[1]

data = np.genfromtxt(f"{folder_name}/results.txt", delimiter="", skip_header=4)
# data structure :    
#                    time | synapse1 | synapse2 | ... | membrane_out_neuron

init_weights_flat = data[0, 1:-1]
init_weights_img = init_weights_flat.reshape((5, 5))

final_weights_flat = data[-1, 1:-1]
final_weights_img = final_weights_flat.reshape((5, 5))

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
axe3.imshow(init_weights_img, cmap='gray_r')
axe3.set_title("Initial Weights")
axe3.axis('off')

# Display the final trained weights 
axe4.imshow(final_weights_img, cmap='gray_r')
axe4.set_title("trained weights")
axe4.axis('off')

plt.tight_layout()  
plt.show()

