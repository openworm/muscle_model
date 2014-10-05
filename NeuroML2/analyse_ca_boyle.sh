# Assumes https://github.com/OpenSourceBrain/BlueBrainProjectShowcase has been cloned in ~/git

set -e
python ~/git/BlueBrainProjectShowcase/Channelpedia/NML2ChannelAnalyse.py -temperature 34   -minV -55  -maxV 80  -duration 600  -clampBaseVoltage -55  -clampDuration 580  -stepTargetVoltage 10  -erev 50  ca_boyle.channel.nml ca_boyle
jnml LEMS_Test_ca_boyle.xml