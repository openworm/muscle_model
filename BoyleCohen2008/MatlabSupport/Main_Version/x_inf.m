%Generalised funciton for getting x_inf from given paramaters
function output = x_inf(V,Vhalf,k)

output = 1/[1 + exp((Vhalf - V)/k)];