
import numpy as np
import os
import matplotlib.pyplot as plt 

#input = "./generated_npy/generated_1.npy"
input = "./mnist_npy/image_10.npy"

image = np.load(input)
plt.imshow(image, cmap ='gray')
plt.colorbar()
plt.show()

