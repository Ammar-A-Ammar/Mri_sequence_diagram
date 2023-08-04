import matplotlib.pyplot
import mrsd
import math
import json

############### READ JSON File ##############
with open('parameters.json', 'r') as file:
    params = json.load(file)

############# Update the parameters with JSON data #######
Profile_GRE = params['Profiles']['GRE']
Profile_SE = params['Profiles']['SE']
Profile_BSSFP = params['Profiles']['BSSFP']

# Create the underlying Matplotlib objects and the diagram
figure, plot = matplotlib.pyplot.subplots(tight_layout=True)
diagram = mrsd.Diagram(
    plot, ["RF", "$G_z$", "$G_y$", "$G_x$", "RO"])

############################### Time sorting ##########################
TimeBaseList=[("demo",0)]
#TimeBasedict={"id":"A1","Time":0}
""" TimeBasedict["id"] = id
    TimeBasedict["Time"] = Time """
def middle(n):  
    return n[1] 

data = params['GRE'][0]
RF = data['RF']
Gr = data['Gradient']
MGR = data['Multi_gradient']
for item in RF:
    id = item.get('id')
    Time = item.get('Time')
    TimeBaseList.append((id,Time))
for item in Gr:
    id = item.get('id')
    Time = item.get('Time')
    TimeBaseList.append((id,Time))
for item in MGR:
    id = item.get('id')
    Time = item.get('Time')
    TimeBaseList.append((id,Time))
    
TimeBaseList.sort(reverse=False,key=middle)
print(TimeBaseList)

with open('Time_file.txt', 'w') as f:
    f.writelines(str(TimeBaseList))


if (Profile_GRE == True):
    print("Profile GRE: " + str(Profile_GRE))
    data = params['GRE'][0]
    TE = data['TE']
    TR = data['TR']
    ################## Readout/Signal GRE #################

    Readout = data['Readout']
    #print("Readout = " + str(Readout))

    d_ramp = Readout.get('d_ramp')
    d_readout = Readout.get('d_readout')
    d_encoding = Readout.get('d_encoding')
    area_factor = Readout.get('area_factor')
    adc, echo, readout = diagram.readout(
        "RO", "$G_x$", d_readout, ramp = d_ramp, center=TE,
        adc_kwargs={"ec": "0.5"})
    diagram.add("$G_x$", readout.adapt(d_encoding, -0.5, d_ramp, end=readout.begin))

    ################### RF GRE ###########################

    RF = data['RF']
    length = len(RF)

    i = 0
    for length in RF:
        FA = RF[i].get('FA')
        Flip_A = math.radians(FA)
        Time = RF[i].get('Time')
        Sign = RF[i].get('Sign')
        Duration = RF[i].get('Duration')
        excitation, slice_selection = diagram.selective_pulse("RF", "$G_z$", duration=Duration, pulse_amplitude=Flip_A, ramp=d_ramp, center=Time)
        diagram.annotate("RF",excitation.center+0.5,2, r"$\alpha$ = " + str(Sign)+str(FA) )
        i = i + 1


    ################## Gradient GRE ####################

    Gradient = data['Gradient']
    #print("Gradient = " + str(Gradient))

    length = len(Gradient)
    #print("Length G = " + str(length))

    i = 0
    for length in Gradient:
        Time = Gradient[i].get('Time')
        Amp = Gradient[i].get('Amp')
        Duration = Gradient[i].get('Duration')
        if (Gradient[i].get('Axis') == "y"):
            diagram.gradient("$G_y$", Duration, Amp, center=Time)
        elif (Gradient[i].get('Axis') == "x"):
            diagram.gradient("$G_x$", Duration, Amp, center=Time)
        elif (Gradient[i].get('Axis') == "z"):
            diagram.gradient("$G_z$", Duration, Amp, center=Time)
        i = i + 1  

    ################# Multi Gradient GRE #############
    Multi_gradient = data['Multi_gradient']
    length = len(Multi_gradient)
    i = 0
    for length in Multi_gradient:
        Time = Multi_gradient[i].get('Time')
        Amp = Multi_gradient[i].get('Amp')
        Duration = Multi_gradient[i].get('Duration')
        if (Multi_gradient[i].get('Axis') == "y"):
            diagram.multi_gradient("$G_y$", d_encoding, 0.5, d_ramp, center = Time)
        elif (Multi_gradient[i].get('Axis') == "x"):
            diagram.multi_gradient("$G_x$", d_encoding, 0.5, d_ramp, center = Time)
        elif (Multi_gradient[i].get('Axis') == "z"):
            diagram.multi_gradient("$G_z$", d_encoding, 0.5, d_ramp, center = Time)
        i = i + 1  

