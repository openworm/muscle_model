#include "cost.hh"
using namespace std;

double cost(simulationdata simdata, int which, char type, double targets[8][20]){
	double cost, tempcost;
	float reference;
	float points[20];
	float weight[20] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
	int count = 0;
	int whichdata;
	float multiplier = 0;
	switch(type){
		case 'V':
			for(int i = (int)floor(simdata.numpoints/5); i < simdata.numpoints; i += 20){
				points[count] = simdata.V[i];
				//cerr << i << " ";
				++count;
			}
			multiplier = 1e3;
			whichdata = which;	
			break;
		case 'I':
			for(int i = (int)floor(simdata.numpoints/5)+10; i <= 3*(int)floor(simdata.numpoints/5); i += 10){//we add 2 to count so we get 20 pts
				//cerr << i << " ";
				points[count] = simdata.I[i];
				++count;
			}
			multiplier = 10e9;
			weight[0] = 0;
			weight[1] = 2;
			weight[2] = 2;
			weight[3] = 2;
			weight[4] = 2;
			weight[5] = 2;
			whichdata = which + 3;
			break;
	}		
	
	for(int i = 0; i < 20; ++i){
		reference = targets[whichdata][i];
		
		if(isnan(points[i])){
			cost = 1.2e60;
			//cerr << "\n A NAN cost has been removed";
			i = 20;
		}
		else{ 
			tempcost = pow(((reference - points[i])*multiplier),2)*weight[i];
			cost += tempcost;
		}
	}
	//cerr << "\n Good cost! = " << cost;
	return cost;
}

