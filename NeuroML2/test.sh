set -e

jnml -validate k*channel.nml Leak.channel.nml CaPool.nml *.cell.nml Figure2A.net.nml
jnml LEMS_Figure2A.xml -nogui
jnml LEMS_Figure2B.xml -nogui

./analyse_k_slow.sh -nogui
./analyse_k_fast.sh -nogui
./analyse_ca_boyle.sh -nogui