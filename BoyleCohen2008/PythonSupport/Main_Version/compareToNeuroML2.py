from input_vars import *

import neuroml.loaders as loaders
from neuroml import Cell
from math import pi


def printout(name, bc2008, nml2):
    width = 25
    a = str(bc2008)
    b = str(nml2)
    line = "|  %s  |  %s  |  %s  |"%(name+' '*(width-len(name)), a+' '*(width-len(a)), b+' '*(width-len(b)))
    print(line)
    

printout("Parameter", "BoyleCohen2008", "NeuroML2")

cell_doc = loaders.NeuroMLLoader.load("../../../NeuroML2/SingleCompMuscle.cell.nml")
cell = cell_doc.cells[0]
d = cell.morphology.segments[0].distal
p = cell.morphology.segments[0].proximal
assert(d.diameter==p.diameter)
area_um2 = pi * (d.diameter) * ((d.x-p.x)**2 + (d.y-p.y)**2 + (d.z-p.z)**2)**0.5
cm_nml = cell.biophysical_properties.membrane_properties.specific_capacitances[0].value


printout("Spec cap", "%g ??"%(Cmem/area_um2), cm_nml)


