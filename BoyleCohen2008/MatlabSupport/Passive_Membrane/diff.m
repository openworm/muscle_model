%another simple program with passive membrane model. Effect of coupling on
%voltage difference between two cells
Vrest = -30e-3;
C1 = 30e-12;
C2 = 50e-12;
Gl = 1/1.5e9;
GJ = 370e-12;
Vl = -30e-3;
Iin = 30e-12;

duration = 1;
deltat = 0.01e-3;
numpoints = round(duration/deltat);
xaxis = deltat:deltat:duration;

V = ones(2,numpoints)*Vrest;
Igap = zeros(1,numpoints);

for i = 1:numpoints-1
    Igap(1,i) = GJ*(V(1,i) - V(2,i));
    dV1 = (Iin - Igap(1,i) - Gl*(V(1,i) - (Vl*C1/C1)))/C1;
    dV2 = (Iin + Igap(1,i) - Gl*(V(2,i) - (Vl*C2/C1)))/C2;
    V(1,i+1) = V(1,i) + dV1*deltat;
    V(2,i+1) = V(2,i) + dV2*deltat;
end

plot(xaxis*1e3,V(1,:)*1e3,'r',xaxis*1e3,V(2,:)*1e3,'b')
hold on
