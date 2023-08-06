import matplotlib.pyplot
import mrsd
import math
import json

############### READ JSON File ##############
with open('Bssf_profile.json', 'r') as file:
    params = json.load(file)

############# Update the parameters with JSON data #######
""" Profile_GRE = params['Profiles']['GRE']
Profile_SE = params['Profiles']['SE']
Profile_BSSFP = params['Profiles']['BSSFP']
 """
# Create the underlying Matplotlib objects and the diagram
figure, plot = matplotlib.pyplot.subplots(tight_layout=True)
diagram = mrsd.Diagram(
    plot, ["RF", "$G_z$", "$G_y$", "$G_x$", "RO"])

############################### Time sorting ##########################


def middle(n):
    return n[1]


data = params
RF = params['RF']
Gr = data['Gradient']
MGR = data['Multi_gradient']
TE = data['TE']
TR = data['TR']

TimeBaseList = [("TE",-1 ,TE), ("TR",-2, TR)]

for item in RF:
    Time = item.get('Time')
    # FA_Sign = item.get("Sign")+item.get("FA")
    Duration = item.get('Duration')
    FA = item.get("FA")
    Sign = item.get("Sign")
    TimeBaseList.append(("RF", Time, Duration, FA, Sign))
for item in Gr:
    Time = item.get('Time')
    Duration = item.get('Duration')
    Amp = item.get("Amp")
    Axis = item.get('Axis')
    Sign = item.get("Sign")
    TimeBaseList.append(("Gr", Time, Duration, Amp, Axis, Sign))
for item in MGR:
    Time = item.get('Time')
    Amp = item.get("Amp")
    Axis = item.get('Axis')
    Sign = item.get("Sign")
    TimeBaseList.append(("MGR", Time, Amp, Axis, Sign))

TimeBaseList.sort(reverse=False,key=middle)
#print("TimeBaseList: ",TimeBaseList)

############################### delay function ##########################

delayList = []

for i, item in enumerate(TimeBaseList):
    if i < 3:
        continue
    if i < len(TimeBaseList)-1 and TimeBaseList[i][1] != TimeBaseList[i+1][1]:
        delayList.append(("delay", TimeBaseList[i+1][1]-TimeBaseList[i][1]))
    #print(i, item)
#print("delayList: ",delayList)

############################### delay appending ##########################
MergedList=[TimeBaseList[0:2]]
#print ("MergedList: ",MergedList )
z=0
for i, item in enumerate(TimeBaseList):
    if i < 2:
        continue
    comparableIndex=i < len(TimeBaseList)-1
    if i < len(TimeBaseList)-1 and z<len(delayList) and TimeBaseList[i+1][1]-TimeBaseList[i][1]==delayList[z][1]:
        #delayList.append(("delay", TimeBaseList[i+1][1]-TimeBaseList[i][1]))
        MergedList.extend([TimeBaseList[i],delayList[z]])
        z=z+1
    else:
        MergedList.append(TimeBaseList[i])

print("MergedList after:",MergedList )



############################### write file ##########################

with open('Time_file.txt', 'w') as f:
    f.writelines(str(TimeBaseList))

if (1 == True):
    ################## Readout/Signal #################
    """ d_ramp =  0.1
    d_readout = 2
    d_encoding = 1
    area_factor = -0.2 """
    Readout = data['Readout']
    d_ramp = Readout.get('d_ramp')
    d_readout = Readout.get('d_readout')
    d_encoding = Readout.get('d_encoding')
    area_factor = Readout.get('area_factor')
    # Duration=Readout.get("Duration")
    adc, echo, readout = diagram.readout(
        "RO", "$G_x$", d_readout, ramp=d_ramp, center=TE,
        adc_kwargs={"ec": "0.5"})
    diagram.add("$G_x$", readout.adapt(
        d_encoding, -0.5, d_ramp, end=readout.begin))

    ################### RF ###########################

    for item in RF:
        FA = item.get('FA')
        Flip_A = math.radians(FA)
        Time = item.get('Time')
        Sign = item.get('Sign')
        Duration = item.get('Duration')
        if Sign == "-":
            excitation, slice_selection = diagram.selective_pulse(
                "RF", "$G_z$", duration=Duration, gradient_amplitude=-1, pulse_amplitude=Flip_A, ramp=d_ramp, center=Time)
        elif Sign == "+":
            excitation, slice_selection = diagram.selective_pulse(
                "RF", "$G_z$", duration=Duration, gradient_amplitude=-1, pulse_amplitude=Flip_A, ramp=d_ramp, center=Time)
        diagram.annotate("RF", excitation.center+0.5, 2,
                         r"$\alpha$ = " + str(Sign)+str(FA))
    ################## Gradient ####################
    Gradient = Gr

    for item in Gradient:
        Time = item.get('Time')
        Amp = item.get('Amp')
        Duration = item.get('Duration')
        if (item.get('Axis') == "y"):
            diagram.gradient("$G_y$", Duration, Amp, center=Time)
        elif (item.get('Axis') == "x"):
            diagram.gradient("$G_x$", Duration, Amp, center=Time)
        elif (item.get('Axis') == "z"):
            diagram.gradient("$G_z$", Amp, 0.8, ramp=0.1, center=Time)

    ################# Multi Gradient #############
    Multi_gradient = MGR

    for item in Multi_gradient:
        Time = item.get('Time')
        Amp = item.get('Amp')
        Sign = item.get('Sign')
        if (item.get('Axis') == "y"):
            multiGradient = diagram.multi_gradient(
                "$G_y$", d_encoding, 0.5, d_ramp, center=Time)
            if Sign == "+":
                diagram.annotate(
                    "$G_y$", multiGradient.center+0.5, 0, r"$\uparrow$")
            elif Sign == "-":
                diagram.annotate(
                    "$G_y$", multiGradient.center+0.5, 0, r"$\downarrow$")
        elif (item.get('Axis') == "x"):
            multiGradient = diagram.multi_gradient(
                "$G_x$", d_encoding, 0.5, d_ramp, center=Time)
            if Sign == "+":
                diagram.annotate(
                    "$G_x$", multiGradient.center+0.5, 0, r"$\uparrow$")
            elif Sign == "-":
                diagram.annotate(
                    "$G_x$", multiGradient.center+0.5, 0, r"$\downarrow$")
        elif (item.get('Axis') == "z"):
            multiGradient = diagram.multi_gradient(
                "$G_z$", d_encoding, 0.5, d_ramp, center=Time)
            if Sign == "+":
                diagram.annotate(
                    "$G_z$", multiGradient.center+0.5, 0, r"$\uparrow$")
            elif Sign == "-":
                diagram.annotate(
                    "$G_z$", multiGradient.center+0.5, 0, r"$\downarrow$")


################## Annotations ###############

# Add flip angles and TE/TR intervals
diagram.interval(0, TE, -1.5, "TE")
diagram.interval(0, TR, -2.5, "TR")

################### PLOT ####################

matplotlib.pyplot.show()
