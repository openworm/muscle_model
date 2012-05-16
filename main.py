"""
Simulation of C.Elegans muscle cell with three currents
and one calcium pump.

This is still at a very early stage, being optimized on
CamGrid using neuronoptimizer. The model represented
here requires the publically-unavailable nrntools
module from the nrndev library. Please email
author (vellamike@gmail.com) for these libraries.

Author:Mike Vella
email:mv333@cam.ac.uk
"""

from neuron import h
import neuron
import numpy as np
from matplotlib import pyplot as plt
#from nrndev import nrntools


muscle=h.Section()
muscle_part_2=h.Section()

muscle.connect(muscle_part_2)

muscle.insert('na')
muscle_part_2.insert('na')
muscle.insert('kv')
muscle.insert('canrgc')
muscle.insert('cad2')

stim=h.IClamp(muscle(0.5))
stim.delay=100
stim.amp=0.2
stim.dur=200

#set the recroding section:
rec_t=h.Vector()
rec_t.record(h._ref_t)
rec_v=h.Vector()
rec_v.record(muscle(0.5)._ref_v)


h.dt=0.05
h.finitialize(-70.0)
neuron.init()
sim_time=2000

if sim_time:
    neuron.run(sim_time)
else:
    neuron.run(sim_time)


x=np.array(rec_t)
y=np.array(rec_v)
plt.plot(x,y)
plt.show()

##if using nrntools, much of the above can be accomplished as follows:
#sim=nrntools.Simulation(muscle,sim_time=2200,v_init=-70.0)
#sim.set_IClamp(100, 0.2, 2000)
#sim.go()
#sim.show()
