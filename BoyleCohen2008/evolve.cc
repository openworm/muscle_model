#include <iostream>
#include "evolve.hh"
using namespace std;

vector2d evolve(int popsize, int genomelength, vector2d pop, int numgens, float CR, float F, double targets[8][20]){
	// here we declare variables and determine the initial cost matrix
	vector2d optimum = create_vector2d(2,genomelength);
	vector2d trial  = create_vector2d(1,genomelength);
	vector2d pop2 = create_vector2d(popsize, genomelength);
	double cost[popsize];
	double bestcost = 1e40;
	int bestmember = -1;
		
	for(int i = 0; i < popsize ; ++i){
		//trial[0] = pop[i];
		cost[i] = evaluate(pop, i, genomelength, targets);
		//cerr << "\n costed @ " << cost[i];

		if(cost[i] < bestcost){
			bestcost = cost[i];
			bestmember = i;
			optimum[0] = pop[i];
		}
	}	


	
	double score;
	int count = 0;
	int a, b, c, j;
	// here we begin the generations of the GA
	while(count < numgens){
		for(int i = 0; i < popsize; ++i){
			do {a = randval(popsize - 1);} while(a==i);
			do {b = randval(popsize - 1);} while(b==i||b==a);
			do {c = randval(popsize - 1);} while(c==i||c==b||c==a);
			j = randval(genomelength - 1);
			for(int k = 0; k < genomelength - 1; ++k){
				double x = randval(1);
				if(x < CR || k==genomelength-1){
					trial[0][j] = pop[c][j] + F*(pop[b][j]-pop[a][j]);
					while(trial[0][j] < pop[popsize+1][j]){ 
						trial[0][j] = (pop[popsize][j] + (trial[0][j] - pop[popsize+1][j]));//wrap round
					}
					while(trial[0][j] > pop[popsize][j]){ 
						trial[0][j] = (pop[popsize+1][j] + (trial[0][j] - pop[popsize][j]));//wrap round
					}
				}
				else{ 
					trial[0][j] = pop[i][j];
				}
				j = (++j)%genomelength;
			}

		score = evaluate(trial, 0, genomelength, targets);
		if(score <= cost[i]){
			for(int k = 0; k < genomelength; ++k) pop2[i][k] = trial[0][k];
			cost[i] = score;
		}
		else for(int k = 0; k < genomelength; ++k) pop2[i][k] = pop[i][k];
		}

		for(int i = 0; i < popsize; ++i){
			pop[i] = pop2[i];
		}
	++count;
	bestcost = cost[0];
	bestmember = 0;
	optimum[0] = pop[0];
	for(int i = 1; i < popsize; ++i){
		if(cost[i] < bestcost){
			bestcost = cost[i];
			bestmember = i;
			optimum[0] = pop[i];
		}
	}
	}
	optimum[1][0] = bestcost;
	return optimum;
}
