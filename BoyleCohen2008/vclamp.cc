#include "vclamp.hh"
#include <iostream>
using namespace std;

simulationdata vclamp(simulationdata simdata){
	// First initailaise gating variables to steady state values
	simdata.Ca[0] = 0;
	for(int i = NN; i <= FF; ++i){
		simdata.gatevars[i] = 1/(1+exp((simdata.vhalf_x[i] - simdata.V[0])/simdata.k_x[i]));
	}
	simdata.gatevars[HH] = 1/(1+exp((simdata.vhalf_x[HH] - simdata.Ca[0])/simdata.k_x[HH]));
	simdata.I[0] = simdata.gxs[IKs]*simdata.gatevars[NN]*(simdata.V[0] - simdata.vrevs[IKs]) + simdata.gxs[IKf]*pow(simdata.gatevars[PP],4)*simdata.gatevars[QQ]*(simdata.V[0] - simdata.vrevs[IKf]) + simdata.gxs[ICa]*pow(simdata.gatevars[EE],2)*simdata.gatevars[FF]*(1 + (simdata.gatevars[HH] - 1)*simdata.alphaCa)*(simdata.V[0]-simdata.vrevs[ICa]) + simdata.gxs[Il]*(simdata.V[0] - simdata.vrevs[Il]);
	
	// Now do main loop
	for(int i = 1; i < simdata.numpoints; ++i){
		double k1[6], k2[6], k3[6], k4[6];
		double h_2 = simdata.deltat/2;
		double tempgate[6];
		double tempCa, tempH;
				
		//step 1 - get k1 values
		for(int j = NN; j <= FF; ++j){
			k1[j] = dx(simdata.gatevars[j], simdata.V[i], simdata.T_x[j], simdata.vhalf_x[j], simdata.k_x[j]);
		}
		tempH = 1/(1+exp((simdata.vhalf_x[HH] - simdata.Ca[i-1])/simdata.k_x[HH]));
		k1[HH] = dCa(simdata.gxs, simdata.gatevars, simdata.vrevs, simdata.alphaCa, simdata.V[i], simdata.TCa, simdata.thiCa, simdata.Ca[i-1]);

		//step 2  - get k2 values
		tempCa = simdata.Ca[i-1] + k1[HH]*h_2;
		for(int j = NN; j <= FF; ++j){
			tempgate[j] =  (simdata.gatevars[j] + k1[j]*h_2);
			k2[j] = dx(tempgate[j], simdata.V[i], simdata.T_x[j], simdata.vhalf_x[j], simdata.k_x[j]);
		}
		tempH = 1/(1+exp((simdata.vhalf_x[HH] - tempCa)/simdata.k_x[HH]));
		k2[HH] = dCa(simdata.gxs, tempgate, simdata.vrevs, simdata.alphaCa, simdata.V[i], simdata.TCa, simdata.thiCa, tempCa);
		
		//step 3  - get k3 values
		tempCa = simdata.Ca[i-1] + k2[HH]*h_2;
		for(int j = NN; j <= FF; ++j){
			tempgate[j] =  (simdata.gatevars[j] + k2[j]*h_2);
			k3[j] = dx(tempgate[j], simdata.V[i], simdata.T_x[j], simdata.vhalf_x[j], simdata.k_x[j]);
		}
		tempH = 1/(1+exp((simdata.vhalf_x[HH] - tempCa)/simdata.k_x[HH]));
		k3[HH] = dCa(simdata.gxs, tempgate, simdata.vrevs, simdata.alphaCa, simdata.V[i], simdata.TCa, simdata.thiCa, tempCa);
	
		//step 4  - get k4 values
		tempCa = simdata.Ca[i-1] + k3[HH]*h_2*2;
		for(int j = NN; j <= FF; ++j){
			tempgate[j] =  (simdata.gatevars[j] + k3[j]*h_2*2);
			k4[j] = dx(tempgate[j], simdata.V[i], simdata.T_x[j], simdata.vhalf_x[j], simdata.k_x[j]);
		}
		tempH = 1/(1+exp((simdata.vhalf_x[HH] - tempCa)/simdata.k_x[HH]));
		k4[HH] = dCa(simdata.gxs, tempgate, simdata.vrevs, simdata.alphaCa, simdata.V[i], simdata.TCa, simdata.thiCa, tempCa);
	
		// now we must combine them to get final value
		for(int j = NN; j <= FF; ++j){
			simdata.gatevars[j] += (simdata.deltat/6)*(k1[j] + 2*k2[j] + 2*k3[j] + k4[j]);
		}
		simdata.Ca[i] = simdata.Ca[i-1] + (simdata.deltat/6)*(k1[HH] + 2*k2[HH] + 2*k3[HH] + k4[HH]);
		
		simdata.gatevars[HH] = 1/(1+exp((simdata.vhalf_x[HH] - simdata.Ca[i])/simdata.k_x[HH]));
		
		simdata.I[i] = simdata.gxs[IKs]*simdata.gatevars[NN]*(simdata.V[i] - simdata.vrevs[IKs]) + simdata.gxs[IKf]*pow(simdata.gatevars[PP],4)*simdata.gatevars[QQ]*(simdata.V[i] - simdata.vrevs[IKf]) + simdata.gxs[ICa]*pow(simdata.gatevars[EE],2)*simdata.gatevars[FF]*(1 + (simdata.gatevars[HH] - 1)*simdata.alphaCa)*(simdata.V[i]-simdata.vrevs[ICa]);// + simdata.gxs[Il]*(simdata.V[i] - simdata.vrevs[Il]);  NOTE: Il removed for consistency with Jospin

		//if(isnan(simdata.I[i])) cerr << "Vclamp has returned a NAN";
	}
	return simdata;
}
