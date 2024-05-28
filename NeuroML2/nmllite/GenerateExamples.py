from neuromllite import *
from neuromllite.NetworkGenerator import *
from neuromllite.utils import create_new_model
import sys

sys.path.append("..")


def generate(cell, duration=45, config='IClamp',parameters = None):
    
    reference = "%s_%s"%(config, cell)

    cell_id = '%sCell'%cell
    cell_nmll = Cell(id=cell_id, neuroml2_source_file='../%s.cell.nml'%(cell))
 
    ################################################################################
    ###   Add some inputs
    
    if 'IClamp' in config:
        
        if not parameters:
            parameters = {}
            parameters['stim_amp'] = '700pA'
            parameters['offset_stim_amp'] = '-120 pA'
        
        input_source0 = InputSource(id='iclamp_stim', 
                                   neuroml2_input='PulseGenerator', 
                                   parameters={'amplitude':'stim_amp', 'delay':'5ms', 'duration':'20ms'})

        input_source1 = InputSource(id='iclamp_offset', 
                                   neuroml2_input='PulseGenerator', 
                                   parameters={'amplitude':'offset_stim_amp', 'delay':'0ms', 'duration':'10000ms'})
      
        
    else:

        if not parameters:
            parameters = {}
            parameters['average_rate'] = '100 Hz'
            parameters['number_per_cell'] = '10'
            
        input_source0 = InputSource(id='pfs0', 
                                   neuroml2_input='PoissonFiringSynapse', 
                                   parameters={'average_rate':'average_rate', 
                                               'synapse':syn_exc.id, 
                                               'spike_target':"./%s"%syn_exc.id})
                                               
    sim, net = create_new_model(reference,
                     duration, 
                     dt=0.025, # ms 
                     temperature=34, # degC
                     default_region='Worm',
                     parameters = parameters,
                     cell_for_default_population=cell_nmll,
                     input_for_default_population=input_source0)
                
    net.input_sources.append(input_source1)
    net.inputs.append(Input(id='input_offset',
                            input_source=input_source1.id,
                            population=net.populations[0].id,
                            percentage=100))
    net.to_json_file()

    return sim, net



if __name__ == "__main__":
    
    sim, net = generate('SingleCompMuscle', 45, config="IClamp")

        
    check_to_generate_or_run(sys.argv, sim)
    
