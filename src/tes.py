import numpy as np


input_data = np.load('input_data.npy')
flat_input_data = input_data.flatten()

print(f"\n pixels \n {flat_input_data} \n ")

n_spikes = 3+5*(flat_input_data/255)


print(f"\n n_spikes \n {n_spikes} \n ")
