import pypulseq as pp
import matplotlib.pyplot as plt
import json

# Read parameters from the JSON file
with open('parameters1.json', 'r') as file:
    parameters = json.load(file)

system = pp.Opts(max_grad=32, grad_unit='mT/m', max_slew=130, slew_unit='mT/m/ms')
seq = pp.Sequence(system=system)

Nx, Ny = parameters['Nx'], parameters['Ny']
fov = parameters['fov']
delta_k = fov / Nx

# RF sinc pulse with a 90 degree flip angle
rf90 = pp.make_sinc_pulse(flip_angle=parameters['flip_angle'], duration=parameters['rf_duration'],
                         system=system, slice_thickness=parameters['slice_thickness'],
                         apodization=parameters['apodization'], time_bw_product=parameters['time_bw_product'])

# Frequency encode, trapezoidal event
gx = pp.make_trapezoid(channel='x', flat_area=Nx * delta_k, flat_time=parameters['gx_flat_time'], system=system)

# ADC readout
adc = pp.make_adc(num_samples=Nx, duration=gx.flat_time, delay=gx.rise_time, system=system)

seq.add_block(rf90)
seq.add_block(gx, adc)

# Create a custom plot to merge the RF pulse and the gradient
plt.figure()
plt.title('MRI Sequence Diagram')

# Plot RF Pulse
rf_time = rf90.t * 1e-6  # Convert to seconds
rf_amp = rf90.signal
plt.plot(rf_time, rf_amp, label='RF Pulse', color='blue')

# Plot Gradient
grad_time = gx.t * 1e-6  # Convert to seconds
grad_amp = gx.waveforms[gx.channel]
plt.plot(grad_time, grad_amp, label='Gradient', color='green')

plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()

plt.tight_layout()
plt.show()

seq.write('demo.seq')
