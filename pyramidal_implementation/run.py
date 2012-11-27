 #Idea here is that it will accept CLI arguments, analyse the result and print the fitness to a file for
#reading by the main evaluator

#e.g usage:
#  $ python run.py 16.130067085410197 0.0 237.5393647187672

import sys
import main
import numpy
import random
from optimalneuron import traceanalysis
import numpy

plot_sim = False

targets = {'peak_linear_gradient': 0.0126455, 'average_minimum': 32.9139683819512, 'spike_frequency_adaptation': 0.054102950823597951, 'trough_phase_adaptation': -0.032339835206814785, 'mean_spike_frequency': 170.75638755391191, 'average_maximum': 52.484330488178259, 'trough_decay_exponent': 0.082997586003614746, 'interspike_time_covar': 0.67343012507213718, 'min_peak_no': 27, 'spike_width_adaptation': 5.196371093168479e-17, 'max_peak_no': 28, 'first_spike_time': 105.37999999997665, 'peak_decay_exponent': -0.074000673186574759}

weights = {'peak_linear_gradient': 20,'average_minimum': 0.0, 'spike_frequency_adaptation': 0.0, 'trough_phase_adaptation': 0.0, 'mean_spike_frequency': 1.0, 'average_maximum': 2.0, 'trough_decay_exponent': 0.0, 'interspike_time_covar': 0.0, 'min_peak_no': 1.0, 'spike_width_adaptation': 0.0, 'max_peak_no': 50.0, 'first_spike_time': 1.0, 'peak_decay_exponent': 0.0}

params=sys.argv[1:]

if len(params)>1:
    print params[0]
    print params[1]
    print params[2]
    print params[3]

    simulation = main.muscle_simulation(k_fast_specific_gbar=params[0],
                                        k_slow_specific_gbar=params[1],
                                        ca_channel_specific_gbar=params[2],
					ca_h_A_F=params[3])
    
    

else:
    simulation = main.muscle_simulation()

simulation.run(1100)

if plot_sim:
	simulation.plot()


v = numpy.array(simulation.neuron_env.rec_v)
t = numpy.array(simulation.neuron_env.rec_t)

#now need to do some analysis

analysis_var={'peak_delta':0.0,'baseline':100,'dvdt_threshold':0.0,'peak_threshold':10}

analysis=traceanalysis.IClampAnalysis(v,t,analysis_var,
				      start_analysis=100,
				      end_analysis=1000,
				      smooth_data=False)

analysis.analyse()

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

try:
    print analysis.analysis_results
except:
    "results not vaiable"
