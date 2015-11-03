'''

This script compares the data used in the Matlab version of the Boyle & Cohen 2008 model:
https://github.com/openworm/muscle_model/blob/master/BoyleCohen2008/MatlabSupport/Main_Version/data/input.csv#L20

with the values used in the NeuroML version, e.g.
https://github.com/openworm/muscle_model/blob/master/NeuroML2/SingleCompMuscle.cell.nml

'''

from input_vars import *

import neuroml.loaders as loaders
from math import pi


import urllib
import tempfile

link = "https://raw.githubusercontent.com/NeuroML/NeuroML2/master/NeuroML2CoreTypes/NeuroMLCoreDimensions.xml"
nml2_dims_contents = urllib.urlopen(link).read()
nml2_dims_file = tempfile.NamedTemporaryFile(delete=False)
nml2_dims_file.write(nml2_dims_contents)
nml2_dims_file.close()


from lems.model.model import Model
model = Model()
model.import_from_file(nml2_dims_file.name)

def get_si_value(nml2_value):
    return model.get_numeric_value(nml2_value, None)

def printout(name, bc2008, nml2):
    width = 36
    a = str(bc2008)
    b = str(nml2)
    line = "|  %s  |  %s  |  %s  |"%(name+' '*(width-len(name)), a+' '*(width-len(a)), b+' '*(width-len(b)))
    print(line)
    

dash = '------------------------------------'

print('')

cell_doc = loaders.NeuroMLLoader.load("../../../NeuroML2/SingleCompMuscle.cell.nml")
cell = cell_doc.cells[0]

d = cell.morphology.segments[0].distal
p = cell.morphology.segments[0].proximal

assert(d.diameter==p.diameter)
area_um2 = pi * (d.diameter) * ((d.x-p.x)**2 + (d.y-p.y)**2 + (d.z-p.z)**2)**0.5
area_m2 = get_si_value("%sum2"%area_um2)
cm_nml_str = cell.biophysical_properties.membrane_properties.specific_capacitances[0].value

print('Surface area of NeuroML2 cell: %s um2'%area_um2)
print('')
printout(dash, dash, dash)
printout("Parameter", "BoyleCohen2008", "NeuroML2")

membrane_properties = cell.biophysical_properties.membrane_properties
rev_pots = {}
densities = {}
for chan_dens in membrane_properties.channel_densities:
    rev_pots[chan_dens.id] = chan_dens.erev
    densities[chan_dens.id] = chan_dens.cond_density

def print_voltage(v_str):
    return "%s V (%s)"%(get_si_value(v_str),v_str)

def print_time(t_str):
    return "%s s (%s)"%(get_si_value(t_str),t_str)

printout(dash, dash, dash)
printout("Cmem (Total capacitance)", "%g F"%(Cmem), "%s F" % (get_si_value(cm_nml_str)*area_m2))
printout("  Spec cap", "%g F/m2"%(Cmem/area_m2), "%s F/m2" % (get_si_value(cm_nml_str)))

leak_dens_si  = get_si_value(densities['Leak_all'])

printout("gL (leak cond/cap)", "%s S/F"%(gL/Cmem), "%s S/F"%(leak_dens_si/get_si_value(cm_nml_str)))
printout("  gL total (leak)", "%s S"%(gL), "%s S"%(leak_dens_si*area_m2))
printout("  gL density (leak)", "%s S/m2"%(gL/area_m2), "%s S/m2 (%s)"%(leak_dens_si,densities['Leak_all']))

printout("  gKS density", "%s S/m2"%(gKS/area_m2), "%s S/m2 (%s)"%(get_si_value(densities['k_slow_all']),densities['k_slow_all']))
printout("  gKF density", "%s S/m2"%(gKF/area_m2), "%s S/m2 (%s)"%(get_si_value(densities['k_fast_all']),densities['k_fast_all']))
printout("  gCa density", "%s S/m2"%(gCa/area_m2), "%s S/m2 (%s)"%(get_si_value(densities['ca_boyle_all']),densities['ca_boyle_all']))

printout("VKS (rev pot slow K chans)",   "%s V"%VKS, print_voltage(rev_pots['k_slow_all']))
printout("VKF (rev pot fast K chans)",   "%s V"%VKF, print_voltage(rev_pots['k_fast_all']))
printout("VCa (rev pot Ca chans)",       "%s V"%VCa, print_voltage(rev_pots['ca_boyle_all']))
printout("VL (rev pot Leak)",            "%s V"%VL,  print_voltage(rev_pots['Leak_all']))


