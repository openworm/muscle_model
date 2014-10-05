%This simple program models the membrane completely passively, with just a
%leak conductance and capacitance
Vrest = -30e-3;
C = 30e-12;
Gl = 1/1.5e9;
GJ = 370e-12;
Iin = 10e-12;

duration = 1;
deltat = 0.01e-3;
numpoints = round(duration/deltat);
xaxis = deltat:deltat:duration;

Vstim = ones(1,numpoints)*Vrest;
Vout = ones(1,numpoints)*Vrest;
Igap = zeros(1,numpoints);

A = 50e-3;
D = 25e-3;
T = 150e-3;
numspikes = floor(duration/T);

for i = 1:numspikes
    index = round((T*i - D)/(deltat));
    for j = 1:round(D/deltat);
        Vstim(1,index + j) = Vstim(1,index + j) + A;
    end
end

for i = 1:numpoints-1
    Igap(1,i) = GJ*(Vstim(1,i) - Vout(1,i));
    Ileak = Gl*(Vout(1,i) - Vrest);
    dV = (Iin + Igap(1,i) - Ileak)/C;
    Vout(1,i+1) = Vout(1,i) + dV*deltat;
end

subplot(2,1,1),plot(xaxis*1e3,Vstim*1e3,'r',xaxis*1e3,Vout*1e3,'b')
hold on
subplot(2,1,2),plot(xaxis*1e3,Igap*1e12,'k')
hold on