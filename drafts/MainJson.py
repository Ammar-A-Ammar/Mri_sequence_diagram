import copy
import matplotlib.pyplot as plt
import mrsd
import math
from math import degrees
import json

# Read parameters from the JSON file
with open('parameters.json', 'r') as file:
    params = json.load(file)

# Update the parameters with JSON data
TE = params.get('TE', 10)
TR = params.get('TR', 10)
d_ramp = params.get('d_ramp', 0.1)
d_pulse = params.get('d_pulse', 1)
d_encoding = params.get('d_encoding', 1)
duration = params.get('duration', 2)
alternate = params.get('alternate', 1)
flip_angle = params.get('flip_angle', 90)

# Function to create RF pulse and gradients
def create_pulse_and_gradients(diagram, RF_params, gradient_params, RF_suffix):
    duration = RF_params.get('duration', 1)
    distance = RF_params.get('distance', 0.5)
    degree = RF_params.get('degree', 90)
    sign = RF_params.get('sign', 1)

    alpha = math.radians(degree)
    center = distance / (2 * d_ramp)  # Calculate the center based on distance and ramp duration

    excitation, slice_selection = diagram.selective_pulse(
        "RF" + RF_suffix, "$G_{slice}$", duration, alpha, ramp=d_ramp, center=center)

    # Apply the RF phase using a gradient reversal
    slice_selection.rotate(math.pi * sign)

    gradient_params["duration"] = duration
    gradient_params["sign"] = sign
    diagram.add("$G_" + gradient_params['axis'] + RF_suffix + "$",
                mrsd.trapezoid(gradient_params))

    diagram.multi_gradient("$G_{phase}$", d_encoding, 1, d_ramp, end=readout.begin)
    diagram.add("$G_{readout}$", readout.adapt(d_encoding, -0.5, d_ramp, end=readout.begin))
    # Start of next TR
    diagram.add("RF" + RF_suffix, copy.copy(excitation).move(TR))
    diagram.add("$G_{slice}$", copy.copy(slice_selection).move(TR))

# Create the underlying Matplotlib objects and the diagram
figure, plot = plt.subplots(tight_layout=True)
diagram = mrsd.Diagram(
    plot, ["RF", "$G_{slice}$", "$G_{phase}$", "$G_{readout}$", "Signal"])

# Readout, centered on TE
adc, echo, readout = diagram.readout(
    "Signal", "$G_{readout}$", duration, ramp=d_ramp, center=TE,
    adc_kwargs={"ec": "0.5"})

# Check if RF_1 exists in the parameters and create the first RF pulse and gradients
if 'RF_1' in params:
    RF1_params = params['RF_1']
    gradient_x_1_params = params.get('gradient_x_1', {})
    create_pulse_and_gradients(diagram, RF1_params, gradient_x_1_params, "_1")

# Check if RF_2 exists in the parameters and create the second RF pulse and gradients
if 'RF_2' in params:
    RF2_params = params['RF_2']
    gradient_y_1_params = params.get('gradient_y_1', {})
    create_pulse_and_gradients(diagram, RF2_params, gradient_y_1_params, "_2")

# Check if RF_3 exists in the parameters and create the third RF pulse and gradients
if 'RF_3' in params:
    RF3_params = params['RF_3']
    readout_1_params = params.get('readout_1', {})
    create_pulse_and_gradients(diagram, RF3_params, readout_1_params, "_3")

# Add annotations: flip angles and TE/TR intervals
diagram.annotate("RF", 0.2, 1, r"$\alpha$ = " + str(flip_angle))
diagram.annotate("RF", TR + 0.2, 1, r"$\alpha$ = " + str(flip_angle))
diagram.interval(0, TE, -1.5, "TE")
diagram.interval(0, TR, -2.5, "TR")

plt.show()
