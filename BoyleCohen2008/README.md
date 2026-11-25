Muscle cell code from Boyle and Cohen 2008
------------------------------------------

This software was used in [Boyle and Cohen 2008](https://www.sciencedirect.com/science/article/pii/S0303264708001408?via%3Dihub), ([preprint](https://groups.google.com/group/openworm-discuss/attach/df619bba6defa84f/C.%20elegans%20Body%20Wall%20Muscles%20are%20Simple%20Actuators%20-%20Boyle,%20Cohen%20-%202007.pdf?part=0.2&authuser=0)):

_J.H. Boyle, N. Cohen, Caenorhabditis elegans body wall muscles are simple actuators, BioSystems 94 (2008) 170–181_

to both define and optimise the parameters of a muscle cell model for  _C. elegans_.

**If you use or alter this code please cite the above publication.**

This is being used by the OpenWorm project to create an [initial model of a muscle cell in NeuroML 2](https://github.com/openworm/muscle_model/tree/master/NeuroML2).

A key matlab script is located at [MatlabSupport/Main_Version/vclamp.m](MatlabSupport/Main_Version/vclamp.m) which, when run, should produce a main graph of the paper.

A Python version of this has been added at [PythonSupport/Main_Version/vclamp.py](PythonSupport/Main_Version/vclamp.py).  When run correctly it should produce the following image:

![vclamp.py running correctly](https://cloud.githubusercontent.com/assets/1037756/5603263/93dc8866-9331-11e4-8696-cc26a85b6208.png)

This reproduces figure 2B of the Boyle & Cohen paper.

This code is released under the terms of the MIT license.
