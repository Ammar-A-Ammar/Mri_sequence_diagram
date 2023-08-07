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





# Get phantom to simulate
phantom = shepp_logan(64)  # Phantom object [M, T1, T2, PD]
N = 64  # Phantom size

rf = 0.05         # Radiofrequency pulse phase shift (adjust to control contrast)
gradient_x = 0.2  # Gradient in the x-direction (adjust to control contrast)
gradient_y = 0.2  # Gradient in the y-direction (adjust to control contrast)



# Get sequence based on time
#sequence = sequence_viewer.getSequenceBasedOnTime()  # [(Time, Type, Duration, FA, Sign), ...]

# Initialize k space result
k_space_result = np.zeros((N, N), dtype=complex)

angles = np.linspace(0, 360, N)  # Angles that will be used to generate the phase shifts
gradient_indices = np.linspace(-0.5, 0.5, N, endpoint=False)  # Indices that will be used to generate the phase shifts

u_range = np.fft.fftfreq(N)
v_range = np.fft.fftfreq(N)
for pe_gradient, u in enumerate(u_range):
    for fe_gradient, v in enumerate(v_range):
        for x in range(N):
            for y in range(N):
                phase_shift = -2j * np.pi * (u * x + v * y) + rf + gradient_x * x + gradient_y * y
                k_space_result[pe_gradient,fe_gradient] += phantom[x, y] * np.exp(phase_shift)

#k_space_viewer.drawData(k_space_result, "K Space")
        
    ## Generate output
    ### Make inverse fourier transform



#result_image = np.fft.ifft2(k_space_result)


k_space_after = np.fft.fftshift(k_space_result)
plot(np.abs(k_space_after), "Magnitude of k-space")

image2 = np.fft.ifft2(k_space_after)
plot(np.abs(image2), "Restored Image")