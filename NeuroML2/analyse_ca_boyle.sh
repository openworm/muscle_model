
set -e
pynml-channelanalysis -temperature 34   -minV -55  -maxV 80  -duration 600  -clampBaseVoltage -55  -clampDuration 580  -stepTargetVoltage 10  -erev 50  -caConc 0.001 -norun ca_boyle.channel.nml
pynml LEMS_Test_ca_boyle.xml $1
