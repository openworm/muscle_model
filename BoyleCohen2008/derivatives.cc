#include "derivatives.hh"
#include <iostream>
using namespace std;

double dx(double x, double V, double T, double vhalf, double k){
	double x_inf = 1/(1 + exp((vhalf - V)/k));
	return (x_inf - x)/T;
}

double dV(double gxs[4], double gatevars[6], double vrevs[4], double alphaCa, double Iin, double Cmem, double V){
	double Imem = gxs[IKs]*gatevars[NN]*(V-vrevs[IKs]) + gxs[IKf]*pow(gatevars[PP],4)*gatevars[QQ]*(V-vrevs[IKf]) + gxs[ICa]*pow(gatevars[EE],2)*gatevars[FF]*(1 + (gatevars[HH] - 1)*alphaCa)*(V-vrevs[ICa]) + gxs[Il]*(V-vrevs[Il]);
	return (-(Iin + Imem)/Cmem);
}

double dCa (double gxs[4], double gatevars[6], double vrevs[4], double alphaCa,  double V, double TCa, double thiCa, double Ca){
	double Ca_flow = gxs[ICa]*pow(gatevars[EE],2)*gatevars[FF]*(1 + (gatevars[HH] - 1)*alphaCa)*(V-vrevs[ICa]);
	return -(Ca/TCa + Ca_flow*thiCa);
}
