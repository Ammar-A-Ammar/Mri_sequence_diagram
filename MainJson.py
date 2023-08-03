import copy
import matplotlib.pyplot
import mrsd
import math
from math import degrees
import json

with open('parameters.json', 'r') as file:
    params = json.load(file)

# Extract the TE sets from the params dictionary
TE_sets = params['TE']
TR = params.get('TR', 10)
d_ramp = params.get('d_ramp', 0.1)
d_pulse = params.get('d_pulse', 1)
d_encoding = params.get('d_encoding', 1)
duration_global = params.get('duration', 2)
alternate = params.get('alternate', 1)
flip_angle = params.get('flip_angle', 90)

# Function to create a diagram for a given TE set
def create_diagram_for_te(te_params):
    TE = te_params['duration']
    alpha = math.radians(te_params['degree'])
    

    # Create the underlying Matplotlib objects and the diagram
    figure, plot = matplotlib.pyplot.subplots(tight_layout=True)
    diagram = mrsd.Diagram(
        plot, ["RF", "$G_{slice}$", "$G_{phase}$", "$G_{readout}$", "Signal"])

    # Readout, centered on TE
    adc, echo, readout = diagram.readout(
        "Signal", "$G_{readout}$", duration_global, ramp=d_ramp, center=TE,
        adc_kwargs={"ec": "0.5"})

    # Encoding: rewind slice-selection gradient, run phase gradient, prephase
    # read-out gradient
    if alternate == 0:
        # Slice-selective pulse of the first TR
        excitation, slice_selection = diagram.selective_pulse(
            "RF", "$G_{slice}$", d_pulse, alpha, ramp=d_ramp, center=0)
        diagram.add("$G_{slice}$", slice_selection.adapt(d_encoding, -0.5, d_ramp, end=readout.begin))
        diagram.multi_gradient("$G_{phase}$", d_encoding, 1, d_ramp, end=readout.begin)
        diagram.add("$G_{readout}$", readout.adapt(d_encoding, -0.5, d_ramp, end=readout.begin))
        # Start of next TR
        diagram.add("RF", copy.copy(excitation).move(TR))
        diagram.add("$G_{slice}$", copy.copy(slice_selection).move(TR))
    else:
        # Create the underlying Matplotlib objects and the diagram
        diagram = mrsd.Diagram(plot, ["RF", "$G_{phase}$", "$G_{slice}$", "$G_{readout}$", "Signal"])

        # Slice-selective pulse of the first TR
        excitation, slice_selection = diagram.selective_pulse(
            "RF", "$G_{slice}$", d_pulse, alpha, ramp=d_ramp, center=0)

        diagram.multi_gradient("$G_{phase}$", d_encoding, 1, d_ramp, end=readout.begin)
        diagram.add("$G_{slice}$", slice_selection.adapt(d_encoding, -0.5, d_ramp, end=readout.begin))
        diagram.add("$G_{readout}$", readout.adapt(d_encoding, -0.5, d_ramp, end=readout.begin))
        # Start of next TR
        diagram.add("RF", copy.copy(excitation).move(TR))
        diagram.add("$G_{slice}$", copy.copy(slice_selection).move(TR))

    # Add annotations: flip angles and TE/TR intervals
    diagram.annotate("RF", 0.2, 1, r"$\alpha$ = " + str(te_params['degree']))
    diagram.annotate("RF", TR + 0.2, 1, r"$\alpha$ = " + str(te_params['degree']))
    diagram.interval(0, TE, -1.5, "TE")
    diagram.interval(0, TR, -2.5, "TR")

    return diagram

# Create diagrams for each TE set
for te_params in TE_sets:
    diagram = create_diagram_for_te(te_params)
    matplotlib.pyplot.show()
