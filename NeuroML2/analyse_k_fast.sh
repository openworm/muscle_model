# Assumes https://github.com/OpenSourceBrain/BlueBrainProjectShowcase has been cloned in ~/git

set -e
python ~/git/BlueBrainProjectShowcase/Channelpedia/NML2ChannelAnalyse.py -temperature 34   -minV -55  -maxV 80  -duration 600  -clampBaseVoltage -55  -clampDuration 580  -stepTargetVoltage 10  -erev -55  k_fast.channel.nml k_fast
jnml LEMS_Test_k_fast.xml $1