duration = 100;
deltat = 10e-3;
num = duration/deltat;
A = 2;

signal = zeros(1,num);
Psig_calc = 0;

for i = 1:num
    signal(i) = A*cos(1*pi*deltat*i);
    Psig_calc = Psig_calc + signal(i)^2;
end
Psig_calc = Psig_calc/num

window = 2^12;

Fomega = fft(signal(1,:),window);

spect = Fomega.*conj(Fomega)/window;

deltaF = deltat^-1/window

Faxis = deltaF.*(0:window/2);

numreal = length(Faxis);

Psig_fft = 0;

for i = 1:numreal
    Psig_fft = Psig_fft + abs(spect(i));
end
Psig_fft/numreal