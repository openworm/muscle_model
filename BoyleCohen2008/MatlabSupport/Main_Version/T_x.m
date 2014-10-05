%Generalised function for gettin time constants from given paramaters
function output = T_x(V,Vhalf,k,Tmin)

output = ((1 - Tmin)/[1 + exp(((V - Vhalf)/k)^2)])*2 + Tmin;