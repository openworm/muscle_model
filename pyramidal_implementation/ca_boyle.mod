COMMENT


My attempt at encoding boyle's theory into a mod file


ENDCOMMENT


NEURON {
    SUFFIX ca_boyle
    USEION ca READ cai WRITE ica
    RANGE gbar
    RANGE e, f, h
    GLOBAL eca
}




PARAMETER {
    gbar     = 100      (pS/um2)

    eca  = 49.1    (mV)

    v                                 (mV)
    dt                                (ms)

    vmin     = -150    (mV)
    vmax     = 150    (mV)

    cai 	= .000050 (mM)		: initial [Ca]i = 50 nM
:    cao 	= 2	(mM)		: [Ca]o = 2 mM

    e_half	= -3.4 (mv)
    f_half	=  25.2 (mv)
    h_half	= 64.1e-9 :units?
    
    f_slope 	=  5.0 (mv)
    e_slope	=  6.7 (mv)
    h_slope	=  -10e-3  (mM)


    alpha_ca	= 0.283    

    etau = 0.1    (ms)
    ftau = 151.0    (ms)
    htau = 11.6	  (ms)

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
    hinf
}


STATE { e f h }


INITIAL {
    trates(v)
    e = einf
    f = finf
    h = hinf
}




BREAKPOINT {
    SOLVE states METHOD cnexp
    gca = gbar*e*e*f*(1 + (h-1) * alpha_ca)
    ica = (1e-4) * gca * (v - eca)
}



DERIVATIVE states {
    trates(v)
    e' =  (einf-e) / etau
    f' =  (finf-f) / ftau
    h' =  (hinf-h) / htau
}




PROCEDURE trates(v) {
    TABLE einf, etau, finf, ftau, hinf, htau
    FROM vmin TO vmax WITH 199
    rates(v): not consistently executed from here if usetable == 1
}



PROCEDURE rates(vm) {

    einf = inf(vm,e_half,e_slope)
    finf = inf(vm,f_half,f_slope)
    hinf = inf(cai,h_half,h_slope)

}

FUNCTION inf(v,v_half,k) {

	 inf = 1 / (1 + exp((v_half - v) / k))
}

