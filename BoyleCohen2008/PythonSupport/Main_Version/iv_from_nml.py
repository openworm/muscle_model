#!/usr/bin/python

'''
This script generates I-V plots of the Fig.3 of the Boyle & Cohen 2008 paper from NeuroML2 files
'''

import neuroml.loaders as loaders
from math import pi
import urllib
import tempfile
from lems.model.model import Model
import xml.etree.ElementTree as ET

import sys
import numpy as np
import matplotlib.pyplot as plt
from math import exp

link = "https://raw.githubusercontent.com/NeuroML/NeuroML2/master/NeuroML2CoreTypes/NeuroMLCoreDimensions.xml"
nml2_dims_contents = urllib.urlopen(link).read()
nml2_dims_file = tempfile.NamedTemporaryFile(delete=False)
nml2_dims_file.write(nml2_dims_contents)
nml2_dims_file.close()

model = Model()
model.import_from_file(nml2_dims_file.name)

def get_si_value(nml2_value):
    return model.get_numeric_value(nml2_value, None)

cell_doc = loaders.NeuroMLLoader.load("../../../NeuroML2/SingleCompMuscle.cell.nml")
k_slow = loaders.NeuroMLLoader.load("../../../NeuroML2/k_slow.channel.nml").ion_channel[0]
k_fast = loaders.NeuroMLLoader.load("../../../NeuroML2/k_fast.channel.nml").ion_channel[0]
ca_boyle = loaders.NeuroMLLoader.load("../../../NeuroML2/ca_boyle.channel.nml").ion_channel[0]
ca_pool = loaders.NeuroMLLoader.load("../../../NeuroML2/CaPool.nml").fixed_factor_concentration_models[0]
tree = ET.parse('../../../NeuroML2/ca_boyle.channel.nml')

cell = cell_doc.cells[0]

d = cell.morphology.segments[0].distal
p = cell.morphology.segments[0].proximal
assert(d.diameter==p.diameter)
area_um2 = pi * (d.diameter) * ((d.x-p.x)**2 + (d.y-p.y)**2 + (d.z-p.z)**2)**0.5
area_m2 = get_si_value("%sum2"%area_um2)
cm_nml_str = cell.biophysical_properties.membrane_properties.specific_capacitances[0].value

membrane_properties = cell.biophysical_properties.membrane_properties
rev_pots = {}
densities = {}
for chan_dens in membrane_properties.channel_densities:
    rev_pots[chan_dens.id] = chan_dens.erev
    densities[chan_dens.id] = chan_dens.cond_density

nml2_Cmem = get_si_value(cm_nml_str) * area_m2
nml2_GKS = get_si_value(densities['k_slow_all']) * nml2_Cmem
nml2_GKF = get_si_value(densities['k_fast_all']) * nml2_Cmem
nml2_GCa = get_si_value(densities['ca_boyle_all']) * nml2_Cmem

nml2_VKS = get_si_value(rev_pots['k_slow_all'])
nml2_VKF = get_si_value(rev_pots['k_fast_all'])
nml2_VCa = get_si_value(rev_pots['ca_boyle_all'])

nml2_v_half_n = get_si_value(k_slow.gate_hh_tau_infs[0].steady_state.midpoint)
nml2_v_half_p = get_si_value(k_fast.gate_hh_tau_infs[0].steady_state.midpoint)
nml2_v_half_q = get_si_value(k_fast.gate_hh_tau_infs[1].steady_state.midpoint)
nml2_v_half_e = get_si_value(ca_boyle.gate_hh_tau_infs[0].steady_state.midpoint)
nml2_v_half_f = get_si_value(ca_boyle.gate_hh_tau_infs[1].steady_state.midpoint)

nml2_k_n = get_si_value(k_slow.gate_hh_tau_infs[0].steady_state.scale)
nml2_k_p = get_si_value(k_fast.gate_hh_tau_infs[0].steady_state.scale)
nml2_k_q = get_si_value(k_fast.gate_hh_tau_infs[1].steady_state.scale)
nml2_k_e = get_si_value(ca_boyle.gate_hh_tau_infs[0].steady_state.scale)
nml2_k_f = get_si_value(ca_boyle.gate_hh_tau_infs[1].steady_state.scale)

nml2_T_n = get_si_value(k_slow.gate_hh_tau_infs[0].time_course.tau)
nml2_T_p = get_si_value(k_fast.gate_hh_tau_infs[0].time_course.tau)
nml2_T_q = get_si_value(k_fast.gate_hh_tau_infs[1].time_course.tau)
nml2_T_e = get_si_value(ca_boyle.gate_hh_tau_infs[0].time_course.tau)
nml2_T_f = get_si_value(ca_boyle.gate_hh_tau_infs[1].time_course.tau)

for c in tree.getroot().iter():
    if 'customHGate' in c.tag:
        nml2_cahalf_h = get_si_value(c.attrib['ca_half'])
        nml2_k_h = get_si_value(c.attrib['k'])
        nml2_alpha_ca  = get_si_value(c.attrib['alpha'])

nml2_t_ca = get_si_value(ca_pool.decay_constant)
nml2_rho = get_si_value(ca_pool.rho)

def x_inf(V,Vhalf,k):
    return 1/(1 + exp((Vhalf - V)/k))

x = np.arange(-0.060, 0.080, 0.001)
numpoints = len(x)
y = np.zeros((2,numpoints))

for i in range(0,numpoints):
    IKS = nml2_GKS * x_inf(x[i], nml2_v_half_n, nml2_k_n) * (x[i] - nml2_VKS)
    IKF = nml2_GKF * x_inf(x[i], nml2_v_half_p, nml2_k_p)**4 * x_inf(x[i], nml2_v_half_q, nml2_k_q) * (x[i]- nml2_VKF)
    ICa = nml2_GCa * x_inf(x[i], nml2_v_half_e, nml2_k_e)**2 * (x[i] - nml2_VCa)

    y[0][i] = (IKF + IKS) / nml2_Cmem
    y[1][i] = ICa  / nml2_Cmem


plt.subplot(1,2,1)
plt.plot([round(i * 1e3, 2) for i in x], [round(j * 1e2, 2) for j in y[1]], 'k', label='$I_{Ca}$')
plt.xlim(-40,80)
plt.ylim(-8,6)
plt.ylabel('I_Ca (A/F)')
plt.xlabel('V (mV)')
plt.grid('on')

plt.subplot(1,2,2)
plt.plot([round(i * 1e3, 2) for i in x], [round(j * 1e2, 2) for j in y[0]], 'k', label='$I_{K}$')
plt.xlim(-70,50)
plt.ylim(-5,40)
plt.ylabel('I_K (A/F)')
plt.xlabel('V (mV)')
plt.grid('on')

plt.show()
