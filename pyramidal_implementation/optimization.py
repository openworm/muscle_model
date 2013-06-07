# The MIT License (MIT)
#
# Copyright (c) 2011, 2013 OpenWorm.
# http://openworm.org
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the MIT License
# which accompanies this distribution, and is available at
# http://opensource.org/licenses/MIT
#
# Contributors:
#      OpenWorm - http://openworm.org/people.html
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
# USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import with_statement
"""
Script to optimize C elegans cell current injection response (simplified version of current ramp)
-uses 25pA current injection instead of current ramp
"""

from optimalneuron import optimizers
from optimalneuron import evaluators
from optimalneuron import controllers

#first off we need to make an evaluator,

#parameters = ['axon_gbar_na','axon_gbar_kv','axon_gbar_kv3'] # these are unused, ignore them - they're all wrong

#manual_vals=[50,50,2000,70,70,5,0.1,28.0,49.0,-73.0,23.0] # Example of how to set a seed
min_constraints = [0.0,0.0,0,20.0, 0.0, 0.0]
#--nocompile = TRUE
max_constraints = [200000.0,0.0,700000.0,200.0, 1.0,1.0]
#--nocompile = FALSE
#max_constraints = [2000.0,0.0,7000.0,200.0, 1.0,1.0]

##the following block is uncommented because we're using dumb evalutation
#analysis_var={'peak_delta':0,'baseline':0,'dvdt_threshold':2}
#
#weights={'average_minimum': 5, 'spike_frequency_adaptation': 0, 'trough_phase_adaptation': 0, 'mean_spike_frequency': 0, 'average_maximum': 0, 'trough_decay_exponent': 5, 'interspike_time_covar': 0, 'min_peak_no': 1, 'spike_width_adaptation': 0, 'max_peak_no': 5, 'first_spike_time': 0, 'peak_decay_exponent': 0,'spike_broadening':5,'pprd_error':5}
#targets={'average_minimum': -38.839498793604541, 'spike_frequency_adaptation': 0.019619800882894008, 'trough_phase_adaptation': 0.005225712358530369, 'mean_spike_requency': 47.353760445682454, 'average_maximum': 29.320249266525668, 'trough_decay_exponent': 0.11282542321257279, 'interspike_time_covar': 0.042610190921388166, 'min_peak_no': 34, 'spike_broadening': 0.81838856772318913, 'spike_width_adaptation': 0.0095057081186080035, 'max_peak_no': 35, 'first_spike_time': 164.0, 'peak_decay_exponent': -0.04596529555434687,'pptd_error':0}

#using automatic target evaluation:
#what we should do next is separate out the controller and pass it as an object to the evaluator-
#we really need to think about this deeply, separating the nrnproject logic from the neuronoptimizer
#may be quite hard

my_controller=controllers.CLIController('python run.py')
fitness_filename = 'evaluations'

my_evaluator=evaluators.DumbEvaluator(my_controller,fitness_filename,threads_number=128)

my_optimizer=optimizers.CustomOptimizerA(max_constraints,min_constraints,my_evaluator,
                                  population_size=1280,
                                  max_evaluations=6400,
                                  num_selected=1000,
                                  num_offspring=2,
                                  num_elites=1,
                                  seeds=None)
my_optimizer.optimize()
