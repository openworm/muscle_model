
## WARNING


This implementation is not compatible with the current
version of libNeuroML, it is currently being rewritten
by Mike Vella.

See also https://github.com/openworm/muscle_model/issues/18



## Compilation of C++ interface


Compile the PyramidalSimulation object:

    g++ -c PyramidalSimulation.cpp -I /usr/include/python2.7/ -I ./ -l python2.7 -o PyramidalSimulation.o
    
Invoke the linker:

    g++ example.cpp PyramidalSimulation.o -I /usr/include/python2.7/ -I ./ -l python2.7 -o simulation


## Experimental data info


Denis Turutin described the simulations he sent us as follows:

1. For spontaneous 50s, It is spontaneous evoked (current clamp) with holding current 0 pA.

2. For CCramp it is, 0 pA for 100ms, -20 pA 5ms, from -20pA to 40 pA linear within 2 s, finally 0 pA for 100ms 

We are using the CCramp data (2) (RATIONALE - it is very difficult to interpret the data obtained under the effect of synaptic input, the current injectino should negate synaptic current influx). 

The experimental data recorded in W05042200_1_1_3_1.txt will be used as a target.

Some Calculations - If Denis' protocol description is correct, total time of execution is 0.1+0.05+2+0.1 = 2.205s. There are 11025 data points in the recording, giving a sampling frequency of 5KHz.

Observations:

1. (initial) Resting potential 30mV

Note: the initial hyperpolarizing step can be used to elicit information about the passive properties of the cell.


## Simulation info


Initial simulation:

The initial simulation will be of reduced complexity:

Take the component of the ramp from 10pA to 40pA and approximate to 25pA. As the current ramp is linear, 10pA should occur at (100+5+1000)ms = 1105, i.e data point 1.105*5000=5525.To data point 2.105*1000=10525

This is saved as redacted_data.txt


Information previously contained in top level README.md
=======================================================

The relevant model is contained in the /pyramidal_implementation folder

This model includes the following currents:
    - k_fast
    - k_slow
    - Ca
    - leak

### Running model


To run model install pyramidal and its dependencies as described here: 
http://pyramidal.readthedocs.org/en/latest/install.html

The relevant model is contained in the /pyramidal_implementation folder, cd to that folder and:

Then execute the command:

     python run.py eval_file0 40.041444758152295 0.0 4514.250191560498 35.2 0.4089 0.6 --compile --plotoverlay

This will use the auto-mod file compilation feature of Pyramidal including nrnivmodl compilation and run the model with the best-optimized parameters to-date.

### Running optimization

To run model install Optimal Neuron and its dependencies as described here: 
http://optimal-neuron.readthedocs.org/en/latest/installation.html

Remove any mod files (such as ca.mod) from the pyramidal_implementation repository as this will interfere with the optimizer behaviour, the optimizer is designed to run with the manual_*.mod files which are located in the /mod_file directory and need to be the only mod files present in the /pyramidal directory before execution of the optimization script.

The current optimization is set up to use features extracted from the data file, the feature values are:

'peak_linear_gradient': 0.0126455, 'average_minimum': 32.9139683819512, 'spike_frequency_adaptation': 0.054102950823597951, 'trough_phase_adaptation': -0.032339835206814785, 'mean_spike_frequency': 170.75638755391191, 'average_maximum': 52.484330488178259, 'trough_decay_exponent': 0.082997586003614746, 'interspike_time_covar': 0.67343012507213718, 'min_peak_no': 20, 'spike_width_adaptation': 5.196371093168479e-17, 'max_peak_no': 20, 'first_spike_time': 105.37999999997665, 'peak_decay_exponent': -0.074000673186574759

and corresponding weights:

'peak_linear_gradient': 20,'average_minimum': 5.0, 'spike_frequency_adaptation': 0.0, 'trough_phase_adaptation': 0.0, 'mean_spike_frequency': 1.0, 'average_maximum': 2.0, 'trough_decay_exponent': 0.0, 'interspike_time_covar': 0.0, 'min_peak_no': 1.0, 'spike_width_adaptation': 0.0, 'max_peak_no': 50.0, 'first_spike_time': 1.0, 'peak_decay_exponent': 0.0

Then run:

     >>>python optimization.py

The optimizer will execute on 64 threads and display the results. Play with optimization.py to change #threads, #population #max_evaluations etc.
