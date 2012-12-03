"""
C elegans muscle model
"""

import neuroml.morphology as ml
import neuroml.kinetics as kinetics
import pyramidal.environments as envs
from matplotlib import pyplot as plt
import numpy as np

class muscle_simulation():
    def __init__(self,
                 k_fast_specific_gbar = 36.0,
                 k_slow_specific_gbar = 0.0,
                 ca_channel_specific_gbar = 120,
		 ca_h_A_F = 20,
                 k_tau_factor = 1.0,
                 ca_tau_factor = 1.0):

#	print 'tau factor is:'
#	print tau_factor
	k_tau_factor = float(k_tau_factor)
      	ca_tau_factor = float(ca_tau_factor)
        self.k_fast_specific_gbar = float(k_fast_specific_gbar)
        self.k_slow_specific_gbar = float(k_slow_specific_gbar)
        self.ca_channel_specific_gbar = float(ca_channel_specific_gbar)
        
        #First build a compartment, I infered these dimensions from the hyperpolarizing pulses
        self.compartment = ml.Segment(length=800,
                                      proximal_diameter=800,
                                      distal_diameter=800)

        #Create a PassiveProperties object:
        self.passive = kinetics.PassiveProperties(init_vm=-30.0,
                                             rm=1/0.3,
                                             cm=10.0, #1.0
                                             ra=0.03)

        #Create a LeakCurrent object:
        self.leak = kinetics.LeakCurrent(em=-30.0)


        #get a Morphology object from the compartment:
        self.morphology = self.compartment.morphology

        #insert the passive properties and leak current into the morphology:
        self.morphology.passive_properties = self.passive
        self.morphology.leak_current = self.leak

        #create two current clamp stimuli:
        self.stim = kinetics.IClamp(current=0.25,
                               delay=100.0,
                               duration=1000.0)

        #problem with Pyramidal here, inserting this overrides the previous?!
        #create a current clamp stimulus:
#        self.stim2 = kinetics.IClamp(current=0.10,
#                               delay=600.0,
#                               duration=500.0)

        
        #insert the stimulus into the morphology
        self.morphology[0].insert(self.stim)
        
        #create Ca ion channel:
        ca_channel = kinetics.HHChannel(name = 'ca',
                                        specific_gbar = self.ca_channel_specific_gbar,
                                        ion = 'ca',
                                        e_rev = 20.0,
                                        x_power = 3.0,
                                        y_power = 1.0)

        #create K fast ion channel:
        k_fast = kinetics.HHChannel(name = 'kfast',
                                       specific_gbar = self.k_fast_specific_gbar,
                                       ion = 'k',
                                       e_rev = -10.0,
                                       x_power = 4.0,
                                       y_power = 0.0)

        k_slow = kinetics.HHChannel(name = 'kslow',
                                       specific_gbar = self.k_slow_specific_gbar,
                                       ion = 'k',
                                       e_rev = -10.0,
                                       x_power = 4.0,
                                       y_power = 0.0)


        #create dicts containing gating parameters:
        ca_m_params = {'A_A':0.1 *25.0*ca_tau_factor, 
                       'A_B': -0.1*ca_tau_factor,
                       'A_C': -1.0,
                       'A_D': -25.0,
                       'A_F':-10.0,
                       'B_A': 4.0*ca_tau_factor,
                       'B_B': 0.0*ca_tau_factor,
                       'B_C': 0.0,
                       'B_D': 0.0,
                       'B_F': 18.0}

        ca_h_params = {'A_A': 0.07*ca_tau_factor,
                       'A_B': 0.0*ca_tau_factor,  
                       'A_C': 0.0,  
                       'A_D': 0.0,  
                       'A_F': ca_h_A_F, #20
                       'B_A': 1.0*ca_tau_factor,  
                       'B_B': 0.0*ca_tau_factor,  
                       'B_C': 1.0,  
                       'B_D': -30.0,
                       'B_F': -10.0}

        k_fast_n_params = {'A_A': 0.01*(10.0)*k_tau_factor,
                      'A_B': -0.01*k_tau_factor, #0.01
                      'A_C': -1.0,
                      'A_D': -10.0,
                      'A_F': -10.0,
                      'B_A': 0.125*k_tau_factor,
                      'B_B': 0.0*k_tau_factor,
                      'B_C': 0.0,
                      'B_D': 0.0,
                      'B_F': 80.0}

        k_fast_h_params = {'A_A': 6.6*k_tau_factor,
                       'A_B': 0.0*k_tau_factor,
                       'A_C': 1.0,
                       'A_D': 15.6,
                       'A_F': 10.0,
                       'B_A': 6.6*k_tau_factor,
                       'B_B': 0.0*k_tau_factor,
                       'B_C': 1.0,
                       'B_D': 15.6,
                       'B_F': -10.0}

        k_slow_n_params = {'A_A': 0.01*(10.0),
                      'A_B': -0.01,
                      'A_C': -2.0,
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
        self.morphology[0].insert(ca_channel)
        self.morphology[0].insert(k_fast)
        self.morphology[0].insert(k_slow)

        #create the NEURON environment
        self.neuron_env = envs.NeuronEnv(sim_time=100,dt=1e-2)

        #import morphology into environment:
        self.neuron_env.import_cell(self.morphology)

    def run(self,time_increment=5):
        self.neuron_env.advance_simulation(time_increment)
        return self.neuron_env.rec_v[-1]


    def plot(self):
        #plot simulation results:
        #neuron_env.show_simulation()

        neuron_voltage = self.neuron_env.rec_v
        neuron_time_vector  = self.neuron_env.rec_t

        #Plotting results:
        neuron_plot, = plt.plot(neuron_time_vector,neuron_voltage)
        plt.xlabel("Time in ms")
        plt.ylabel("Voltage in mV")
        plt.title("Simplified C.Elegans Muscle electrophysilogy")
        plt.show()

    def topology(self):
        print self.neuron_env.topology
        
#example usage:        
#testsim=muscle_simulation()
#for i in range(0,100):
#    print testsim.run(3)
