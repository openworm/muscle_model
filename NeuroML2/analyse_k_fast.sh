
set -e
pynml-channelanalysis -temperature 34   -minV -55  -maxV 80  -duration 600  -clampBaseVoltage -55  -clampDuration 580  -stepTargetVoltage 10  -erev -55 -norun k_fast.channel.nml
pynml LEMS_Test_k_fast.xml $1
