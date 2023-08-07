import numpy as np
import matplotlib.pyplot as plt
from skimage.data import shepp_logan_phantom
from skimage.transform import radon, iradon
from phantominator import shepp_logan


# Generate a Shepp-Logan phantom image
#phantom = shepp_logan_phantom()
phantom=shepp_logan(128)

# Parameters
image_size = phantom.shape
#image_size2 = phantom2.shape

print(image_size)
#print(image_size2)

fov = 0.1  # Field of view in meters
num_samples = 128  # Number of samples in k-space
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

# Reconstruct the image using inverse Radon transform (filtered back projection)
reconstructed_image = iradon(k_space, theta=np.arange(0, 180, 180 / num_samples))

# Display the original phantom image, acquired k-space, and reconstructed image
plt.figure(figsize=(12, 4))

plt.subplot(131)
plt.imshow(phantom, cmap='gray')
plt.title("Original Phantom")

plt.subplot(132)
plt.imshow(np.abs(k_space), cmap='gray', extent=(-0.5, 0.5, -0.5, 0.5))
plt.title("Acquired k-space")

plt.subplot(133)
plt.imshow(reconstructed_image, cmap='gray')
plt.title("Reconstructed Image")

plt.tight_layout()
plt.show()
