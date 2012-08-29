#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," ca.mod");
    fprintf(stderr," k_fast.mod");
    fprintf(stderr," k_slow.mod");
    fprintf(stderr, "\n");
  }
  _ca_reg();
  _k_fast_reg();
  _k_slow_reg();
}