elif (Profile_SE == True):
    ############################### Time sorting ##########################
    TimeBaseList=[("demo",0)]
    #TimeBasedict={"id":"A1","Time":0}
    """ TimeBasedict["id"] = id
        TimeBasedict["Time"] = Time """
    def middle(n):  
        return n[1] 

    data = params['SE'][0]
    RF = data['RF']
    Gr = data['Gradient']
    MGR = data['Multi_gradient']
    for item in RF:
        id = item.get('id')
        Time = item.get('Time')
        TimeBaseList.append((id,Time))
    for item in Gr:
        id = item.get('id')
        Time = item.get('Time')
        TimeBaseList.append((id,Time))
    for item in MGR:
        id = item.get('id')
        Time = item.get('Time')
        TimeBaseList.append((id,Time))
        
    TimeBaseList.sort(reverse=False,key=middle)
    print(TimeBaseList)

    with open('Time_file.txt', 'w') as f:
        f.writelines(str(TimeBaseList))



    
    ################## Readout/Signal SE #################
    TE = data['TE']
    TR = data['TR']
    Readout = data['Readout']
    d_ramp = Readout.get('d_ramp')
    d_readout = Readout.get('d_readout')
    d_encoding = Readout.get('d_encoding')
    area_factor = Readout.get('area_factor')
    adc, echo, readout = diagram.readout(
        "RO", "$G_x$", d_readout, ramp = d_ramp, center=TE,
        adc_kwargs={"ec": "0.5"})
    diagram.add("$G_x$", readout.adapt(d_encoding, -0.5, d_ramp, end=readout.begin))

    ################### RF SE ###########################
    for item in RF:
        FA = item.get('FA')
        Time = item.get('Time')
        Sign = item.get('Sign')
        Duration = item.get('Duration')
        Flip_A = math.radians(FA)
        excitation, slice_selection = diagram.selective_pulse("RF", "$G_z$", duration=Duration, pulse_amplitude=Flip_A, ramp=d_ramp, center=Time)
        diagram.annotate("RF",excitation.center+0.2,2, r"$\alpha$=" + str(Sign)+str(FA) )
        
        if(FA==90):
            Flip_A = math.radians(FA+90)
            excitation = diagram.rf_pulse("RF", Duration, Flip_A, center=TE/2)
            gradient = diagram.gradient("$G_z$", amplitude = 1, flat_top=0.8,ramp=d_ramp, center=TE/2)
            diagram.annotate("RF",excitation.center+0.3,2, r"$\alpha$= " + str(Sign)+str(FA+90) )
        else:
            Flip_A = math.radians(FA-90)
            excitation = diagram.rf_pulse("RF", Duration, Flip_A, center=TE/2)
            gradient = diagram.gradient("$G_z$", amplitude = 1, flat_top=0.8,ramp=d_ramp, center=TE/2)
            diagram.annotate("RF",excitation.center+0.3,2, r"$\alpha$= " + str(Sign)+str(FA-90) )
    
    diagram.interval(0, TE/2, -0.5, "TE/2")


    ################## Gradient SE ####################

    Gradient = data['Gradient']
    #print("Gradient = " + str(Gradient))

    length = len(Gradient)
    #print("Length G = " + str(length))

    i = 0
    for length in Gradient:
        Time = Gradient[i].get('Time')
        Amp = Gradient[i].get('Amp')
        Duration = Gradient[i].get('Duration')
        if (Gradient[i].get('Axis') == "y"):
            diagram.gradient("$G_y$", Duration, Amp, center=Time)
        elif (Gradient[i].get('Axis') == "x"):
            diagram.gradient("$G_x$", Duration, Amp, center=Time)
        elif (Gradient[i].get('Axis') == "z"):
            diagram.gradient("$G_z$", Duration, Amp, center=Time)
        i = i + 1  

    ################# Multi Gradient SE #############
    Multi_gradient = data['Multi_gradient']
    length = len(Multi_gradient)
    i = 0
    for length in Multi_gradient:
        Time = Multi_gradient[i].get('Time')
        Amp = Multi_gradient[i].get('Amp')
        Duration = Multi_gradient[i].get('Duration')
        if (Multi_gradient[i].get('Axis') == "y"):
            diagram.multi_gradient("$G_y$", d_encoding, 0.5, d_ramp, center = Time)
        elif (Multi_gradient[i].get('Axis') == "x"):
            diagram.multi_gradient("$G_x$", d_encoding, 0.5, d_ramp, center = Time)
        elif (Multi_gradient[i].get('Axis') == "z"):
            diagram.multi_gradient("$G_z$", d_encoding, 0.5, d_ramp, center = Time)
        i = i + 1 

