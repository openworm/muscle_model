"""
Simulation of C.Elegans muscle cell with three currents
and one calcium pump.

This is still at a very early stage, being optimized on
CamGrid using neuronoptimizer. The model represented
here requires the publically-unavailable nrntools
module from the nrndev library. Please email
author for these libraries.

Author:Mike Vella
email:mv333@cam.ac.uk
"""

from neuron import h
from nrndev import nrntools


muscle=h.Section()
muscle_part_2=h.Section()

muscle.connect(muscle_part_2)

muscle.insert('na')
muscle_part_2.insert('na')
muscle.insert('kv')
muscle.insert('canrgc')
muscle.insert('cad2')

sim=nrntools.Simulation(muscle,sim_time=2200,v_init=-70.0)
sim.set_IClamp(100, 0.2, 2000)
sim.go()

sim.show()
