# Generalised function for getting x_inf from given parameters

from decimal import *

def x_inf(V,Vhalf,k):
    return 1/(1 + ((Vhalf - V)/k).exp())
