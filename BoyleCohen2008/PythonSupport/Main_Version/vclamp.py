#!/usr/bin/python

# Program for simulating full model with coupling

import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path += '.'
from x_inf import *

# Importing data
f = open('data/input.csv')
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
VL = 10e-3; # float(data[8]);
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

    plt.plot(xaxis, [x * 1e9 for x in I_mem[j]])

plt.ylabel('Imem (nA)')
plt.xlabel('Time (ms)')
plt.show()
