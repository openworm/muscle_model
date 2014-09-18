#include "evaluate.hh"
using namespace std;

double evaluate(vector2d candidate, int index, int genomelength, double targets[8][20]){
	//Declare normal variables
	double totalcost = 0;
	simulationdata simdata;
	float Istim[3] = {-100e-12, -400e-12, -700e-12};	
	float Vhold[3] = {0, 20e-3, 40e-3};
	
	simdata.deltat = 0.1e-3;
	simdata.numpoints = (int)round(0.05/simdata.deltat);
	
	//Next, we must decode the genome
	simdata.Cm = candidate[index][0];
	for(int i = 0; i < 4; ++i) simdata.gxs[i] = simdata.Cm*candidate[index][1+i];//to convert from A/F
	for(int i = 0; i < 4; ++i) simdata.vrevs[i] = candidate[index][5+i];
	for(int i = 0; i < 6; ++i) simdata.vhalf_x[i] = candidate[index][9+i];
	for(int i = 0; i < 6; ++i) simdata.k_x[i] = candidate[index][15+i];
	for(int i = 0; i < 5; ++i) simdata.T_x[i] = candidate[index][21+i];
	//Note, currently hoping I won't need to use V dependent time constants
	//for(int i = 0; i < 5; ++i) simdata.vhalf_Tx[i] = candidate[0][26+i];
	//for(int i = 0; i < 5; ++i) simdata.k_Tx[i] = candidate[0][31+i];
	simdata.TCa = candidate[index][26];//[36];
	simdata.alphaCa = candidate[index][27];//[37];	
	//Now the constant(s) and multiplication of paramaters...
	simdata.thiCa = 6.1e-6/(simdata.gxs[ICa]*simdata.TCa);
	simdata.vhalf_x[5] *= 1e-9;
	simdata.k_x[5] *= 1e-9;

	// The following sections must be repeated 3 times, once for each Istim
	for(int j = 0; j < 3; ++j){
		//then we must set up the input current
		for(int i = 0; i < simdata.numpoints; ++i) simdata.I[i] = (simdata.gxs[Il]*(75e-3 + simdata.vrevs[Il]));
			// Adding Ibias for compatibility with measurements from Matlab version
        	for(int i = simdata.numpoints/5; i <= (simdata.numpoints/5)*3; ++i){ 
			simdata.I[i] += Istim[j];
		}
			//Now add stimulation for 20ms
       	
      		//now it is time to do the actual simulation
		
		simdata = Iclamp(simdata);
		// here we evaluate the simulation to get cost
		totalcost += cost(simdata, j, 'V', targets);	
		//cerr << " Iclamp cost = " << tempcost;
	}
	// The following sections are repeated 3 times, once for each Vhold
	for(int j = 0; j < 3; ++j){
		//then we must set up the voltage pattern 
		for(int i = 0; i < simdata.numpoints; ++i) simdata.V[i] = -70e-3; 
		//Now add stimulation for 20ms
        	for(int i = simdata.numpoints/5; i <= 3*(int)floor(simdata.numpoints/5); ++i){ 
			simdata.V[i] = Vhold[j];
		}
      		//now it is time to do the actual simulation
		
		simdata = vclamp(simdata);
		 //here we evaluate the simulation to get cost
		totalcost += cost(simdata, j, 'I',targets);	
		//cerr << " Vclamp cost = " << tempcost;
	}
	
	// This section checks the steady state IV relationship
	totalcost += IVcost(simdata, targets);

	return totalcost;
}
