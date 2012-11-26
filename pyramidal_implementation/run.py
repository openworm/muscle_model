#Idea here is that it will accept CLI arguments, analyse the result and print the fitness to a file for
#reading by the main evaluator

import sys
import main
import numpy
import random
from optimalneuron import traceanalysis
import numpy

targets = {'average_minimum': -0.13176587745945925, 'spike_frequency_adaptation': 0.0044486257825030575, 'trough_phase_adaptation': 0.0062869350891550874, 'mean_spike_frequency': 20.021290851441854, 'average_maximum': 17.254637946650821, 'trough_decay_exponent': 0.010134228692010657, 'interspike_time_covar': 0.05713062265256301, 'min_peak_no': 19, 'spike_width_adaptation': 5.6532961458987453e-18, 'max_peak_no': 20, 'first_spike_time': 20.604120000000002, 'peak_decay_exponent': 0.0031603942712837966}

weights = {'average_minimum': 1.0, 'spike_frequency_adaptation': 0.0, 'trough_phase_adaptation': 0.0, 'mean_spike_frequency': 1.0, 'average_maximum': 1.0, 'trough_decay_exponent': 0.0, 'interspike_time_covar': 0.0, 'min_peak_no': 1.0, 'spike_width_adaptation': 0.0, 'max_peak_no': 1.0, 'first_spike_time': 1.0, 'peak_decay_exponent': 0.0}

params=sys.argv[1:]

if len(params)>1:
    print params[0]
    print params[1]
    print params[2]
    simulation = main.muscle_simulation(k_fast_specific_gbar=params[0],
                                        k_slow_specific_gbar=params[1],
                                        ca_channel_specific_gbar=params[2])
else:
    simulation = main.muscle_simulation()

simulation.run(1000)
#simulation.plot()
v = numpy.array(simulation.neuron_env.rec_v)
t = numpy.array(simulation.neuron_env.rec_t)

#now need to do some analysis

analysis_var={'peak_delta':0.0,'baseline':5,'dvdt_threshold':0.0}

analysis=traceanalysis.IClampAnalysis(v,t,analysis_var,
				      start_analysis=0,
				      end_analysis=5000,
				      smooth_data=False)

analysis.analyse()

print analysis.analysis_results

fitness=analysis.evaluate_fitness(targets,
				  weights,
				  cost_function=
				  traceanalysis.normalised_cost_function)

#--------------------------------------------------
# write the fitness to the fitness file:
#--------------------------------------------------
print str(fitness)
evaluations_file = open('evaluations','a')
evaluations_file.write(str(fitness)+'\n')
evaluations_file.close()
