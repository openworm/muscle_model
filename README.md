[![Build Status](https://travis-ci.org/openworm/muscle_model.png?branch=master)](https://travis-ci.org/openworm/muscle_model)

Open Worm muscle model
======================

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/openworm/muscle_model?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Authors: Mike Vella, Alex Dibert, Padraig Gleeson, Rayner Lucas
email:mv333@cam.ac.uk

If you contribute to the project please add your name to the Authors field

Introduction
------------

This repository contains the following:

1. Simulation of C.Elegans muscle cell electrical properties, based on Boyle & Cohen 2008.
2. Optimization script for the above model, utliising Optimal Neuron package. Optimizing towards sharp electrode data obtained from lab of Michael M Francis.
3. C++ Module for importation of arbitrary Pyramidal model into C++ program such as Palyanov et al SPH solver.
4. NeuroML 2/LEMS conversion of the muscle cell model


1. Simulation of C.Elegans muscle cell electrical properties
-----------------------------------------------------------
2. Optimization script for the above model
------------------------------------------

**Note: see https://github.com/openworm/muscle_model/issues/18 for details on the current status of these subprojects.**

See https://github.com/openworm/muscle_model/blob/master/pyramidal_implementation/README.md

3. C++ Module for SPH/muscle_model integration
----------------------------------------------

**Note: see https://github.com/openworm/muscle_model/issues/18 for details on the current status of these subprojects.**

This is still at an alpha stage, but has been demonstrated to function as expected.

to compile and run (temp notes with hardcoded paths - replace with your own path)
run the following commands from inside curdir:

$ export PYTHONPATH="/home/mike/dev/cpp_pyramidal_integration/"
OR
export PYTHONPATH=$PYTHONPATH:/home/mike/dev/muscle_model/pyramidal_implementation/
$ g++ main.cpp -l python2.7 -o sim -I /usr/include/python2.7/
$ ./sim

The resultant so file will then be importable in any c++ module and present a PyramidalSimulation class with a run() method which will return the membrane potential at the end of execution of a fixed timestep.

4. NeuroML 2/LEMS conversion of the muscle cell model
-----------------------------------------------------

This version of the muscle model reflects an initial attempt to convert the model from: http://www.sciencedirect.com/science/article/pii/S0303264708001408 into NeuroML 2 (http://www.neuroml.org/neuroml2.php).

We're in the process of updating this to match the version in: https://github.com/openworm/muscle_model/tree/master/neuron_implementation

See issue: https://github.com/openworm/OpenWorm/issues/169 for the latest.

See also http://www.opensourcebrain.org/projects/muscle_model/wiki.

[![Build Status](https://travis-ci.org/openworm/muscle_model.svg?branch=master)](https://travis-ci.org/openworm/muscle_model)
