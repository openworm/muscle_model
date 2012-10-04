COMMENT


My attempt at encoding boyle's theory into a mod file


ENDCOMMENT


NEURON {
    SUFFIX ca_boyle
    USEION ca READ cai,cao WRITE ica
    RANGE gbar
    RANGE e, f
    RANGE einf, etau
    GLOBAL eca
}




PARAMETER {
    gbar     = 100      (pS/um2)
    eca  = 100.0    (mV)
    v                                 (mV)
    dt                                (ms)
    vmin     = -150    (mV)
    vmax     = 150    (mV)
    cai 	= .000050 (mM)		: initial [Ca]i = 50 nM
    cao 	= 2	(mM)		: [Ca]o = 2 mM
    etau = 1    (ms)
    ftau = 1    (ms)
}




UNITS {
     (mA) = (milliamp)
     (mV) = (millivolt)
     (pS) = (picosiemens)
     (um) = (micron)
}




ASSIGNED {
    ica    (mA/cm2)
    gca    (pS/um2)
    einf
    finf
}


STATE { e f }


INITIAL {
    trates(v)
    e = einf
    f = finf
}




BREAKPOINT {
    SOLVE states METHOD cnexp
    gca = gbar*e*e*f
    gca = 0
    ica = (1e-4) * gca * (v - eca)
}




LOCAL mexp
LOCAL hexp




DERIVATIVE states {
    trates(v)
    e' =  (einf-e)/etau
    f' =  (finf-f)/ftau
}




PROCEDURE trates(v) {
    TABLE einf, etau, finf, ftau
    FROM vmin TO vmax WITH 199
    rates(v): not consistently executed from here if usetable == 1
}



PROCEDURE rates(vm) {

    einf = 1e-0
    finf = 1e-0

}





:FUNCTION trap0(v,A,B,C,D,F) {
:	if (fabs(v/A) > 1e-6) {
:	        trap0 = (A + B * v) / (C + exp((v + D)/F))
:	} else {
:	        trap0 = B * F
: 	}
:}


