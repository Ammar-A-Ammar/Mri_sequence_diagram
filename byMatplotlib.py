import matplotlib.pyplot as plt
import numpy as np

# Define sequence parameters (arbitrary units): echo and repetition times,
# durations of ramp, pulses, encoding, and readout
TE, TR = 1, 10
d_ramp, d_pulse, d_encoding, duration = 0.1, 1, 1, 2
alternate = 1
flip_angle = 90

# Create the underlying Matplotlib objects and the diagram
figure, axes = plt.subplots(5, 1, sharex=True, tight_layout=True)

# Function to plot an RF pulse with given parameters
def plot_rf_pulse(ax, center, duration, flip_angle):
    t = np.linspace(center - duration / 2, center + duration / 2, 100)
    rf_pulse = np.sin(2 * np.pi * t / duration) * flip_angle
    ax.plot(t, rf_pulse, label="RF Pulse")

# Function to plot a gradient with given parameters
def plot_gradient(ax, center, duration, amplitude, sign):
    t = np.linspace(center - duration / 2, center + duration / 2, 100)
    gradient = np.ones_like(t) * amplitude * sign
    ax.plot(t, gradient, label="Gradient")

# Readout, centered on TE
readout_center = TE + duration / 2
plot_gradient(axes[3], readout_center, duration, 1, -1)

# Encoding: rewind slice-selection gradient, run phase gradient, prephase read-out gradient
if alternate == 0:
    # Slice-selective pulse of the first TR
    rf1_center = 0
    plot_rf_pulse(axes[0], rf1_center, d_pulse, flip_angle)
    plot_gradient(axes[1], rf1_center, d_encoding, 0.5, 1)

    phase_center = readout_center
    plot_gradient(axes[2], phase_center, d_encoding, 1, 1)

    rf2_center = TR
    plot_rf_pulse(axes[0], rf2_center, d_pulse, flip_angle)
    plot_gradient(axes[1], rf2_center, d_encoding, 0.5, 1)
else:
    rf1_center = 0
    plot_rf_pulse(axes[0], rf1_center, d_pulse, flip_angle)
    plot_gradient(axes[1], rf1_center, d_encoding, 0.5, 1)

    phase_center = readout_center
    plot_gradient(axes[2], phase_center, d_encoding, 1, 1)

    rf2_center = TR
    plot_rf_pulse(axes[0], rf2_center, d_pulse, flip_angle)
    plot_gradient(axes[1], rf2_center, d_encoding, 0.5, 1)

# Add annotations: flip angles and TE/TR intervals
axes[0].annotate(f"Flip Angle: {flip_angle}°", (0.2, flip_angle), xytext=(0.2, flip_angle + 20),
                 arrowprops=dict(arrowstyle="->"))
axes[0].annotate(f"Flip Angle: {flip_angle}°", (TR + 0.2, flip_angle), xytext=(TR + 0.2, flip_angle + 20),
                 arrowprops=dict(arrowstyle="->"))
axes[0].set_ylabel('Amplitude (RF)')
axes[1].set_ylabel('Amplitude (G slice)')
axes[2].set_ylabel('Amplitude (G phase)')
axes[3].set_ylabel('Amplitude (G readout)')
axes[4].set_ylabel('Signal')
axes[4].set_xlabel('Time')
axes[0].legend()

plt.show()
