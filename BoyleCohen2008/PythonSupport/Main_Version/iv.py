#!/usr/bin/python

# Plotting I-V curves

import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path += '.'
from x_inf import *
from input_vars import *

x = np.arange(-0.060, 0.080, 0.001)
numpoints = len(x)
y = np.zeros((2,numpoints))

for i in range(0,numpoints):
    IKS = gKS * x_inf(x[i], Vhalf_n, k_n) * (x[i] - VKS)
    IKF = gKF * x_inf(x[i], Vhalf_p, k_p)**4 * x_inf(x[i], Vhalf_q, k_q) * (x[i]- VKF)
    ICa = gCa * x_inf(x[i], Vhalf_e, k_e)**2 * (x[i] - VCa)

    y[0][i] = (IKF + IKS) / Cmem
    y[1][i] = ICa  / Cmem


plt.subplot(1,2,1)
plt.plot([round(i * 1e3, 2) for i in x], y[1], 'k', label='$I_{Ca}$')
plt.xlim(-40,80)
plt.ylim(-8,6)
plt.ylabel('I_Ca (A/F)')
plt.xlabel('V (mV)')
plt.grid('on')

plt.subplot(1,2,2)
plt.plot([round(i * 1e3, 2) for i in x], y[0], 'k', label='$I_{K}$')
plt.xlim(-70,50)
plt.ylim(-5,40)
plt.ylabel('I_K (A/F)')
plt.xlabel('V (mV)')
plt.grid('on')

plt.show()
