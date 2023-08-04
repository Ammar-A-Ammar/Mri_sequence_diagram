import copy
import matplotlib.pyplot
import mrsd
import math
from math import degrees
import json

# Define sequence parameters (arbitrary units): echo and repetition times,
# durations of ramp, pulses, encoding and readout
# initials

TE, TR = 1, 10
d_ramp, d_pulse, d_encoding, duration = 0.1, 1, 1, 2
flip_angle = 90

with open('parameters.json', 'r') as file:
    params = json.load(file)

# Update the parameters with JSON data
TE = params.get('TE', TE)
TR = params.get('TR', TR)
d_ramp = params.get('d_ramp', d_ramp)
d_pulse = params.get('d_pulse', d_pulse)
d_encoding = params.get('d_encoding', d_encoding)
duration = params.get('duration', duration)
flip_angle = params.get('flip_angle', flip_angle)
alpha = math.radians(flip_angle)

# Create the underlying Matplotlib objects and the diagram
figure, plot = matplotlib.pyplot.subplots(tight_layout=True)
diagram = mrsd.Diagram(
    plot, ["RF", "$G_{slice}$", "$G_{phase}$", "$G_{readout}$", "Signal"])
# Readout, centered on TE
adc, echo, readout = diagram.readout(
    "Signal", "$G_{readout}$", duration, ramp=d_ramp, center=TE,
    adc_kwargs={"ec": "0.5"})

# Encoding: rewind slice-selection gradient, run phase gradient, prephase

# read-out gradient

excitation, slice_selection = diagram.selective_pulse("RF", "$G_{slice}$", d_pulse, alpha, ramp=d_ramp, center=0)
diagram.add("$G_{slice}$", slice_selection.adapt(d_encoding, -0.5, d_ramp, end=readout.begin))
diagram.multi_gradient("$G_{phase}$", d_encoding, 1, d_ramp, end=readout.begin)
diagram.add("$G_{readout}$", readout.adapt(d_encoding, -0.5, d_ramp, end=readout.begin))
# Start of next TR
diagram.add("RF", copy.copy(excitation).move(TR))
diagram.add("$G_{slice}$", copy.copy(slice_selection).move(TR))

# Add annotations: flip angles and TE/TR intervals
diagram.annotate("RF", 0.2, 1, r"$\alpha$ = " + str(flip_angle))
diagram.annotate("RF", TR + 0.2, 1, r"$\alpha$ = " + str(flip_angle))
diagram.interval(0, TE, -1.5, "TE")
diagram.interval(0, TR, -2.5, "TR")

diagram.rf_pulse("RF",1.5,0.5,center=5)
diagram.gradient("$G_{slice}$",1.5,0.5,center=5)

matplotlib.pyplot.show()
