import numpy as np
import matplotlib.pyplot as plt
from phantominator import shepp_logan

# Load an example image (you can replace this with your own image)
#image = plt.imread("path_to_your_image.jpg")  # Make sure to provide the correct image path

image=shepp_logan(64)


def plot(image, title):
    # Display the magnitude of the filled k-space matrix
    plt.imshow(image, cmap='gray', extent=(-0.5, 0.5, -0.5, 0.5))
    plt.title(title)
    plt.xlabel("u")
    plt.ylabel("v")
    plt.colorbar()
    plt.show()
    #plt.savefig(title)


#image = shepp_logan(64)
plot(image, "Original image")

# Get image size
image_size = image.shape

# Compute spatial frequency grids
u_range = np.fft.fftfreq(image_size[0])
v_range = np.fft.fftfreq(image_size[1])

# Create a blank k-space matrix
k_space = np.zeros(image_size, dtype=np.complex128)

# Populate the k-space matrix using the Fourier Transform
for u_index, u in enumerate(u_range):
    for v_index, v in enumerate(v_range):
        for x in range(image_size[0]):
            for y in range(image_size[1]):
                signal = image[x, y] * np.exp(-2j * np.pi * (u * x + v * y))
                k_space[u_index, v_index] += signal




k_space_after = np.fft.fftshift(k_space)
plot(np.abs(k_space_after), "Magnitude of k-space")

image2 = np.fft.ifft2(k_space_after)
plot(np.abs(image2), "Restored Image")



# Display the magnitude of the filled k-space matrix
""" 
plt.imshow(np.abs(k_space), cmap='gray', extent=(-0.5, 0.5, -0.5, 0.5))
plt.title("Filled k-space Matrix from Image")
plt.xlabel("u")
plt.ylabel("v")
plt.colorbar()
plt.show() 
"""

