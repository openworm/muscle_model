#!/usr/bin/python

# Data import, separated into its own module for reuse in other scripts.

# Importing data
f = open('../../MatlabSupport/Main_Version/data/input.csv')
data = f.read().splitlines()

# Model parameters

Cmem = float(data[0])
gKS = float(data[1]) * Cmem
gKF = float(data[2]) * Cmem
gCa = float(data[3]) * Cmem
gL = float(data[4]) * Cmem
VKS = float(data[5])
VKF = float(data[6])
VCa = float(data[7])
VL = 10e-3; # float(data[8]); # This is also commented out in all the original Matlab scripts
Vhalf_n = float(data[9])
Vhalf_p = float(data[10])
Vhalf_q = float(data[11])
Vhalf_e = float(data[12])
Vhalf_f = float(data[13])
Cahalf_h = float(data[14]) * 1e-9
k_n = float(data[15])
k_p = float(data[16])
k_q = float(data[17])
k_e = float(data[18])
k_f = float(data[19])
k_h = float(data[20]) * 1e-9
T_n = float(data[21])
T_p = float(data[22])
T_q = float(data[23])
T_e = float(data[24])
T_f = float(data[25])
T_Ca = float(data[26])
alphaCa = float(data[27])
thiCa = 6.1e-6 / (T_Ca * gCa)

