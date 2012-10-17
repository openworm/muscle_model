"""
C elegans muscle model
"""

import neuroml.morphology as ml
import neuroml.kinetics as kinetics
import pyramidal.environments as envs
from matplotlib import pyplot as plt
import numpy as np

#First build a compartment:
compartment = ml.Segment(length=500,proximal_diameter=500,distal_diameter=500)

#Create a PassiveProperties object:
passive = kinetics.PassiveProperties(init_vm=-40.0,
                                     rm=1/0.3,
                                     cm=1.0,
                                     ra=0.03)

#Create a LeakCurrent object:
leak = kinetics.LeakCurrent(em=-40.0)


#get a Morphology object from the compartment:
morphology = compartment.morphology

#insert the passive properties and leak current into the morphology:
morphology.passive_properties = passive
morphology.leak_current = leak

#create a current clamp stimulus:
stim = kinetics.IClamp(current=0.2,
                       delay=10.0,
                       duration=100.0)

#insert the stimulus into the morphology
morphology[0].insert(stim)

#create Ca ion channel:
ca_channel = kinetics.HHChannel(name = 'ca',
                                specific_gbar = 120.0,
                                ion = 'ca',
                                e_rev = 125.0,
                                x_power = 3.0,
                                y_power = 1.0)

#create K fast ion channel:
k_fast = kinetics.HHChannel(name = 'kfast',
                               specific_gbar = 36.0,
                               ion = 'k',
                               e_rev = -12.0,
                               x_power = 4.0,
                               y_power = 0.0)

k_slow = kinetics.HHChannel(name = 'kslow',
                               specific_gbar = 0.0,
                               ion = 'k',
                               e_rev = -12.0,
                               x_power = 4.0,
                               y_power = 0.0)


#create dicts containing gating parameters:
ca_m_params = {'A_A':0.1 * (25.0),
               'A_B': -0.1,
               'A_C': -1.0,
               'A_D': -25.0,
               'A_F':-10.0,
               'B_A': 4.0,
               'B_B': 0.0,
               'B_C': 0.0,
               'B_D': 0.0,
               'B_F': 18.0}

ca_h_params = {'A_A': 0.07, 
               'A_B': 0.0,  
               'A_C': 0.0,  
               'A_D': 0.0,  
               'A_F': 20.0, 
               'B_A': 1.0,  
               'B_B': 0.0,  
               'B_C': 1.0,  
               'B_D': -30.0,
               'B_F': -10.0}

k_fast_n_params = {'A_A': 0.01*(10.0),
              'A_B': -0.01,
              'A_C': -1.0,
              'A_D': -10.0,
              'A_F': -10.0,
              'B_A': 0.125,
              'B_B': 0.0,
              'B_C': 0.0,
              'B_D': 0.0,
              'B_F': 80.0}

k_fast_h_params = {'A_A': 6.6,
               'A_B': 0.0,
               'A_C': 1.0,
               'A_D': 15.6,
               'A_F': 10.0,
               'B_A': 6.6,
               'B_B': 0.0,
               'B_C': 1.0,
               'B_D': 15.6,
               'B_F': -10.0}

k_slow_n_params = {'A_A': 0.01*(10.0),
              'A_B': -0.01,
              'A_C': -1.0,
              'A_D': -10.0,
              'A_F': -10.0,
              'B_A': 0.125,
              'B_B': 0.0,
              'B_C': 0.0,
              'B_D': 0.0,
              'B_F': 80.0}

#setup the channel gating parameters:
ca_channel.setup_alpha(gate = 'X',
                       params = ca_m_params,
                       vdivs = 150,
                       vmin = -30,
                       vmax = 120)

ca_channel.setup_alpha(gate = 'Y',
                       params = ca_h_params,
                       vdivs = 150,
                       vmin = -30,
                       vmax = 120)

k_fast.setup_alpha(gate = 'X',
                      params = k_fast_n_params,
                      vdivs = 150,
                      vmin = -30,
                      vmax = 120)

k_fast.setup_alpha(gate = 'Y',
                       params = k_fast_h_params,
                       vdivs = 300,
                       vmin = -150,
                       vmax = 150)

k_slow.setup_alpha(gate = 'X',
                      params = k_slow_n_params,
                      vdivs = 150,
                      vmin = -30,
                      vmax = 120)

#insert the channels:
morphology[0].insert(ca_channel)
morphology[0].insert(k_fast)
morphology[0].insert(k_slow)

#create the MOOSE environmet:
moose_env = envs.MooseEnv(sim_time=100,dt=1e-2)

#import morphology into environment:
moose_env.import_cell(morphology)

#Run the MOOSE simulation:
moose_env.run_simulation()

#plot simulation results:
#moose_env.show_simulation()

#create the NEURON environment
neuron_env = envs.NeuronEnv(sim_time=100,dt=1e-2)

#now should be able to autogenerate these really:
#calcium_attributes = {'gbar':120e2}
#ca = kinetics.Nmodl('ca',calcium_attributes)
#potassium_attributes = {'gbar':36e2}
#kv = kinetics.Nmodl('kv',potassium_attributes)

#morphology[0].insert(ca)
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

moose_voltage = moose_env.rec_v
moose_time_vector  = np.linspace(0, moose_env.t_final, len(moose_env.rec_v))

#Plotting results:
moose_plot, = plt.plot(moose_time_vector,moose_voltage)
neuron_plot, = plt.plot(neuron_time_vector,neuron_voltage)
plt.xlabel("Time in ms")
plt.ylabel("Voltage in mV")
plt.title("Simplified C.Elegans Muscle electrophysilogy")
plt.legend([moose_plot,neuron_plot],["MOOSE VALIDATION","NEURON (MOD)"])
plt.show()

print neuron_env.topology
