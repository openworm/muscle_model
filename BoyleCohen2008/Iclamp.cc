#include "Iclamp.hh"
#include <iostream>
using namespace std;

simulationdata Iclamp(simulationdata simdata){
	// First initialize V and gating variables to steady state values
	simdata.V[0] = -0.075;
	simdata.Ca[0] = 0;
	for(int i = NN; i <= FF; ++i){
		simdata.gatevars[i] = 1/(1+exp((simdata.vhalf_x[i] - simdata.V[0])/simdata.k_x[i]));
	}
	simdata.gatevars[HH] = 1/(1+exp((simdata.vhalf_x[HH] - simdata.Ca[0])/simdata.k_x[HH]));
	
	// Now do main loop
	for(int i = 1; i < simdata.numpoints; ++i){
		double k1[7], k2[7], k3[7], k4[7];
		double h_2 = simdata.deltat/2;
		double tempgate[6];
		double tempCa, tempV;
		
		//step 1 - get k1 values
		for(int j = NN; j <= FF; ++j){
			k1[j] = dx(simdata.gatevars[j], simdata.V[i-1], simdata.T_x[j], simdata.vhalf_x[j], simdata.k_x[j]);
		}
		tempgate[HH] = 1/(1+exp((simdata.vhalf_x[HH] - simdata.Ca[i-1])/simdata.k_x[HH]));
		k1[HH] = dCa(simdata.gxs, simdata.gatevars, simdata.vrevs, simdata.alphaCa, simdata.V[i-1], simdata.TCa, simdata.thiCa, simdata.Ca[i-1]);
		k1[HH+1] = dV(simdata.gxs, simdata.gatevars, simdata.vrevs, simdata.alphaCa, simdata.I[i], simdata.Cm, simdata.V[i-1]);	

		//step 2  - get k2 values
		tempV = simdata.V[i-1] + k1[HH+1]*h_2;
		tempCa = simdata.Ca[i-1] + k1[HH]*h_2;
		for(int j = NN; j <= FF; ++j){
			tempgate[j] =  (simdata.gatevars[j] + k1[j]*h_2);
			k2[j] = dx(tempgate[j], tempV, simdata.T_x[j], simdata.vhalf_x[j], simdata.k_x[j]);
		}
		tempgate[HH] = 1/(1+exp((simdata.vhalf_x[HH] - tempCa)/simdata.k_x[HH]));
		k2[HH] = dCa(simdata.gxs, tempgate, simdata.vrevs, simdata.alphaCa, tempV, simdata.TCa, simdata.thiCa, tempCa);
		k2[HH+1] = dV(simdata.gxs, tempgate, simdata.vrevs, simdata.alphaCa, simdata.I[i], simdata.Cm, tempV);	
		
		//step 3  - get k3 values
		tempV = simdata.V[i-1] + k2[HH+1]*h_2;
		tempCa = simdata.Ca[i-1] + k2[HH]*h_2;
		for(int j = NN; j <= FF; ++j){
			tempgate[j] =  (simdata.gatevars[j] + k2[j]*h_2);
			k3[j] = dx(tempgate[j], tempV, simdata.T_x[j], simdata.vhalf_x[j], simdata.k_x[j]);
		}
		tempgate[HH] = 1/(1+exp((simdata.vhalf_x[HH] - tempCa)/simdata.k_x[HH]));
		k3[HH] = dCa(simdata.gxs, tempgate, simdata.vrevs, simdata.alphaCa, tempV, simdata.TCa, simdata.thiCa, tempCa);
		k3[HH+1] = dV(simdata.gxs, tempgate, simdata.vrevs, simdata.alphaCa, simdata.I[i], simdata.Cm, tempV);	
	
		//step 4  - get k4 values
		tempV = simdata.V[i-1] + k3[HH+1]*h_2*2;
		tempCa = simdata.Ca[i-1] + k3[HH]*h_2*2;
		for(int j = NN; j <= FF; ++j){
			tempgate[j] =  (simdata.gatevars[j] + k3[j]*h_2*2);
			k4[j] = dx(tempgate[j], tempV, simdata.T_x[j], simdata.vhalf_x[j], simdata.k_x[j]);
		}
		tempgate[HH] = 1/(1+exp((simdata.vhalf_x[HH] - tempCa)/simdata.k_x[HH]));
		k4[HH] = dCa(simdata.gxs, tempgate, simdata.vrevs, simdata.alphaCa, tempV, simdata.TCa, simdata.thiCa, tempCa);
		k4[HH+1] = dV(simdata.gxs, tempgate, simdata.vrevs, simdata.alphaCa, simdata.I[i], simdata.Cm, tempV);	
	
		// now we must combine them to get final value
		for(int j = NN; j <= FF; ++j){
			simdata.gatevars[j] += (simdata.deltat/6)*(k1[j] + 2*k2[j] + 2*k3[j] + k4[j]);
		}
		simdata.Ca[i] = simdata.Ca[i-1] + (simdata.deltat/6)*(k1[HH] + 2*k2[HH] + 2*k3[HH] + k4[HH]);
		simdata.gatevars[HH] = 1/(1+exp((simdata.vhalf_x[HH] - tempCa)/simdata.k_x[HH]));
		simdata.V[i] = simdata.V[i-1] + (simdata.deltat/6)*(k1[HH+1] + 2*k2[HH+1] + 2*k3[HH+1] + k4[HH+1]);
	}
	return simdata;
}
