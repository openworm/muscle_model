"""
Simulation of C.Elegans muscle cell electrical
properties based on Boyle and Cohen 2008.

This model includes the following currents:
    - k_fast
    - k_slow
    - Ca
    - leak

Author:Mike Vella
email:mv333@cam.ac.uk
"""
import neuroml.morphology as ml
import neuroml.kinetics as kinetics
import pyramidal.environments as envs
from matplotlib import pyplot as plt
import numpy as np

#First build a compartment: - Question - what are some more sensible dimensions to be using?
compartment = ml.Segment(length=500,proximal_diameter=500,distal_diameter=500)

#Create a PassiveProperties object:
passive = kinetics.PassiveProperties(init_vm=-58.0,
                                     rm=1/0.3,
                                     cm=30e-12,
                                     ra=0.03
                                     )

#Create a LeakCurrent object:
leak = kinetics.LeakCurrent(em=-20e-3)


#get a Morphology object from the compartment:
morphology = compartment.morphology

#insert the passive properties and leak current into the morphology:
morphology.passive_properties = passive
morphology.leak_current = leak

#create a current clamp stimulus - we need to find one which is the same as the current
#which was injected during our experimental data recording
stim = kinetics.IClamp(current=0.0,
                       delay=1,
                       duration=3)

#insert the stimulus into the morphology
morphology[0].insert(stim)

#calcium:
ca_attributes = {'gCaL':10.0}
ca = kinetics.Nmodl('ICaL',ca_attributes)
morphology[0].insert(ca)


#calcium pump:
ca_pump_attributes = {} # {'gbar':100}
ca_pump = kinetics.Nmodl('ca_pump',ca_pump_attributes)
morphology[0].insert(ca_pump)

#calcium pump:
#cad_attributes = {} # {'gbar':100}
#cad = kinetics.Nmodl('cad',cad_attributes)
#morphology[0].insert(cad)

#create k_fast ion channel:
k_fast = kinetics.HHChannel(name = 'k_fast',
                                specific_gbar = 100.0,
                                ion = 'k',
                                e_rev = -55.0,
                                x_power = 4.0,
                                y_power = 1.0)

#create k_slow ion channel:
k_slow = kinetics.HHChannel(name = 'k_slow',
                               specific_gbar = 0.0,
                               ion = 'k',
                               e_rev = -64.3,
                               x_power = 1.0,
                               y_power = 0.0)

#create ca ion channel:
#ca = kinetics.HHChannel(name = 'ca',
#                               specific_gbar = 220.0,
#                               ion = 'ca',
#                               e_rev = 49.1,
#                               x_power = 2.0,
#                               y_power = 1.0)
#
#create dicts containing gating parameters:
k_fast_m_params = {'A_A': 434.8,
               'A_B': 0.0,
               'A_C': 0.0,
               'A_D': 8.1,
               'A_F': -7.4,
               'B_A': 434.8,
               'B_B': 0.0,
               'B_C': 0.0,
               'B_D': 55.0,
               'B_F': 10000.0}
coeff = 1
k_fast_h_params = {'A_A': 0.13 * coeff,
               'A_B': 0.0,
               'A_C': 0.0,
               'A_D': 15.6,
               'A_F': 10.0,
               'B_A': 0.13 * coeff,
               'B_B': 0.0,
               'B_C': 0.0,
               'B_D': 55.0,
               'B_F': 10000.0}

k_slow_m_params = {'A_A': 40.0,
                   'A_B': 0.0,
                   'A_C': 0.0,
                   'A_D': -19.9,
                   'A_F': -15.9,
                   'B_A': 40.0,
                   'B_B': 0.0,
                   'B_C': 0.0,
                   'B_D': 64.3,
                   'B_F': 10000.0}

#k_slow_h_params = {'A_A': 0.0, # Not used.
#            'A_B': 0.0,
#            'A_C': 0.0,
#            'A_D': 0.0,
#            'A_F': 0.0,
#            'B_A': 0.0,
#            'B_B': 0.0,
#            'B_C': 0.0,
#            'B_D': 0.0,
#            'B_F': 0.0}'''

#ca_m_params = {'A_A': 10000.0,
#               'A_B': 0.0,
#               'A_C': 0.0,
#               'A_D': 3.4,
#               'A_F': -6.7,
#               'B_A': 10000.0,
#               'B_B': 0.0,
#               'B_C': 0.0,
#               'B_D': -49.1,
#               'B_F': 10000.0}
#
#ca_h_params = {'A_A': 6.66,
#               'A_B': 0.0,
#               'A_C': 0.0,
#               'A_D': -25.2,
#               'A_F': -5.0,
#               'B_A': 6.66,
#               'B_B': 0.0,
#               'B_C': 0.0,
#               'B_D': -49.1,
#               'B_F': 10000.0}

#setup the channel gating parameters:
k_fast.setup_alpha(gate = 'X',
                       params = k_fast_m_params,
                       vdivs = 300,
                       vmin = -150,
                       vmax = 150)

k_fast.setup_alpha(gate = 'Y',
                       params = k_fast_h_params,
                       vdivs = 300,
                       vmin = -150,
                       vmax = 150)

k_slow.setup_alpha(gate = 'X',
                       params = k_slow_m_params,
                       vdivs = 300,
                       vmin = -150,
                       vmax = 150)

#'''k_slow.setup_alpha(gate = 'Y',
#                       params = k_slow_h_params,
#                       vdivs = 1500,
#                       vmin = -300,
#                       vmax = 1200)'''
#
#ca.setup_alpha(gate = 'X',
#                       params = ca_m_params,
#                       vdivs = 300,
#                       vmin = -150,
#                       vmax = 150)
#
#ca.setup_alpha(gate = 'Y',
#                       params = ca_h_params,
#                       vdivs = 300,
#                       vmin = -150,
#                       vmax = 150)
#
#insert the channels:
morphology[0].insert(k_fast)
morphology[0].insert(k_slow)
#morphology[0].insert(ca)

#create the MOOSE environmet:
#moose_env = envs.MooseEnv(sim_time=5,dt=1e-4)

#import morphology into environment:
#moose_env.import_cell(morphology)

#Run the MOOSE simulation:
#moose_env.run_simulation()

#plot simulation results:
#moose_env.show_simulation()

#create the NEURON environment
neuron_env = envs.NeuronEnv(sim_time=5,dt=1e-4)

#now should be able to autogenerate these really:
#sodium_attributes = {'gbar':120e2}
#na = kinetics.Nmodl('na',sodium_attributes)
#potassium_attributes = {'gbar':36e2}
#kv = kinetics.Nmodl('kv',potassium_attributes)

#morphology[0].insert(na)
#morphology[0].insert(kv)

#import morphology into environment:
neuron_env.import_cell(morphology)

#run the NEURON simulation
print 'About to run simulation'
neuron_env.run_simulation()

#plot simulation results:
#neuron_env.show_simulation()

neuron_voltage = neuron_env.rec_v
neuron_time_vector  = neuron_env.rec_t

#moose_voltage = moose_env.rec_v
#moose_time_vector  = np.linspace(0, moose_env.t_final, len(moose_env.rec_v))

#Plotting results:
#moose_plot, = plt.plot(moose_time_vector,moose_voltage)
neuron_plot, = plt.plot(neuron_time_vector,neuron_voltage)
plt.xlabel("Time in ms")
plt.ylabel("Voltage in mV")
#plt.legend([moose_plot,neuron_plot],["MOOSE","NEURON"])
plt.show()

print neuron_env.topology
