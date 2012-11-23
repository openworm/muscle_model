from neuron import h
import pylab

def test_function():
    #to test interaction with c++
    return 0

def plot(vectors_dict):
    # plot the results
    pylab.subplot (2 ,1 ,1)
    pylab.plot (vectors_dict['t'], vectors_dict['v_pre'] ,
    vectors_dict['t'] , vectors_dict['v_post'])
    pylab.subplot (2 ,1 ,2)
    pylab.plot(vectors_dict['t'],vectors_dict['i_syn'])
    pylab.show()

class test_simulation():

    #simple simulation to test the principle
    
    def __init__(self,increment=0.1):
        #create pre- and post- synaptic sections

        self.increment = increment
        self.pre = h.Section()
        self.post = h.Section()

        for sec in self.pre,self.post:
            sec.insert('hh')
            
        #inject current in the pre-synaptic section

        self.stim = h.IClamp(0.5, sec=self.pre)
        self.stim.amp = 10.0
        self.stim.delay = 5.0
        self.stim.dur = 5.0

        #create a synapse in the pre-synaptic section
        self.syn = h.ExpSyn(0.5,sec=self.post)

        #connect the pre-synaptic section to the synapse object:

        self.nc = h.NetCon(self.pre(0.5)._ref_v,self.syn)
        self.nc.weight[0] = 2.0

        # record the membrane potentials and
        # synaptic currents
        vec = {}
        for var in 'v_pre', 'v_post', 'i_syn', 't':
            vec[var] = h.Vector()
        vec['v_pre'].record(self.pre(0.5)._ref_v )
        vec['v_post'].record(self.post(0.5)._ref_v )
        vec['i_syn'].record(self.syn._ref_i )
        vec['t'].record(h._ref_t)
       
        self.vector = vec

        #Initialize the simulation
        h.load_file ("stdrun.hoc")
        h.init()
        
    def run(self,do_plot = False):
    #run and return resting potential
        t_now = h.t
        while h.t < t_now + self.increment:
            h.fadvance()
        
        if do_plot:
            plot(self.vector)
        #return the post-synaptic membrane potential
        return self.vector['v_post'][-1]
            
#example use:
#a=test_simulation(increment=1)
#print a.run(do_plot=True)
#print a.run(do_plot=True)
