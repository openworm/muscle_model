#Idea here is that it will accept CLI arguments, analyse the result and print the fitness to a file for
#reading by the main evaluator

import sys
import main
import numpy
import random
import traceanalysis
import numpy

target_data_path = 
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

simulation.run(100)
simulation.plot()
voltage = numpy.array(simulation.neuron_env.rec_v)

#now need to do some analysis

#------------------------------------------
# STEP 1 - Obtain targets
#-------------------------------------------

t,v_raw=traceanalysis.load_csv_data(target_data_path)
v=numpy.array(v_raw)
v_smooth=list(traceanalysis.smooth(v))
analysis=traceanalysis.IClampAnalysis(
    v_smooth,t,analysis_var,start_analysis=analysis_start_time,
    end_analysis=analysis_end_time) 
analysis.analyse()
self.targets=analysis.analysis_results
print('Obtained targets are:')
print(self.targets)

#-------------------------------------
# STEP 2 - Get fitness
#-------------------------------------

analysis=traceanalysis.IClampAnalysis(exp_data.samples,
                                      exp_data.t,self.analysis_var,
                                      self.analysis_start_time,
                                      self.analysis_end_time,
                                      target_data_path=self.target_data_path)

print 'staritng analysis'

analysis.analyse()

print 'obtaining fitness'

fitness=analysis.evaluate_fitness(self.targets,
                                  self.weights,cost_function=
                                  traceanalysis.normalised_cost_function)

#--------------------------------------------------
# STEP 3 - write the fitness to the fitness file:
#--------------------------------------------------

evaluations_file = open('evaluations','a')
evaluations_file.write(fitness+'\n')
evaluations_file.close()
