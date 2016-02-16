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

typedef struct
{
	double totalSurfaceArea;
	double spikeThresh;
	double specificCapacitance;
	double v;	// mV
	double iSyn;	// uA
	int spiking;
	FixedFactorConcentrationModel concentrationModel;
	Leak leak;
	K_fast k_fast;
	K_slow k_slow;
	CA_boyle ca_boyle;
} MuscleCell;

int main()
{
	const int integrationStepSize = 10;	// 10 us	// Need to use a step size < any of the taus
	const int simulationTime = 45 * 1e3;	// 45 ms
	MuscleCell muscleCells[7];

	// Initialize
	for(int j = 0; j < 7; j++)
	{
		muscleCells[j].totalSurfaceArea = 2.0 * M_PI * 230.3459 * (10.0 / 2.0) * 1.0e-8;	// um2 to cm2
		muscleCells[j].spikeThresh = 0.0;
		muscleCells[j].specificCapacitance = 1.0 * 1.0e-3;	// uF_per_cm2 to mF_per_cm2

		// initMembPotential
		muscleCells[j].v = -75.0;	// mV
		// Incoming current from synapses
		muscleCells[j].iSyn = (-120.0 * 1.0e-6);	// -120 pA
		muscleCells[j].spiking = 0;

		// Create Muscle FixedFactorConcentrationModel
		muscleCells[j].concentrationModel.restingConc = 0.0;
		muscleCells[j].concentrationModel.decayConstant = 11.5943;	// ms
		muscleCells[j].concentrationModel.rho = 0.000238919 * 1.0e5;	// mol_per_m_per_A_per_s to m-mol_per_cm_per_mA_per_ms
		muscleCells[j].concentrationModel.concentration = 0.0;	// from species.initialConcentration

		// Create Muscle Ion Channels
		muscleCells[j].leak.condDensity = 0.0193181;	// mS_per_cm2
		muscleCells[j].leak.erev = 10.0;	// mV

		muscleCells[j].k_fast.condDensity = 0.399994;		// mS_per_cm2
		muscleCells[j].k_fast.erev = -54.9998;	// mV
		muscleCells[j].k_fast.p_gate.instances = 4.0;
		muscleCells[j].k_fast.p_gate.timeCourse.tau = 2.25518;	// ms
		muscleCells[j].k_fast.p_gate.steadyState.rate = 1.0;
		muscleCells[j].k_fast.p_gate.steadyState.midpoint = -8.05232;	// mV
		muscleCells[j].k_fast.p_gate.steadyState.scale = 7.42636;	// mV
		// Uses initMembPotential for muscle cell (-75)
		muscleCells[j].k_fast.p_gate.q = (muscleCells[j].k_fast.p_gate.steadyState.rate / (1.0 + exp(0.0 - (-75.0 - muscleCells[j].k_fast.p_gate.steadyState.midpoint) / muscleCells[j].k_fast.p_gate.steadyState.scale)));
		muscleCells[j].k_fast.q_gate.instances = 1.0;
		muscleCells[j].k_fast.q_gate.timeCourse.tau = 149.963;	// ms
		muscleCells[j].k_fast.q_gate.steadyState.rate = 1.0;
		muscleCells[j].k_fast.q_gate.steadyState.midpoint = -15.6456;	// mV
		muscleCells[j].k_fast.q_gate.steadyState.scale = -9.97468;	// mV
		// Uses initMembPotential for muscle cell (-75)
		muscleCells[j].k_fast.q_gate.q = (muscleCells[j].k_fast.q_gate.steadyState.rate / (1.0 + exp(0.0 - (-75.0 - muscleCells[j].k_fast.q_gate.steadyState.midpoint) / muscleCells[j].k_fast.q_gate.steadyState.scale)));

		muscleCells[j].k_slow.condDensity = 0.43584;		// mS_per_cm2
		muscleCells[j].k_slow.erev = -64.3461;	// mV
		muscleCells[j].k_slow.n_gate.instances = 1.0;
		muscleCells[j].k_slow.n_gate.timeCourse.tau = 25.0007;	// ms
		muscleCells[j].k_slow.n_gate.steadyState.rate = 1.0;
		muscleCells[j].k_slow.n_gate.steadyState.midpoint = 19.8741;	// mV
		muscleCells[j].k_slow.n_gate.steadyState.scale = 15.8512;	// mV
		// Uses initMembPotential for muscle cell (-75)
		muscleCells[j].k_slow.n_gate.q = (muscleCells[j].k_slow.n_gate.steadyState.rate / (1.0 + exp(0.0 - (-75.0 - muscleCells[j].k_slow.n_gate.steadyState.midpoint) / muscleCells[j].k_slow.n_gate.steadyState.scale)));

		muscleCells[j].ca_boyle.condDensity = 0.220209;		// mS_per_cm2
		muscleCells[j].ca_boyle.erev = 49.11;	// mV
		muscleCells[j].ca_boyle.e_gate.instances = 2.0;
		muscleCells[j].ca_boyle.e_gate.timeCourse.tau = 0.100027;	// ms
		muscleCells[j].ca_boyle.e_gate.steadyState.rate = 1.0;
		muscleCells[j].ca_boyle.e_gate.steadyState.midpoint = -3.3568;	// mV
		muscleCells[j].ca_boyle.e_gate.steadyState.scale = 6.74821;	// mV
		// Uses initMembPotential for muscle cell (-75)
		muscleCells[j].ca_boyle.e_gate.q = (muscleCells[j].ca_boyle.e_gate.steadyState.rate / (1.0 + exp(0.0 - (-75.0 - muscleCells[j].ca_boyle.e_gate.steadyState.midpoint) / muscleCells[j].ca_boyle.e_gate.steadyState.scale)));
		muscleCells[j].ca_boyle.f_gate.instances = 1.0;
		muscleCells[j].ca_boyle.f_gate.timeCourse.tau = 150.88;	// ms
		muscleCells[j].ca_boyle.f_gate.steadyState.rate = 1.0;
		muscleCells[j].ca_boyle.f_gate.steadyState.midpoint = 25.1815;	// mV
		muscleCells[j].ca_boyle.f_gate.steadyState.scale = -5.03176;	// mV
		// Uses initMembPotential for muscle cell (-75)
		muscleCells[j].ca_boyle.f_gate.q = (muscleCells[j].ca_boyle.f_gate.steadyState.rate / (1.0 + exp(0.0 - (-75.0 - muscleCells[j].ca_boyle.f_gate.steadyState.midpoint) / muscleCells[j].ca_boyle.f_gate.steadyState.scale)));
		// Definition of customHGate from ca_boyle.channel.nml
		muscleCells[j].ca_boyle.h_gate.instances = 1.0;
		muscleCells[j].ca_boyle.h_gate.alpha = 0.282473;
		muscleCells[j].ca_boyle.h_gate.k = -1.00056e-8;	// mM
		muscleCells[j].ca_boyle.h_gate.ca_half = 6.41889e-8;	// mM
	}

	// Run Simulation for simulationTime useconds with integrationStepSize useconds timesteps
	for(int i = 0; i < simulationTime; i += integrationStepSize)
	{
		for(int j = 0; j < 7; j++)
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
			fopen *= pow(muscleCells[j].ca_boyle.e_gate.q, muscleCells[j].ca_boyle.e_gate.instances);
			// f
			fopen *= pow(muscleCells[j].ca_boyle.f_gate.q, muscleCells[j].ca_boyle.f_gate.instances);
			// h (custom)
			h_q = (1.0 / (1.0 + (exp((muscleCells[j].ca_boyle.h_gate.ca_half - muscleCells[j].concentrationModel.concentration) / muscleCells[j].ca_boyle.h_gate.k))));
			fopen *= (1.0 + ((h_q - 1.0) * muscleCells[j].ca_boyle.h_gate.alpha));

			totChanDensCurrentDensityCa = ((muscleCells[j].ca_boyle.condDensity * fopen) * (muscleCells[j].ca_boyle.erev - muscleCells[j].v));

			iCa = totChanDensCurrentDensityCa * muscleCells[j].totalSurfaceArea;

			deltaConcentration = (((iCa / muscleCells[j].totalSurfaceArea) * muscleCells[j].concentrationModel.rho) - ((muscleCells[j].concentrationModel.concentration - muscleCells[j].concentrationModel.restingConc) / muscleCells[j].concentrationModel.decayConstant));

			muscleCells[j].concentrationModel.concentration += (((double)integrationStepSize) * 1.0e-6) * 1.0e3 * deltaConcentration;

			if(muscleCells[j].concentrationModel.concentration < 0)
			{
				muscleCells[j].concentrationModel.concentration = 0.0;
			}

			/*
			 * End Update Concentration Model
			 */

			/*
			 * Update Channel Densities
			 *   deltaQ = (inf - q) / tau
			 */
			muscleCells[j].k_fast.p_gate.q += (((double)integrationStepSize) * 1.0e-6) * 1.0e3 * ((muscleCells[j].k_fast.p_gate.steadyState.rate / (1.0 + exp(0.0 - (muscleCells[j].v - muscleCells[j].k_fast.p_gate.steadyState.midpoint) / muscleCells[j].k_fast.p_gate.steadyState.scale))) - muscleCells[j].k_fast.p_gate.q) / muscleCells[j].k_fast.p_gate.timeCourse.tau;
			muscleCells[j].k_fast.q_gate.q += (((double)integrationStepSize) * 1.0e-6) * 1.0e3 * ((muscleCells[j].k_fast.q_gate.steadyState.rate / (1.0 + exp(0.0 - (muscleCells[j].v - muscleCells[j].k_fast.q_gate.steadyState.midpoint) / muscleCells[j].k_fast.q_gate.steadyState.scale))) - muscleCells[j].k_fast.q_gate.q) / muscleCells[j].k_fast.q_gate.timeCourse.tau;
			muscleCells[j].k_slow.n_gate.q += (((double)integrationStepSize) * 1.0e-6) * 1.0e3 * ((muscleCells[j].k_slow.n_gate.steadyState.rate / (1.0 + exp(0.0 - (muscleCells[j].v - muscleCells[j].k_slow.n_gate.steadyState.midpoint) / muscleCells[j].k_slow.n_gate.steadyState.scale))) - muscleCells[j].k_slow.n_gate.q) / muscleCells[j].k_slow.n_gate.timeCourse.tau;
			muscleCells[j].ca_boyle.e_gate.q += (((double)integrationStepSize) * 1.0e-6) * 1.0e3 * ((muscleCells[j].ca_boyle.e_gate.steadyState.rate / (1.0 + exp(0.0 - (muscleCells[j].v - muscleCells[j].ca_boyle.e_gate.steadyState.midpoint) / muscleCells[j].ca_boyle.e_gate.steadyState.scale))) - muscleCells[j].ca_boyle.e_gate.q) / muscleCells[j].ca_boyle.e_gate.timeCourse.tau;
			muscleCells[j].ca_boyle.f_gate.q += (((double)integrationStepSize) * 1.0e-6) * 1.0e3 * ((muscleCells[j].ca_boyle.f_gate.steadyState.rate / (1.0 + exp(0.0 - (muscleCells[j].v - muscleCells[j].ca_boyle.f_gate.steadyState.midpoint) / muscleCells[j].ca_boyle.f_gate.steadyState.scale))) - muscleCells[j].ca_boyle.f_gate.q) / muscleCells[j].ca_boyle.f_gate.timeCourse.tau;
			/*
			 * End Update Channel Densities
			 */

			/*
			 * Update Muscle
			 */
			muscleCells[j].iSyn = 0.0;

			// From 0 ms to 1000 ms
			if((i >= 0) && (i < 1000 * 1e3))
			{
				muscleCells[j].iSyn += (-120.0 * 1.0e-6);	// -120 pA
			}
			// From 5 ms to 25 ms
			if((i >= 5000) && (i < 25000))
			{
				muscleCells[j].iSyn += (j + 1) * (100.0 * 1.0e-6);	// 100 - 700 pA
			}
			/*
			 * End Update Muscle
			 */

			/*
			 * Update Muscle Voltage
			 *   iChannels = totChanDensCurrentDensity * surfaceArea
			 */
			totChanDensCurrentDensity = 0.0;

			// leak
			totChanDensCurrentDensity += (muscleCells[j].leak.condDensity * (muscleCells[j].leak.erev - muscleCells[j].v));

			// k_fast
			fopen = 1.0;
			// p
			fopen *= pow(muscleCells[j].k_fast.p_gate.q, muscleCells[j].k_fast.p_gate.instances);
			// q
			fopen *= pow(muscleCells[j].k_fast.q_gate.q, muscleCells[j].k_fast.q_gate.instances);
			totChanDensCurrentDensity += ((muscleCells[j].k_fast.condDensity * fopen) * (muscleCells[j].k_fast.erev - muscleCells[j].v));

			// k_slow
			fopen = 1.0;
			// n
			fopen *= pow(muscleCells[j].k_slow.n_gate.q, muscleCells[j].k_slow.n_gate.instances);
			totChanDensCurrentDensity += ((muscleCells[j].k_slow.condDensity * fopen) * (muscleCells[j].k_slow.erev - muscleCells[j].v));

			// ca_boyle
			fopen = 1.0;
			// e
			fopen *= pow(muscleCells[j].ca_boyle.e_gate.q, muscleCells[j].ca_boyle.e_gate.instances);
			// f
			fopen *= pow(muscleCells[j].ca_boyle.f_gate.q, muscleCells[j].ca_boyle.f_gate.instances);
			// h (custom)
			h_q = (1.0 / (1.0 + (exp((muscleCells[j].ca_boyle.h_gate.ca_half - muscleCells[j].concentrationModel.concentration) / muscleCells[j].ca_boyle.h_gate.k))));
			fopen *= (1.0 + ((h_q - 1.0) * muscleCells[j].ca_boyle.h_gate.alpha));
			totChanDensCurrentDensity += ((muscleCells[j].ca_boyle.condDensity * fopen) * (muscleCells[j].ca_boyle.erev - muscleCells[j].v));

			muscleCells[j].v += (((double)integrationStepSize) * 1.0e-6) * (((totChanDensCurrentDensity * muscleCells[j].totalSurfaceArea) + muscleCells[j].iSyn) / (muscleCells[j].specificCapacitance * muscleCells[j].totalSurfaceArea));
		}

		printf("%f", ((double)i) / 1000.0);
		for(int j = 0; j < 7; j++)
		{
			printf("\t%f", muscleCells[j].v);

			if((muscleCells[j].v > muscleCells[j].spikeThresh) && (!muscleCells[j].spiking))
			{
				muscleCells[j].spiking = 1;
			}
			else if(muscleCells[j].v < muscleCells[j].spikeThresh)
			{
				muscleCells[j].spiking = 0;
			}
		}
		printf("\n");
	}

	return 0;
}
