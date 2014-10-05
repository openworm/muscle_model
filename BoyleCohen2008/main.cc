#include "header.hh"
using namespace std;
double targets[8][20];

int main(int argc, char*argv[]) {

	//here we load the data
	ifstream in0("data/data100.csv");
        ifstream in1("data/data400.csv");
        ifstream in2("data/data700.csv");
        ifstream in3("data/V_0.csv");
        ifstream in4("data/V_20.csv");
        ifstream in5("data/V_40.csv");
        ifstream in6("data/IK_ss.csv");
        ifstream in7("data/ICa_pk.csv");
        for(int i = 0; i < 20; ++i){
                in0 >> targets[0][i];
                in1 >> targets[1][i];
                in2 >> targets[2][i];
                in3 >> targets[3][i];
                in4 >> targets[4][i];
                in5 >> targets[5][i];
        }
        for(int i = 0; i < 10; ++i){
                in6 >> targets[6][i];
                in7 >> targets[7][i];
        }
        in0.close();
        in1.close();
        in2.close();
        in3.close();
        in4.close();
        in5.close();
        in6.close();
        in7.close();
	
	//This was the start of the program
	int popsize, genomelength, numgens;
	genomelength = 28;//38;  //  38 needed if we want to include V dependent time constants
	popsize = genomelength * 15;
	numgens = 500;
	int choice;
	char PCnum;
	if(argc > 1){
		PCnum = argv[1][0];
	}
	else{
		PCnum = '0';
	}
	cout << "\n	 Main Program:\n	1) Run New Evolution\n	2) Read In Results\n";
	cin >> choice;
	float F[] = {0.1};//{0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1};
	int numF = 1;//10;  //NOTE! change here for a range of F vals
	float CR[] = {0.2, 0.8};//{0, 0.2, 0.4, 0.6, 0.8};
	int numCR = 2;//5;
	int numeach = 5;
	char filename[] = "results/PC_w_F_x_CR_y_num_zz.csv";
	char num_to_char[2][20] = {
	       	{'0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'},
                {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        };
	if(choice == 1){
		double max_min[2][genomelength];
		//I must still make sure the genome is correct!!!!!
		vector2d max_min_vector = create_vector2d(2,genomelength);
		cerr << "\n Setting Limits ";	
		max_min[0][0] = 80e-12;		//max Cmem
		max_min[1][0] = 70e-12;		//min Cmem
		max_min[0][1] = 500;		//max gKs A/F
		max_min[1][1] = 100;		//min gKs A/F
		max_min[0][2] = 400;		//max gKf 
		max_min[1][2] = 50;		//min gKf
		max_min[0][3] = 400;		//max gCa
		max_min[1][3] = 100;		//min gCa
		max_min[0][4] = 50;		//max gLeak
		max_min[1][4] = 5;		//min gLeak
		max_min[0][5] = -55e-3;		//max Vks
		max_min[1][5] = -80e-3;		//min Vks	
		max_min[0][6] = -35e-3;		//max Vkf
		max_min[1][6] = -55e-3;		//min Vkf
		max_min[0][7] = 70e-3;		//max VCa
		max_min[1][7] = 40e-3;		//min VCa
		max_min[0][8] = 20e-3;		//max VL
		max_min[1][8] = -40e-3;		//min VL
		max_min[0][9] = 30e-3;		//max Vn
		max_min[1][9] = -10e-3;		//min Vn
		max_min[0][10] = 30e-3;		//max Vp
		max_min[1][10] = -10e-3;	//min Vp
		max_min[0][11] = 30e-3;		//max Vq 
		max_min[1][11] = -20e-3;	//min Vq
		max_min[0][12] = 30e-3;		//max Ve
		max_min[1][12] = -10e-3;	//min Ve
		max_min[0][13] = 30e-3;		//max Vf
		max_min[1][13] = -10e-3;	//min Vf
		max_min[0][14] = 300;		//max [Ca2+]_0.5 Note, later multiplication by 1e-9 is required
		max_min[1][14] = 10;		//min [Ca2+]_0.5 as above
		max_min[0][15] = 20e-3;		//max kn
		max_min[1][15] = 4e-3;		//min kn
		max_min[0][16] = 20e-3;		//max kp
		max_min[1][16] = 4e-3;		//min kp
		max_min[0][17] = -5e-3;		//max kq
		max_min[1][17] = -30e-3;	//min kq
		max_min[0][18] = 20e-3;		//max ke
		max_min[1][18] = 4e-3;		//min ke
		max_min[0][19] = -5e-3;		//max kf
		max_min[1][19] = -30e-3;	//min kf
		max_min[0][20] = -10;		//max kh Note, later multiplication by 1e-9 is required
		max_min[1][20] = -150;		//min kh as above
		max_min[0][21] = 75e-3;		//max Tn
		max_min[1][21] = 25e-3;		//min Tn
		max_min[0][22] = 20e-3;		//max Tp
		max_min[1][22] = 1e-3;		//min Tp
		max_min[0][23] = 150e-3;	//max Tq 
		max_min[1][23] = 15e-3;		//min Tq
		max_min[0][24] = 2e-3;		//max Te
		max_min[1][24] = 0.1e-3;	//min Te
		max_min[0][25] = 500e-3;	//max Tf
		max_min[1][25] = 150e-3;	//min Tf
		max_min[0][26] = 20e-3;		//max TCa 	
		max_min[1][26] = 0.5e-3;	//min TCa 
		max_min[0][27] = 0.4;		//max alphaCa		
		max_min[1][27] = 0.1;		//min alphaCa
		/*max_min[0][28] = 0e-3;
		max_min[1][28] = 0e-3;	
		max_min[0][29] = 0e-3;
		max_min[1][29] = 0e-3;	
		max_min[0][30] = 0e-3;
		max_min[1][30] = 0e-3;	
		max_min[0][31] = 0e-3;
		max_min[1][31] = 0e-3;	
		max_min[0][32] = 0e-3;
		max_min[1][32] = 0e-3;	
		max_min[0][33] = 0e-3;
		max_min[1][33] = 0e-3;	
		max_min[0][34] = 0e-3;
		max_min[1][34] = 0e-3;	
		max_min[0][35] = 0e-3;
		max_min[1][35] = 0e-3;	
		max_min[0][36] = 0e-3;
		max_min[1][36] = 0e-3;	
		max_min[0][37] = 0e-3;
		max_min[1][37] = 0e-3;	*/
		
		for(int i = 0; i < genomelength; ++i){
			max_min_vector[0][i] = max_min[0][i];
			max_min_vector[1][i] = max_min[1][i];
		}

		vector2d pop = create_vector2d((popsize + 2), genomelength);
		vector2d optimum = create_vector2d(2, genomelength);
		//start multi test loop here?
		for(int x = 0; x < numF; ++x){
			for(int y = 0; y < numCR; ++y){
				for(int z = 0; z < numeach; ++z){
					pop = populator(popsize, genomelength, max_min_vector);
					cerr << "\n populated";
					optimum = evolve(popsize, genomelength, pop, numgens, CR[y], F[x], targets);
					cerr << "\n evolve finished";	
					filename[11] = PCnum;
					filename[15] = num_to_char[1][x];
					filename[20] = num_to_char[1][y];
					filename[26] = num_to_char[0][z];
					filename[27] = num_to_char[1][z];
					
					ofstream outfile(filename);
					
					for(int i = 0; i < genomelength; ++i){
						outfile << optimum[0][i] << "\n";
					}
					outfile << optimum[1][0];
					outfile.close();
					cout << "\n	File : " << filename << " has been written";
				}
			}
		}
	}
	else if(choice == 2){
		vector2d best = create_vector2d(3,genomelength + 1);
		best = findbest(genomelength, numF, numCR, numeach, filename, CR, F);
		ofstream outfile("simtest/opt.csv");
		for(int i = 0; i < genomelength; ++i){
			outfile << best[2][i] << "\n";
		}
		outfile.close();
	}		
	else{
		cout << "\n Error!\n";
	}
	return 0;
}
	
