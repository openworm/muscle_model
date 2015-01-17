# Assumes https://github.com/OpenSourceBrain/BlueBrainProjectShowcase has been cloned in ~/git

set -e
OPENWORM_HOME=${OPENWORM_HOME:-~/git/}
python $OPENWORM_HOME/BlueBrainProjectShowcase/Channelpedia/NML2ChannelAnalyse.py -temperature 34   -minV -55  -maxV 80  -duration 600  -clampBaseVoltage -55  -clampDuration 580  -stepTargetVoltage 10  -erev 50  -caConc 0.001 ca_boyle.channel.nml ca_boyle
jnml LEMS_Test_ca_boyle.xml $1