k_slow = loaders.NeuroMLLoader.load("../../../NeuroML2/k_slow.channel.nml").ion_channel[0]
k_fast = loaders.NeuroMLLoader.load("../../../NeuroML2/k_fast.channel.nml").ion_channel[0]
ca_boyle = loaders.NeuroMLLoader.load("../../../NeuroML2/ca_boyle.channel.nml").ion_channel[0]
ca_pool = loaders.NeuroMLLoader.load("../../../NeuroML2/CaPool.nml").fixed_factor_concentration_models[0]

nml2_v_half_n = k_slow.gate_hh_tau_infs[0].steady_state.midpoint
nml2_v_half_p = k_fast.gate_hh_tau_infs[0].steady_state.midpoint
nml2_v_half_q = k_fast.gate_hh_tau_infs[1].steady_state.midpoint
nml2_v_half_e = ca_boyle.gate_hh_tau_infs[0].steady_state.midpoint
nml2_v_half_f = ca_boyle.gate_hh_tau_infs[1].steady_state.midpoint


nml2_k_n = k_slow.gate_hh_tau_infs[0].steady_state.scale
nml2_k_p = k_fast.gate_hh_tau_infs[0].steady_state.scale
nml2_k_q = k_fast.gate_hh_tau_infs[1].steady_state.scale
nml2_k_e = ca_boyle.gate_hh_tau_infs[0].steady_state.scale
nml2_k_f = ca_boyle.gate_hh_tau_infs[1].steady_state.scale

nml2_T_n = k_slow.gate_hh_tau_infs[0].time_course.tau
nml2_T_p = k_fast.gate_hh_tau_infs[0].time_course.tau
nml2_T_q = k_fast.gate_hh_tau_infs[1].time_course.tau
nml2_T_e = ca_boyle.gate_hh_tau_infs[0].time_course.tau
nml2_T_f = ca_boyle.gate_hh_tau_infs[1].time_course.tau



printout("Vhalf_n", "%s V"%Vhalf_n,  "%s "%( print_voltage(nml2_v_half_n) ))
printout("Vhalf_p", "%s V"%Vhalf_p,  "%s "%( print_voltage(nml2_v_half_p) ))
printout("Vhalf_q", "%s V"%Vhalf_q,  "%s "%( print_voltage(nml2_v_half_q) ))
printout("Vhalf_e", "%s V"%Vhalf_e,  "%s "%( print_voltage(nml2_v_half_e) ))
printout("Vhalf_f", "%s V"%Vhalf_f,  "%s "%( print_voltage(nml2_v_half_f) ))

import xml.etree.ElementTree as ET
tree = ET.parse('../../../NeuroML2/ca_boyle.channel.nml')

#  There's probably a better way to do this...
for c in tree.getroot().iter():
    if 'gateHHtauInf' in c.tag and c.attrib.has_key('type') and c.attrib['type'] == "customHGate":
        nml2_cahalf_h = c.attrib['ca_half']
        nml2_k_h = c.attrib['k']
        nml2_alpha_ca  = c.attrib['alpha']
        


printout("Cahalf_h", "%s mM?"%Cahalf_h,  "%s mM"%(get_si_value(nml2_cahalf_h)))

printout("k_n", "%s V"%k_n,  "%s"%( print_voltage(nml2_k_n) ))
printout("k_p", "%s V"%k_p,  "%s"%( print_voltage(nml2_k_p) ))
printout("k_q", "%s V"%k_q,  "%s"%( print_voltage(nml2_k_q) ))
printout("k_e", "%s V"%k_e,  "%s"%( print_voltage(nml2_k_e) ))
printout("k_f", "%s V"%k_f,  "%s"%( print_voltage(nml2_k_f) ))

printout("k_h", "%s mM??"%k_h, "%s mM"%(get_si_value(nml2_k_h)))

printout("T_n", "%s s"%T_n,  "%s "%( print_time(nml2_T_n) ))
printout("T_p", "%s s"%T_p,  "%s "%( print_time(nml2_T_p) ))
printout("T_q", "%s s"%T_q,  "%s "%( print_time(nml2_T_q) ))
printout("T_e", "%s s"%T_e,  "%s "%( print_time(nml2_T_e) ))
printout("T_f", "%s s"%T_f,  "%s "%( print_time(nml2_T_f) ))

nml2_t_ca = ca_pool.decay_constant
nml2_rho = ca_pool.rho

nml2_thi_ca = get_si_value(nml2_rho) / area_m2 


printout("T_Ca", "%s s"%T_Ca,  "%s "%( print_time(nml2_t_ca) ))


printout("alphaCa", "%s (dimensionless)"%alphaCa,  "%s "%( nml2_alpha_ca ))
printout("thiCa", "%s mM s-1 A-1??"%thiCa,  "%s mM s-1 A-1??? "%( nml2_thi_ca ))


printout(dash, dash, dash)

print('')
