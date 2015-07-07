C elegans muscle cell model in NeuroML 2
----------------------------------------

This is a NeuroML 2 implementation of the C elegans muscle cell model of [Boyle & Cohen, 2008](http://www.sciencedirect.com/science/article/pii/S0303264708001408).
    
To install & run this version, install either jNeuroML (for **jnml**, as outlined [here](https://github.com/NeuroML/jNeuroML/blob/master/README.md)), or PyNeuroML (for **pynml**, as outlined [here](https://github.com/NeuroML/pyNeuroML)).

Get a local copy of this repository with:

    git clone https://github.com/openworm/muscle_model.git

or

    git clone git@github.com:openworm/muscle_model.git  # if SSH authentication is set up locally

Go into the directory with the NeuroML 2 version of the model:

    cd muscle_model/NeuroML2

Run the example cell (trying to reproduce Figure 2A in [Boyle & Cohen, 2008](http://www.sciencedirect.com/science/article/pii/S0303264708001408)) with:

    jnml LEMS_Figure2A.xml  # using jNeuroML

or 

    pynml LEMS_Figure2A.xml  # using PyNeuroML

Run the example cell (trying to reproduce Figure 2B in [Boyle & Cohen, 2008](http://www.sciencedirect.com/science/article/pii/S0303264708001408)) with:

    jnml LEMS_Figure2B.xml
    pynml LEMS_Figure2B.xml
    
An iPython notebook with examples of how to explore elements of the muscle model is available at [Explore.ipynb](http://nbviewer.ipython.org/github/openworm/muscle_model/blob/master/NeuroML2/Explore.ipynb).
    
For more details on the current status of this conversion, see issue: https://github.com/openworm/OpenWorm/issues/169
