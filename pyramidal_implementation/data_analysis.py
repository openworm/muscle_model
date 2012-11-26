import numpy as np
from matplotlib import pyplot
from optimalneuron import traceanalysis

data_fname = "redacted_data.txt"
dt = 0.0002

#load the voltage:
file=open(data_fname)

#make voltage into a numpy array in mV:
v = np.array([float(i) for i in file.readlines()])*1000

t_init = 0.0
t_final = len(v)*dt

t = np.linspace(t_init,t_final,len(v))*1000

pyplot.plot(t,v)
pyplot.show()

analysis_var={'peak_delta':0.0,'baseline':5,'dvdt_threshold':0.0}

analysis=traceanalysis.IClampAnalysis(v,t,analysis_var,start_analysis=150,end_analysis=900)

analysis.analyse()
print analysis.analysis_results
