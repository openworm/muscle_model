A conversion of the NeuroML 2 muscle cell model to C by Robby Simpson

This code requires no external libraries and is intended to be useful to those wishing to understand how the muscle cell, as well as NeuroML 2 and LEMS, can be implemented in a simulator using Euler's method.

Reproduces Figure 2A in [Boyle & Cohen, 2008](http://www.sciencedirect.com/science/article/pii/S0303264708001408)

To compile:

    gcc testMuscleOpenworm.c -lm -o muscleC
    
Then the simulation can be run with:

    ./muscleC
    
To plot the results, pipe the output to a file and use your favourite plotting tool (or [neuroConstruct](https://github.com/NeuralEnsemble/neuroConstruct/blob/master/INSTALL)) to plot them:

    ./muscleC > results.dat
    ~/neuroConstruct/nCplot.sh -b results.dat
    
![plot](https://raw.githubusercontent.com/openworm/muscle_model/master/NeuroML2/C/Plot.png)
    
