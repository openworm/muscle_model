#!/usr/bin/python

# Data import, separated into its own module for reuse in other scripts.

from decimal import *

getcontext().prec = 28 # decimal precision

# Importing data
f = open('../../MatlabSupport/Main_Version/data/input.csv')
data = f.read().splitlines()

# Model parameters

Cmem = Decimal(data[0])
gKS = Decimal(data[1]) * Cmem
gKF = Decimal(data[2]) * Cmem
gCa = Decimal(data[3]) * Cmem
gL = Decimal(data[4]) * Cmem
VKS = Decimal(data[5])
VKF = Decimal(data[6])
VCa = Decimal(data[7])
VL = Decimal('10e-3') # Decimal(data[8]) # This is also commented out in all the original Matlab scripts
Vhalf_n = Decimal(data[9])
Vhalf_p = Decimal(data[10])
Vhalf_q = Decimal(data[11])
Vhalf_e = Decimal(data[12])
Vhalf_f = Decimal(data[13])
Cahalf_h = Decimal(data[14]) * Decimal('1e-9')
k_n = Decimal(data[15])
k_p = Decimal(data[16])
k_q = Decimal(data[17])
k_e = Decimal(data[18])
k_f = Decimal(data[19])
k_h = Decimal(data[20]) * Decimal('1e-9')
T_n = Decimal(data[21])
T_p = Decimal(data[22])
T_q = Decimal(data[23])
T_e = Decimal(data[24])
T_f = Decimal(data[25])
T_Ca = Decimal(data[26])
alphaCa = Decimal(data[27])
thiCa = Decimal('6.1e-6') / (T_Ca * gCa)

