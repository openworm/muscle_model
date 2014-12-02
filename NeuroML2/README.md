C elegans muscle cell model in NeuroML 2
----------------------------------------

This is a NeuroML 2 implementation of the C elegans muscle cell model of [Boyle & Cohen, 2008](http://www.sciencedirect.com/science/article/pii/S0303264708001408).
    
To install & run this version, install jNeuroML (as outlined here: https://github.com/NeuroML/jNeuroML/blob/master/README.md)

Get a local copy of the repository with:

    git clone https://github.com/openworm/muscle_model.git

or

    git clone git@github.com:openworm/muscle_model.git

Go into the directory with the NeuroML 2 version of the model:

    cd muscle_model/NeuroML2

Run the example cell (trying to reproduce Figure 2A in [Boyle & Cohen, 2008](http://www.sciencedirect.com/science/article/pii/S0303264708001408)) with:

    jnml LEMS_Figure2A.xml

Run the example cell (trying to reproduce Figure 2B in [Boyle & Cohen, 2008](http://www.sciencedirect.com/science/article/pii/S0303264708001408)) with:

    jnml LEMS_Figure2B.xml
    
For more details on the current status of this conversion, see issue: https://github.com/openworm/OpenWorm/issues/169
