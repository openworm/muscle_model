#include "populator.hh"
using namespace std;

vector2d populator(int popsize, int genomelength, vector2d max_min){

	int seed = 0; 
	rseed(&seed);
	vector2d pop = create_vector2d((popsize + 2), genomelength);
	
	for (int i = 0; i < popsize; ++i){
		for (int j = 0; j < genomelength; ++j){
			//I have decided to try initally with a uniform distribution over a wide range. 
			pop[i][j] = (max_min[1][j] + randval(max_min[0][j] - max_min[1][j]));
		}
	}
	for(int j = 0; j < genomelength; ++j){ 
		pop[popsize][j] = max_min[0][j];
		pop[popsize+1][j] = max_min[1][j];
	}
	return pop;
}
