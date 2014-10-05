#include "decoder.hh"
using namespace std;

vector2d findbest(int genomelength, int numF, int numCR, int numeach, char in_name[], float CR[], float F[]){
	
	char num_to_char[2][20] = {
		{'0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'}, 
		{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
	};
	
	vector2d data = create_vector2d(4, genomelength + 1);	
	data[1][genomelength] = 1e25; 
 	data[2][genomelength] = 1e25;	
	data[3][genomelength] = 0;
	vector2d good = create_vector2d(100, genomelength +1);
	int numgood = 0;
	char PCnum;

	cerr << "\n	Please enter PC number: ";
	cin >> PCnum;

	for(int x = 0; x < numF; ++x){
		for(int y = 0; y < numCR; ++y){
			for(int z = 0; z < numeach; ++z){
				char* filename = in_name;
				filename[11] = PCnum;
				filename[15] = num_to_char[1][x];
				filename[20] = num_to_char[1][y];
				filename[26] = num_to_char[0][z];
				filename[27] = num_to_char[1][z];
				cerr << "\n	" << filename;	
			       	ifstream infile(filename);
				int i = 0;
				while(!infile.eof()){
					infile >> data[0][i];
					++i;
				}
				infile.close();
				
				if(isnan(data[0][genomelength])){
					cerr << "\nNAN alert!";
				}
				else{
				data[3][genomelength] += data[0][genomelength];
				if(data[0][genomelength] < data[1][genomelength]){
					for(int j = 0; j < (genomelength + 1); ++j){
						data[1][j] = data[0][j];
					}
				}
				if(data[0][genomelength] < data[2][genomelength]){
					for(int j = 0; j < (genomelength + 1); ++j){
						data[2][j] = data[0][j];
					}
				}
				/*
				if(data[0][genomelength] < 600){
					for(int j = 0; j < (genomelength + 1); ++j){
						good[numgood][j] = data[0][j];
					}
					++numgood;
				}
				*/
				}
				cerr << "\n Checked \n";
			}
			cout << "\n  For F = "<< F[x] << ", CR = " << CR[y] << ", best cost is : " << data[1][genomelength] << " and mean cost is : " << data[3][genomelength];
			data[1][genomelength] = 1e15;	
			data[3][genomelength] = 0;
		}
	}
	cout << "\n Best cost overall = " << data[2][genomelength];
	ofstream outfile("results/promising.csv");
	for(int j = 0; j < (genomelength + 1); ++j){
		for(int k = 0; k < numgood; ++k){
			outfile << good[k][j] << ", ";
		}
		outfile << endl;
	}
	outfile.close();
	return data;
}
