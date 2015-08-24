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


'''
**Note: this is an early attempt to convert the muscle model to NEURON**


**It does not match the [MATLAB](https://github.com/openworm/muscle_model/tree/master/BoyleCohen2008/MatlabSupport/Main_Version), 
[Python](https://github.com/openworm/muscle_model/tree/master/BoyleCohen2008/PythonSupport/Main_Version) or 
[NeuroML](https://github.com/openworm/muscle_model/tree/master/NeuroML2) versions of the model!**
'''

from __future__ import with_statement
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

WARNING: Not under development as of 29/8/12. Development focus has shifted
to the pyramidal implementation.
"""

from neuron import h
import neuron
import numpy as np
from matplotlib import pyplot as plt
#from nrndev import nrntools

def set_section_mechanism(sec, mech, mech_attribute, mech_value): #Is this passing by reference, do you need to state that explicitly in Python?
    for seg in sec:
        setattr(getattr(seg, mech), mech_attribute, mech_value)

# Create muscle cell body
muscle=h.Section()

# XXX Placeholder values - check dimensions
# Using dimensions from ../NeuroML2/SingleCompMuscle.cell.nml
# Dimensions are in um
muscle.diam = 5
muscle.L = 20

muscle.insert('na')
muscle.insert('kv')
muscle.insert('canrgc')
muscle.insert('cad2')

# set conductance density
set_section_mechanism(muscle,'canrgc','gbar',0.1)
set_section_mechanism(muscle,'kv','gbar',20)
set_section_mechanism(muscle,'na','gbar',100)


# Loop to connect muscle arms
num_arms = 5 # Number of arms per cell
num_compartments = 10 # Number of compartments per arm
arms = []
for i in range(num_arms):
    arms.append([])
    arm_compartment = None
    prev_compartment = muscle

    # Connect 10 compartments per arm
    for j in range(num_compartments):
        arm_compartment = h.Section()

        # Set dimensions
        arm_compartment.diam = 0.75
        arm_compartment.L = 1

        arm_compartment.cm = 1   # uF/cm2
        arm_compartment.Ra = 100 # Ohm-cm

        # Set currents
        arm_compartment.insert('pas')
        set_section_mechanism(arm_compartment, 'pas', 'g', 0.000022222)

        arm_compartment.connect(prev_compartment)
        arms[i].append(arm_compartment)
        prev_compartment = arm_compartment

    # Set up stimulus at end of each muscle arm
    stim=h.IClamp(arms[i][num_compartments-1](0.5))
    stim.delay=100
    stim.amp=0.02
    stim.dur=200


# Set the recording section - middle of muscle cell:
rec_t=h.Vector()
rec_t.record(h._ref_t)
rec_v=h.Vector()
#rec_v.record(arms[0][9](0.5)._ref_v)
rec_v.record(muscle(0.5)._ref_v)

rec_ina = h.Vector()
rec_ina.record(muscle(0.5)._ref_ina)

rec_ik = h.Vector()
rec_ik.record(muscle(0.5)._ref_ik)

rec_ica = h.Vector()
rec_ica.record(muscle(0.5)._ref_ica)

h.dt=0.05
h.finitialize(-70.0)
neuron.init()
sim_time=500

if sim_time:
    neuron.run(sim_time)
else:
    neuron.run(sim_time)


x=np.array(rec_t)
y=np.array(rec_v)
plt.figure(1)
plt.subplot(411)
plt.plot(x,y)

na=np.array(rec_ina)
plt.subplot(412)
plt.plot(x,na)

k=np.array(rec_ik)
plt.subplot(413)
plt.plot(x,k)

ca=np.array(rec_ica)
plt.subplot(414)
plt.plot(x,ca)

plt.show()

##if using nrntools, much of the above can be accomplished as follows:
#sim=nrntools.Simulation(muscle,sim_time=2200,v_init=-70.0)
#sim.set_IClamp(100, 0.2, 2000)
#sim.go()
#sim.show()
