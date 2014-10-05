#include "IVcost.hh"
using namespace std;

double IVcost(simulationdata simdata, double targets[8][20]){
	double cost = 0;
	double  n_inf, p_inf, q_inf, e_inf, f_inf, h_inf;
	float K_ref, Ca_ref;
	float K_points[10], Ca_points[10];
	float V;
	
	for(int i = 0; i < 10; ++i){
		V = -50e-3 + i*10e-3;
		n_inf = 1/(1 + exp((simdata.vhalf_x[NN] - V)/simdata.k_x[NN]));
		p_inf = 1/(1 + exp((simdata.vhalf_x[PP] - V)/simdata.k_x[PP]));
		q_inf = 1/(1 + exp((simdata.vhalf_x[QQ] - V)/simdata.k_x[QQ]));
		K_points[i] = simdata.gxs[IKf]*pow(p_inf, 4)*q_inf*(V - simdata.vrevs[IKf]) + simdata.gxs[IKs]*n_inf*(V - simdata.vrevs[IKs]);
		K_points[i] /= simdata.Cm;

		//NOTE: in order to avoid problems with Ca2+ inactivation, I have decided to use the peak IV relationship for ICa
		V = -30e-3 + i*10e-3;
		e_inf = 1/(1 + exp((simdata.vhalf_x[EE] - V)/simdata.k_x[EE]));
		f_inf = 1;	
		h_inf = 1;
		
		Ca_points[i] = simdata.gxs[ICa]*pow(e_inf, 2)*f_inf*h_inf*(V - simdata.vrevs[ICa]);
		Ca_points[i] /= simdata.Cm;
	}	
	
	for(int i = 0; i < 10 ; ++i){
		K_ref = targets[6][i];
		cost +=	pow((K_ref - K_points[i])*4,2)*50;
	}
	
	for(int i = 0; i < 10 ; ++i){
		Ca_ref = targets[7][i];
		cost +=	pow((Ca_ref - Ca_points[i])*4,2)*100;
	}
	if(isnan(cost)){
		//cerr << "IVcost.hh has returned NAN!";
		cost = 1e60;
	}
	//cerr << "\n Good cost! = " << cost;
	return cost;
}
	
