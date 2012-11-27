"""
Script to optimize C elegans cell current injection response (simplified version of current ramp)
"""

from optimalneuron import optimizers
from optimalneuron import evaluators
from optimalneuron import controllers

#first off we need to make an evaluator,

parameters = ['axon_gbar_na','axon_gbar_kv','axon_gbar_kv3'] # these are unused, ignore them - they're all wrong

#manual_vals=[50,50,2000,70,70,5,0.1,28.0,49.0,-73.0,23.0] # Example of how to set a seed
min_constraints = [0.0,0.0,0,20.0, 0.0]
max_constraints = [2000.0,0.0,7000.0,200.0, 1.0]

##the following block is uncommented because we're using dumb evalutation
#analysis_var={'peak_delta':0,'baseline':0,'dvdt_threshold':2}
#
#weights={'average_minimum': 5, 'spike_frequency_adaptation': 0, 'trough_phase_adaptation': 0, 'mean_spike_frequency': 0, 'average_maximum': 0, 'trough_decay_exponent': 5, 'interspike_time_covar': 0, 'min_peak_no': 1, 'spike_width_adaptation': 0, 'max_peak_no': 5, 'first_spike_time': 0, 'peak_decay_exponent': 0,'spike_broadening':5,'pprd_error':5}
#targets={'average_minimum': -38.839498793604541, 'spike_frequency_adaptation': 0.019619800882894008, 'trough_phase_adaptation': 0.005225712358530369, 'mean_spike_frequency': 47.353760445682454, 'average_maximum': 29.320249266525668, 'trough_decay_exponent': 0.11282542321257279, 'interspike_time_covar': 0.042610190921388166, 'min_peak_no': 34, 'spike_broadening': 0.81838856772318913, 'spike_width_adaptation': 0.0095057081186080035, 'max_peak_no': 35, 'first_spike_time': 164.0, 'peak_decay_exponent': -0.04596529555434687,'pptd_error':0}

#using automatic target evaluation:
#what we should do next is separate out the controller and pass it as an object to the evaluator-
#we really need to think about this deeply, separating the nrnproject logic from the neuronoptimizer
#may be quite hard

my_controller=controllers.CLIController('ipython run.py')
fitness_filename = 'evaluations'

my_evaluator=evaluators.DumbEvaluator(my_controller,fitness_filename)

my_optimizer=optimizers.CustomOptimizerA(max_constraints,min_constraints,my_evaluator,
                                  population_size=500,
                                  max_evaluations=2000,
                                  num_selected=10,
                                  num_offspring=10,
                                  num_elites=1,
                                  seeds=None)
my_optimizer.optimize()
