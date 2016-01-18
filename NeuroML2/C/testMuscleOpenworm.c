// Using the data from https://github.com/openworm/muscle_model accessed on 12/14/15
#include <stdio.h>
#include <math.h>

typedef struct
{
	double tau;
} HHTime;

typedef struct
{
	double rate;
	double midpoint;
	double scale;
} HHVariable;

typedef struct
{
	HHTime timeCourse;
	HHVariable steadyState;
	unsigned int instances;
	double q;
} GateHHTauInf;

typedef struct
{
	unsigned int instances;
	double alpha;
	double k;
	double ca_half;
} CustomHGate;

typedef struct
{
	double restingConc;
	double decayConstant;
	double rho;
	double concentration;
} FixedFactorConcentrationModel;

typedef struct
{
	double condDensity;
	double erev;
} Leak;

typedef struct
{
	double condDensity;
	double erev;
	GateHHTauInf p_gate;
	GateHHTauInf q_gate;
} K_fast;

typedef struct
{
	double condDensity;
	double erev;
	GateHHTauInf n_gate;
} K_slow;

typedef struct
{
	double condDensity;
	double erev;
	GateHHTauInf e_gate;
	GateHHTauInf f_gate;
	CustomHGate h_gate;
} CA_boyle;

int main()
{
	double v;
	double totalSurfaceArea;
	double spikeThresh;
	double specificCapacitance;
	double iSyn;
	double iSynPrev;
	int spiking;
	FixedFactorConcentrationModel concentrationModel;
	Leak leak;
	K_fast k_fast;
	K_slow k_slow;
	CA_boyle ca_boyle;

	// initMembPotential
	v = -75.0;	// mV
	totalSurfaceArea = 2.0*M_PI*230.3459*10.0 * 1.0e-8;	// um2 to cm2
	spikeThresh = 0.0;
	specificCapacitance = 1.0 * 1.0e-3;	// uF_per_cm2 to mF_per_cm2
	// Incoming current from synapses (0 in this case)
	iSyn = 0.0;
	iSynPrev = 0.0;
	spiking = 0.0;

	// Create Muscle FixedFactorConcentrationModel
	concentrationModel.restingConc = 0.0;
	concentrationModel.decayConstant = 11.5943;	// ms
	concentrationModel.rho = 0.000238919 * 1.0e5;	// mol_per_m_per_A_per_s to m-mol_per_cm_per_mA_per_ms
	concentrationModel.concentration = 0.0;	// from species.initialConcentration

	// Create Muscle Ion Channels
	leak.condDensity = 0.0193181;	// mS_per_cm2
	leak.erev = 10.0;	// mV

	k_fast.condDensity = 0.399994;		// mS_per_cm2
	k_fast.erev = -54.9998;	// mV
	k_fast.p_gate.instances = 4.0;
	k_fast.p_gate.timeCourse.tau = 2.25518;	// ms
	k_fast.p_gate.steadyState.rate = 1.0;
	k_fast.p_gate.steadyState.midpoint = -8.05232;	// mV
	k_fast.p_gate.steadyState.scale = 7.42636;	// mV
	// Uses initMembPotential for muscle cell (-75)
	k_fast.p_gate.q = (k_fast.p_gate.steadyState.rate / (1.0 + exp(0.0 - (-75.0 - k_fast.p_gate.steadyState.midpoint) / k_fast.p_gate.steadyState.scale)));
	k_fast.q_gate.instances = 1.0;
	k_fast.q_gate.timeCourse.tau = 149.963;	// ms
	k_fast.q_gate.steadyState.rate = 1.0;
	k_fast.q_gate.steadyState.midpoint = -15.6456;	// mV
	k_fast.q_gate.steadyState.scale = -9.97468;	// mV
	// Uses initMembPotential for muscle cell (-75)
	k_fast.q_gate.q = (k_fast.q_gate.steadyState.rate / (1.0 + exp(0.0 - (-75.0 - k_fast.q_gate.steadyState.midpoint) / k_fast.q_gate.steadyState.scale)));

	k_slow.condDensity = 0.43584;		// mS_per_cm2
	k_slow.erev = -64.3461;	// mV
	k_slow.n_gate.instances = 1.0;
	k_slow.n_gate.timeCourse.tau = 25.0007;	// ms
	k_slow.n_gate.steadyState.rate = 1.0;
	k_slow.n_gate.steadyState.midpoint = 19.8741;	// mV
	k_slow.n_gate.steadyState.scale = 15.8512;	// mV
	// Uses initMembPotential for muscle cell (-75)
	k_slow.n_gate.q = (k_slow.n_gate.steadyState.rate / (1.0 + exp(0.0 - (-75.0 - k_slow.n_gate.steadyState.midpoint) / k_slow.n_gate.steadyState.scale)));

	ca_boyle.condDensity = 0.220209;		// mS_per_cm2
	ca_boyle.erev = 49.11;	// mV
	ca_boyle.e_gate.instances = 2.0;
	ca_boyle.e_gate.timeCourse.tau = 0.100027;	// ms
	ca_boyle.e_gate.steadyState.rate = 1.0;
	ca_boyle.e_gate.steadyState.midpoint = -3.3568;	// mV
	ca_boyle.e_gate.steadyState.scale = 6.74821;	// mV
	// Uses initMembPotential for muscle cell (-75)
	ca_boyle.e_gate.q = (ca_boyle.e_gate.steadyState.rate / (1.0 + exp(0.0 - (-75.0 - ca_boyle.e_gate.steadyState.midpoint) / ca_boyle.e_gate.steadyState.scale)));
	ca_boyle.f_gate.instances = 1.0;
	ca_boyle.f_gate.timeCourse.tau = 150.88;	// ms
	ca_boyle.f_gate.steadyState.rate = 1.0;
	ca_boyle.f_gate.steadyState.midpoint = 25.1815;	// mV
	ca_boyle.f_gate.steadyState.scale = -5.03176;	// mV
	// Uses initMembPotential for muscle cell (-75)
	ca_boyle.f_gate.q = (ca_boyle.f_gate.steadyState.rate / (1.0 + exp(0.0 - (-75.0 - ca_boyle.f_gate.steadyState.midpoint) / ca_boyle.f_gate.steadyState.scale)));
	// Definition of customHGate from ca_boyle.channel.nml
	ca_boyle.h_gate.instances = 1.0;
	ca_boyle.h_gate.alpha = 0.282473;
	ca_boyle.h_gate.k = -1.00056e-8;	// mM
	ca_boyle.h_gate.ca_half = 6.41889e-8;	// mM

	// Run Simulation for 1 minute with 1 ms timesteps
	for(int i = 0; i < 60000; i++)
	{
		double iCa;
		double totChanDensCurrentDensityCa;
		double deltaConcentration;
		double fopen;
		double h_q;
		double totChanDensCurrentDensity;

		/*
		 * Update Concentration Model
		 */
		totChanDensCurrentDensityCa = 0.0;
		fopen = 1.0;

		// Only use ca channel (ca_boyle)
		// e
		fopen *= pow(ca_boyle.e_gate.q, ca_boyle.e_gate.instances);
		// f
		fopen *= pow(ca_boyle.f_gate.q, ca_boyle.f_gate.instances);
		// h (custom)
		h_q = (1.0 / (1.0 + (exp((ca_boyle.h_gate.ca_half - concentrationModel.concentration) / ca_boyle.h_gate.k))));
		fopen *= (1.0 + ((h_q - 1.0) * ca_boyle.h_gate.alpha));

		totChanDensCurrentDensityCa = ((ca_boyle.condDensity * fopen) * (ca_boyle.erev - v));

		iCa = totChanDensCurrentDensityCa * totalSurfaceArea;

		deltaConcentration = (((iCa / totalSurfaceArea) * concentrationModel.rho) - ((concentrationModel.concentration - concentrationModel.restingConc)
		                     / concentrationModel.decayConstant));

		concentrationModel.concentration += deltaConcentration;

		if(concentrationModel.concentration < 0)
		{
			concentrationModel.concentration = 0.0;
		}

		/*
		 * End Update Concentration Model
		 */

		/*
		 * Update Channel Densities
		 *   deltaQ = (inf - q) / tau
		 */
		k_fast.p_gate.q += ((k_fast.p_gate.steadyState.rate / (1.0 + exp(0.0 - (v - k_fast.p_gate.steadyState.midpoint)
		                   / k_fast.p_gate.steadyState.scale))) - k_fast.p_gate.q) / k_fast.p_gate.timeCourse.tau;
		k_fast.q_gate.q += ((k_fast.q_gate.steadyState.rate / (1.0 + exp(0.0 - (v - k_fast.q_gate.steadyState.midpoint)
		                   / k_fast.q_gate.steadyState.scale))) - k_fast.q_gate.q) / k_fast.q_gate.timeCourse.tau;
		k_slow.n_gate.q += ((k_slow.n_gate.steadyState.rate / (1.0 + exp(0.0 - (v - k_slow.n_gate.steadyState.midpoint)
		                   / k_slow.n_gate.steadyState.scale))) - k_slow.n_gate.q) / k_slow.n_gate.timeCourse.tau;
		ca_boyle.e_gate.q += ((ca_boyle.e_gate.steadyState.rate / (1.0 + exp(0.0 - (v - ca_boyle.e_gate.steadyState.midpoint)
		                     / ca_boyle.e_gate.steadyState.scale))) - ca_boyle.e_gate.q) / ca_boyle.e_gate.timeCourse.tau;
		ca_boyle.f_gate.q += ((ca_boyle.f_gate.steadyState.rate / (1.0 + exp(0.0 - (v - ca_boyle.f_gate.steadyState.midpoint)
		                     / ca_boyle.f_gate.steadyState.scale))) - ca_boyle.f_gate.q) / ca_boyle.f_gate.timeCourse.tau;
		/*
		 * End Update Channel Densities
		 */

		/*
		 * Update Muscle
		 */
		iSynPrev = iSyn;
		iSyn = 0.0;
		/*
		 * End Update Muscle
		 */

		/*
		 * Update Muscle Voltage
		 *   iChannels = totChanDensCurrentDensity * surfaceArea
		 */
		totChanDensCurrentDensity = 0.0;

		// leak
		totChanDensCurrentDensity += (leak.condDensity * (leak.erev - v));

		// k_fast
		fopen = 1.0;
		// p
		fopen *= pow(k_fast.p_gate.q, k_fast.p_gate.instances);
		// q
		fopen *= pow(k_fast.q_gate.q, k_fast.q_gate.instances);
		totChanDensCurrentDensity += ((k_fast.condDensity * fopen) * (k_fast.erev - v));

		// k_slow
		fopen = 1.0;
		// n
		fopen *= pow(k_slow.n_gate.q, k_slow.n_gate.instances);
		totChanDensCurrentDensity += ((k_slow.condDensity * fopen) * (k_slow.erev - v));

		// ca_boyle
		fopen = 1.0;
		// e
		fopen *= pow(ca_boyle.e_gate.q, ca_boyle.e_gate.instances);
		// f
		fopen *= pow(ca_boyle.f_gate.q, ca_boyle.f_gate.instances);
		// h (custom)
		h_q = (1.0 / (1.0 + (exp((ca_boyle.h_gate.ca_half - concentrationModel.concentration) / ca_boyle.h_gate.k))));
		fopen *= (1.0 + ((h_q - 1.0) * ca_boyle.h_gate.alpha));
		totChanDensCurrentDensity += ((ca_boyle.condDensity * fopen) * (ca_boyle.erev - v));

		v += 1.0e-3 * (((totChanDensCurrentDensity * totalSurfaceArea) + iSynPrev) / (specificCapacitance * totalSurfaceArea));

		printf("v = %f mV\n", v);

		if((v > spikeThresh) && (!spiking))
		{
			spiking = 1;
		}
		else if(v < spikeThresh)
		{
			spiking = 0;
		}
	}

	return 0;
}

