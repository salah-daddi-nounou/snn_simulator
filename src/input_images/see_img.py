
import numpy as np
import os
import matplotlib.pyplot as plt 

input = "letter_imgs/generated_K.npy"
#input = "./mnist_npy/image_10.npy"

image = np.load(input)
print(f"size is: {np.size(image)} and shape is {np.shape(image)} ")

plt.imshow(image, cmap ='gray')
plt.colorbar()
plt.show()


