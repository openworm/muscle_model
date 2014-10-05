%Voltage dependence of gap junciton
function output = Gjss(Vj)

A = 40;
V0 = 60e-3;
Gjmin = 0.13;

output = (1 - Gjmin)/(1 + exp(A*(abs(Vj) - V0))) + Gjmin;