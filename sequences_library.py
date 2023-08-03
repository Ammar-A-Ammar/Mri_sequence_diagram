#from mri_sequence_diagram import SequenceDiagram

# Define sequence parameters (arbitrary units): echo and repetition times,
# durations of ramp, pulses, encoding, and readout
TE, TR = 1, 10
d_ramp, d_pulse, d_encoding, duration = 0.1, 1, 1, 2
alternate = 1
flip_angle = 90

# Create the MRI sequence diagram
diagram = SequenceDiagram()

# Add RF pulse
diagram.add_rf_pulse(0, d_pulse, flip_angle)

# Add G slice gradient
diagram.add_gradient("G slice", 0, d_encoding, 0.5)

# Add G phase gradient
phase_center = TE + duration / 2
diagram.add_gradient("G phase", phase_center, d_encoding, 1)

# Readout gradient
readout_center = TE + duration / 2
diagram.add_gradient("G readout", readout_center, duration, -1)

# Encoding: rewind slice-selection gradient, run phase gradient, prephase read-out gradient
if alternate == 0:
    # Start of next TR
    diagram.add_rf_pulse(TR, d_pulse, flip_angle)

    # Add G slice gradient for next TR
    diagram.add_gradient("G slice", TR, d_encoding, 0.5)
else:
    # Add G slice gradient for next TR
    diagram.add_gradient("G slice", TR, d_encoding, 0.5)

    # Start of next TR
    diagram.add_rf_pulse(TR, d_pulse, flip_angle)

# Set annotations for flip angles and TE/TR intervals
diagram.annotate_rf_pulse(0.2, flip_angle, text=r"$\alpha$")
diagram.annotate_rf_pulse(TR + 0.2, flip_angle, text=r"$\alpha$")
diagram.annotate_interval(0, TE, -1.5, "TE")
diagram.annotate_interval(0, TR, -2.5, "TR")

# Show the diagram
diagram.show()
