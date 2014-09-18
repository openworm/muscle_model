#include <cmath>
#define IKs 0
#define IKf 1
#define ICa 2
#define Il 3
#define NN 0
#define PP 1
#define QQ 2
#define EE 3
#define FF 4
#define HH 5

double dx(double x, double V, double T, double vhalf, double k);

double dV(double gxs[4], double gatevars[6], double vrevs[4], double alphaCa, double Iin, double Cmem, double V);

double dCa(double gxs[4], double gatevars[6], double vrevs[4], double alphaCa, double V, double TCa, double thiCa, double Ca);

