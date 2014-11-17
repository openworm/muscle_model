# Generalised function for getting x_inf from given parameters

from math import exp

def x_inf(V,Vhalf,k):
    return 1/(1 + exp((Vhalf - V)/k))
