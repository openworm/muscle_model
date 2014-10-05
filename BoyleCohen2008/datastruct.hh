struct simulationdata{
	float deltat;
	int numpoints;
	double Cm;
	double gxs[4];
	double vrevs[4];
	double vhalf_x[6];
	double k_x[6];
	double T_x[5];
	//double vhalf_Tx[5];
	//double k_Tx[5];
	double TCa;
	double alphaCa;
	double thiCa;
	float I[500];//100 = numpoints, can't figure out how to use a variable??
	float V[500];//100 = numpoints, can't figure out how to use a variable??
	double Ca[500];
	double gatevars[6];
};
