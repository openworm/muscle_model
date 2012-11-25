#Idea here is that it will accept CLI arguments, analyse the result and print the fitness to a file for
#reading by the main evaluator

import sys
import main
import numpy

def somefunction(voltage):
    return 0

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
voltage = numpy.array(simulation.neuron_env.rec_v)

#now write the fitness to the fitness file:
fitness = str(somefunction(voltage))
evaluations_file = open('evaluations','a')
evaluations_file.write(fitness+'\n')
evaluations_file.close()