elif (Profile_BSSFP == True):
    
    print("Profile BSSFP: " + str(Profile_BSSFP))
    data = params['BSSFP'][0]
    TE = data['TE']
    TR = data['TR']
    ################## Readout/Signal BSSFP #################

    Readout = data['Readout']
    #print("Readout = " + str(Readout))

    d_ramp = Readout.get('d_ramp')
    d_readout = Readout.get('d_readout')
    d_encoding = Readout.get('d_encoding')
    area_factor = Readout.get('area_factor')
    adc, echo, readout = diagram.readout(
        "RO", "$G_x$", d_readout, ramp = d_ramp, center=TE,
        adc_kwargs={"ec": "0.5"})
    diagram.add("$G_x$", readout.adapt(d_encoding, -0.5, d_ramp, end=readout.begin))
    diagram.add("$G_x$", readout.adapt(d_encoding, -0.5, d_ramp, center=TR-1))


    ################### RF BSSFP ###########################

    RF = data['RF']
    length = len(RF)

    i = 0
    for length in RF:
        FA = RF[i].get('FA')
        Time = RF[i].get('Time')
        Sign = RF[i].get('Sign')
        Duration = RF[i].get('Duration')
        Flip_A = math.radians(FA)
        excitation, slice_selection = diagram.selective_pulse("RF", "$G_z$", duration=Duration, pulse_amplitude=Flip_A, ramp=d_ramp, center=Time)
        diagram.annotate("RF",excitation.center+0.2,2, r"$\alpha$=" + str(Sign)+str(FA) )
        if (Sign=="+"): 
            excitation = diagram.rf_pulse("RF", Duration, Flip_A, center=TR+Duration)
            gradient = diagram.gradient("$G_z$", amplitude = -1, flat_top=0.8,ramp=d_ramp, center=TR-1)
            diagram.annotate("RF",excitation.center+0.2,2, r"$\alpha$=" + str("-")+str(FA) )
        else:
            excitation = diagram.rf_pulse("RF", Duration, Flip_A, center=TR+Duration)
            diagram.annotate("RF",excitation.center+0.2,2, r"$\alpha$=" + str("+")+str(FA) )
        i = i + 1

    ################## Gradient BSSFP ####################

    Gradient = data['Gradient']
    #print("Gradient = " + str(Gradient))

    length = len(Gradient)
    #print("Length G = " + str(length))

    i = 0
    for length in Gradient:
        Time = Gradient[i].get('Time')
        Amp = Gradient[i].get('Amp')
        Duration = Gradient[i].get('Duration')
        if (Gradient[i].get('Axis') == "y"):
            diagram.gradient("$G_y$", Duration, Amp, center=Time)
        elif (Gradient[i].get('Axis') == "x"):
            diagram.gradient("$G_x$", Duration, Amp, center=Time)
        elif (Gradient[i].get('Axis') == "z"):
            diagram.gradient("$G_z$", Duration, Amp, center=Time)
        i = i + 1  

    ################# Multi Gradient BSSFP #############
    Multi_gradient = data['Multi_gradient']
    length = len(Multi_gradient)
    i = 0
    for length in Multi_gradient:
        Time = Multi_gradient[i].get('Time')
        Amp = Multi_gradient[i].get('Amp')        
        multiGradient = diagram.multi_gradient("$G_y$", d_encoding, Amp, d_ramp, center = Time)
        diagram.annotate("$G_y$",multiGradient.center+0.5, 0, r"$\uparrow$" )
        multiGradient = diagram.multi_gradient("$G_y$", d_encoding, Amp, d_ramp, center = TR-1)
        diagram.annotate("$G_y$",multiGradient.center+0.5, 0, r"$\downarrow$" )
        i = i + 1  

################## Annotations ###############

# Add flip angles and TE/TR intervals
diagram.interval(0, TE, -1.5, "TE")

diagram.interval(0, TR, -2.5, "TR")

################### PLOT ####################

matplotlib.pyplot.show()
