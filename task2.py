import numpy as np
import matplotlib.pyplot as plt
from phantominator import shepp_logan
import cv2

# Load an input image
#input_image_path = 'Figure_1.png'
#input_image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
input_image=shepp_logan(128)

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
plot(input_image, "Original image")


# Parameters
image_size = input_image.shape
fov = 0.2  # Field of view in meters
num_samples = 2048  # Number of samples in k-space
T1 = 800.0  # T1 relaxation time in ms
T2 = 100.0  # T2 relaxation time in ms

# Create spatial frequency ranges
u_range = np.fft.fftfreq(image_size[0], fov / image_size[0])
v_range = np.fft.fftfreq(image_size[1], fov / image_size[1])

# Create a blank k-space matrix
k_space = np.zeros((num_samples, num_samples), dtype=np.complex128)

# Simulate MRI acquisition process
for u_index, u in enumerate(u_range):
    for v_index, v in enumerate(v_range):
        # Simulate gradient encoding
        gradient_x = 2 * np.pi * u * fov
        gradient_y = 2 * np.pi * v * fov

        # Simulate RF pulse and relaxation effects
        signal = np.exp(-1j * (gradient_x + gradient_y)) * \
                 np.exp(-num_samples / T2) * (1 - np.exp(-num_samples / T1))

        # Fill k-space
        k_space[u_index, v_index] = signal

# Display the magnitude of the filled k-space matrix

""" 
plt.imshow(np.abs(k_space), cmap='gray', extent=(-0.5, 0.5, -0.5, 0.5))
plt.title("Filled k-space Matrix (Simulated MRI)")
plt.xlabel("u")
plt.ylabel("v")
plt.colorbar()
plt.show() 

"""


k_space_after = np.fft.fftshift(k_space)
plot(np.abs(k_space_after), "Magnitude of k-space")

image = np.fft.ifft2(k_space_after)
plot(np.abs(image), "Magnitude of k-space")