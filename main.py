import matplotlib.pyplot
import mrsd
import math
import json

############### READ JSON File ##############
with open('parameters.json', 'r') as file:
    params = json.load(file)

############# Update the parameters with JSON data #######
TE = params.get('TE')
TR = params.get('TR')

# Create the underlying Matplotlib objects and the diagram
figure, plot = matplotlib.pyplot.subplots(tight_layout=True)
diagram = mrsd.Diagram(
    plot, ["RF", "$G_z$", "$G_y$", "$G_x$", "RO"])

################## Readout/Signal #################

Readout = params['Readout']
#print("Readout = " + str(Readout))


d_ramp = Readout.get('d_ramp')
d_readout = Readout.get('d_readout')
d_encoding = Readout.get('d_encoding')
area_factor = Readout.get('area_factor')
adc, echo, readout = diagram.readout(
    "RO", "$G_x$", d_readout, ramp = d_ramp, center=TE,
    adc_kwargs={"ec": "0.5"})
diagram.add("$G_x$", readout.adapt(d_encoding, -0.5, d_ramp, end=readout.begin))

################### RF ###########################

RF = params['RF']
length = len(RF)

i = 0
for length in RF:
    FA = RF[i].get('FA')
    Flip_A = math.radians(FA)
    Time = RF[i].get('Time_start')
    Sign = RF[i].get('Sign')
    Duration = RF[i].get('Duration')
    excitation, slice_selection = diagram.selective_pulse("RF", "$G_z$", duration=Duration, pulse_amplitude=Flip_A, ramp=d_ramp, center=Time)
    diagram.annotate("RF",excitation.center+0.5,2, r"$\alpha$ = " + str(Sign)+str(FA) )
    i = i + 1
diagram.add("$G_z$", slice_selection.adapt(d_encoding, area_factor, d_ramp, end=readout.begin))


################## Gradient ####################

Gradient = params['Gradient']
#print("Gradient = " + str(Gradient))

length = len(Gradient)
#print("Length G = " + str(length))

i = 0
for length in Gradient:
    Time = Gradient[i].get('Time_start')
    Amp = Gradient[i].get('Amp')
    Duration = Gradient[i].get('Duration')
    if (Gradient[i].get('Axis') == "y"):
        diagram.gradient("$G_y$", Duration, Amp, center=Time)
    elif (Gradient[i].get('Axis') == "x"):
        diagram.gradient("$G_x$", Duration, Amp, center=Time)
    elif (Gradient[i].get('Axis') == "z"):
        diagram.gradient("$G_z$", Duration, Amp, center=Time)
    i = i + 1  

################# Multi Gradient #############
Multi_gradient = params['Multi_gradient']
length = len(Multi_gradient)
i = 0
for length in Multi_gradient:
    Time = Multi_gradient[i].get('Time_start')
    Amp = Multi_gradient[i].get('Amp')
    Duration = Multi_gradient[i].get('Duration')
    if (Multi_gradient[i].get('Axis') == "y"):
        diagram.multi_gradient("$G_y$", d_encoding, 0.5, d_ramp, center = Time)
    elif (Multi_gradient[i].get('Axis') == "x"):
        diagram.multi_gradient("$G_x$", d_encoding, 0.5, d_ramp, center = Time)
    elif (Multi_gradient[i].get('Axis') == "z"):
        diagram.multi_gradient("$G_z$", d_encoding, 0.5, d_ramp, center = Time)
    i = i + 1  


#diagram.hard_pulse("$G_z$",1 ,1,center = 1)



################## Annotations ###############

# add flip angles and TE/TR intervals
diagram.interval(0, TE, -1.5, "TE")
diagram.interval(0, TR, -2.5, "TR")

################### PLOT ####################

matplotlib.pyplot.show()
