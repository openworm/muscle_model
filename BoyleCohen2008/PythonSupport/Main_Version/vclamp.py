#!/usr/bin/python

# Program for simulating full model with coupling

import sys
import numpy as np

nogui = '-nogui' in sys.argv
if not nogui:
    import matplotlib.pyplot as plt

sys.path += '.'
from x_inf import *
from input_vars import * # Global variables from input data file.

# Simulation Parameters
deltat = 0.01e-3
duration = 0.03                 #*********************      Duration    Duration   ***************
numpoints = int(round(duration/deltat))
numtests = 11
#xaxis = (deltat:deltat:duration) * 1e3
xaxis = [round(x * 1e3, 2) for x in np.arange(deltat, duration+deltat, deltat)]

# Input parameters
onset = int(round(0.002/deltat))
offset = int(round(0.022/deltat))

# Variable Declaration
V = list()
I_j = list()
I_mem = list()
Ca = list()
n = list()
p = list()
q = list()
e = list()
f = list()
h = list()

for i in range(0,numtests):
    V.append(list())
    I_mem.append(list())
    Ca.append(list())
    n.append(0)
    p.append(0)
    q.append(0)
    e.append(0)
    f.append(0)
    h.append(0)
    I_j.append(0)
    for j in range(0,numpoints):
        V[i].append(0)
        I_mem[i].append(0)
        Ca[i].append(0)
I_j.append(0)

# Input initialization
for i in range(0,numtests):
    for j in range(0,numpoints):
        V[i][j] = -70e-3

Vstim = 40e-3
for i in range(0,numtests):
    for j in range(onset-1,offset):
        V[i][j] = Vstim
    Vstim = Vstim - 10e-3

# Variable initialization
for j in range(0,numtests):
    Ca[j][0] = 0
    n[j] = x_inf(V[j][0], Vhalf_n, k_n)
    p[j] = x_inf(V[j][0], Vhalf_p, k_p)
    q[j] = x_inf(V[j][0], Vhalf_q, k_q)
    e[j] = x_inf(V[j][0], Vhalf_e, k_e)
    f[j] = x_inf(V[j][0], Vhalf_f, k_f)

# Start of simulation
for j in range(0,numtests):
    for i in range(1,numpoints):
        dn = (x_inf(V[j][i-1], Vhalf_n, k_n) - n[j])/T_n
        n[j] = n[j] + dn*deltat
        dp = (x_inf(V[j][i-1], Vhalf_p, k_p) - p[j])/T_p
        p[j] = p[j] + dp*deltat
        dq = (x_inf(V[j][i-1], Vhalf_q, k_q) - q[j])/T_q
        q[j] = q[j] + dq*deltat
        de = (x_inf(V[j][i-1], Vhalf_e, k_e) - e[j])/T_e
        e[j] = e[j] + de*deltat
        df = (x_inf(V[j][i-1], Vhalf_f, k_f) - f[j])/T_f
        f[j] = f[j] + df*deltat
        h[j] = x_inf(Ca[j][i-1], Cahalf_h, k_h)
        # H_rec[i] = h[j]
        IKS = gKS * n[j] * (V[j][i-1] - VKS)
        IKF = gKF * p[j]**4 * q[j] * (V[j][i-1] - VKF)
        ICa = gCa * e[j]**2 * f[j] * (1 + (h[j] - 1) * alphaCa) * (V[j][i-1] - VCa)
        IL = gL * (V[j][i-1] - VL)

        dCa = -(Ca[j][i-1]/T_Ca + thiCa*ICa)
        Ca[j][i] = Ca[j][i-1] + dCa*deltat

        I_mem[j][i] = (IKS + IKF + ICa)

    if not nogui: plt.plot(xaxis, [x * 1e9 for x in I_mem[j]])

print('Finished simulation of %s seconds'%duration)

if not nogui: 
    plt.ylabel('Imem (nA)')
    plt.xlabel('Time (ms)')
    plt.show()
