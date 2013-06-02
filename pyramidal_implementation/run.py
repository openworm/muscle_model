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
 #Idea here is that it will accept CLI arguments, analyse the result and print the fitness to a file for
#reading by the main evaluator

# example usage:
# python run.py eval_file0 40.041444758152295 0.0 4514.250191560498 35.2 0.4089 0.6 --compile --plotoverlay

import sys
import main
import numpy
import random
from optimalneuron import traceanalysis
import numpy

def overlay_result_with_data(data_file_name,t_sim,v_sim,
			     displacement=0.0,dt = 0.0002):

    from matplotlib import pyplot
    
    file=open(data_file_name)
    #make voltage into a numpy array in mV:
    v = numpy.array([float(i) for i in file.readlines()])*1000
    t_init = 0.0
    t_final = len(v)*dt
    t = numpy.linspace(t_init,t_final,len(v))*1000+displacement

    pyplot.title("Overlay of experimental recording and (W05042200_1_1_3_1) simulation with parameter set (chromosome) 40.041444758152295 0.0 4514.250191560498 35.2 0.3089 ")
    pyplot.xlabel('Time (ms)')
    pyplot.ylabel('Voltage (mV)')
    pyplot.plot(t,v)
    pyplot.plot(t_sim,v_sim)
    pyplot.show()

params=sys.argv[1:]

plot_sim = False
plot_overlay = False
nocompile = True
evaluations_file = "evals0"

if len(params)>1:
    evaluations_file=params[0]
    
    if '--plotsim' in params:
	plot_sim = True

    if '--plotoverlay' in params:
	plot_overlay = True

    if '--compile' in params:
	nocompile = False

    simulation = main.muscle_simulation(k_fast_specific_gbar=params[1],
                                        k_slow_specific_gbar=params[2],
                                        ca_channel_specific_gbar=params[3],
					ca_h_A_F=params[4],
                                        ca_tau_factor=params[5],
                                        k_tau_factor=params[6],
					nocompile=nocompile)

else:
    simulation = main.muscle_simulation() #run with defaults

simulation.run(1100)

if plot_sim:
	simulation.plot()

v = numpy.array(simulation.neuron_env.rec_v)
v = v+numpy.linspace(-6,4,len(v))
t = numpy.array(simulation.neuron_env.rec_t)

if plot_overlay:
    overlay_result_with_data("redacted_data.txt",t,v,
			     displacement=100.0)

#now need to do some analysis

targets = {'peak_linear_gradient': 0.0126455, 'average_minimum': 32.9139683819512, 'spike_frequency_adaptation': 0.054102950823597951, 'trough_phase_adaptation': -0.032339835206814785, 'mean_spike_frequency': 170.75638755391191, 'average_maximum': 52.484330488178259, 'trough_decay_exponent': 0.082997586003614746, 'interspike_time_covar': 0.67343012507213718, 'min_peak_no': 20, 'spike_width_adaptation': 5.196371093168479e-17, 'max_peak_no': 20, 'first_spike_time': 105.37999999997665, 'peak_decay_exponent': -0.074000673186574759}

weights = {'peak_linear_gradient': 20,'average_minimum': 5.0, 'spike_frequency_adaptation': 0.0, 'trough_phase_adaptation': 0.0, 'mean_spike_frequency': 1.0, 'average_maximum': 2.0, 'trough_decay_exponent': 0.0, 'interspike_time_covar': 0.0, 'min_peak_no': 1.0, 'spike_width_adaptation': 0.0, 'max_peak_no': 50.0, 'first_spike_time': 1.0, 'peak_decay_exponent': 0.0}

analysis_var={'peak_delta':0.0,'baseline':100,'dvdt_threshold':0.0,'peak_threshold':10}

analysis=traceanalysis.IClampAnalysis(v,t,analysis_var,
				      start_analysis=100,
				      end_analysis=1100,
				      smooth_data=False)

analysis.analyse()

fitness=analysis.evaluate_fitness(targets,
				  weights,
				  cost_function=
				  traceanalysis.normalised_cost_function)



# write the fitness to the fitness file:
print str(fitness)
evaluations_file = open(evaluations_file,'a')
evaluations_file.write(str(fitness)+'\n')
evaluations_file.close()

try:
    print analysis.analysis_results
except:
    "results not vaiable"
