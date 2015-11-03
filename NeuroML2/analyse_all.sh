set -e

pynml-channelanalysis -temperature 34   -minV -100  -maxV 100  -duration 600  -clampBaseVoltage -55  -clampDuration 580  -stepTargetVoltage 10  -erev 50  -caConc 0.001 ca_boyle.channel.nml k_fast.channel.nml k_slow.channel.nml -html -md

