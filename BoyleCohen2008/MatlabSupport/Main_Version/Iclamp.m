%Program for simulating full model with coupling

%importing data
data = importdata('data/input.csv'); %Not sure if these are the best paramaters...

% Model paramaters

Cmem = data(1);
gKS = data(2)*Cmem;
gKF = data(3)*Cmem;
gCa = data(4)*Cmem;
gL = data(5)*Cmem;
VKS = data(6);
VKF = data(7);
VCa = data(8);
VL = 10e-3;%data(9);
Vhalf_n = data(10);
Vhalf_p = data(11);
Vhalf_q = data(12);
Vhalf_e = data(13);
Vhalf_f = data(14);
Cahalf_h = data(15)*1e-9;
k_n = data(16);
k_p = data(17);
k_q = data(18);
k_e = data(19);
k_f = data(20);
k_h = data(21)*1e-9;
T_n = data(22);
T_p = data(23);
T_q = data(24);
T_e = data(25);
T_f = data(26);
T_Ca = data(27);
alphaCa = data(28);
thiCa = 6.1e-6/(T_Ca*gCa);


%Simulation Paramaters
deltat = 0.01e-3;
duration = 0.045                 %*********************      Duration    Duration   ***************
numpoints = round(duration/deltat);
numtests = 7;   
xaxis = (deltat:deltat:duration)*1e3;

%Input paramaters
onset = round(0.005/deltat);
offset = round(0.025/deltat);

%Variable Declaration
I_in = zeros(numtests,numpoints);
I_j = zeros(numtests+1,1);
V = zeros(numtests,numpoints);
Ca = zeros(numtests,numpoints);
n = zeros(numtests,1);
p = zeros(numtests,1);
q = zeros(numtests,1);
e = zeros(numtests,1);
f = zeros(numtests,1);
h = zeros(numtests,1);

for i = 1:numtests
    for j = 1:numpoints
        I_in(i,j) = -gL*(-75e-3 - VL);        
    end
end
Istim = -100e-12;
for i = 1:numtests
    for j = onset:offset
        I_in(i,j) = I_in(i,j) + Istim;
    end
    Istim = Istim - 100e-12;
end

%variable initialization
for j = 1:numtests
    V(j,1) = -75e-3;
    Ca(j,1) = 0;
    n(j,1) = x_inf(V(j,1),Vhalf_n,k_n);
    p(j,1) = x_inf(V(j,1),Vhalf_p,k_p);
    q(j,1) = x_inf(V(j,1),Vhalf_q,k_q);
    e(j,1) = x_inf(V(j,1),Vhalf_e,k_e);
    f(j,1) = x_inf(V(j,1),Vhalf_f,k_f);
end

%start of simulation
for j = 1:numtests    
    
    for i = 2:numpoints
        
        dn = (x_inf(V(j,i-1),Vhalf_n,k_n) - n(j,1))/T_n;
        n(j,1) = n(j,1) + dn*deltat;
        dp = (x_inf(V(j,i-1),Vhalf_p,k_p) - p(j,1))/T_p;
        p(j,1) = p(j,1) + dp*deltat;
        dq = (x_inf(V(j,i-1),Vhalf_q,k_q) - q(j,1))/T_q;
        q(j,1) = q(j,1) + dq*deltat;
        de = (x_inf(V(j,i-1),Vhalf_e,k_e) - e(j,1))/T_e;
        e(j,1) = e(j,1) + de*deltat;
        df = (x_inf(V(j,i-1),Vhalf_f,k_f) - f(j,1))/T_f;
        f(j,1) = f(j,1) + df*deltat;
        h(j,1) = x_inf(Ca(j,i-1),Cahalf_h,k_h);
        
        IKS = gKS*n(j,1)*(V(j,i-1) - VKS);
        IKF = gKF*p(j,1)^4*q(j,1)*(V(j,i-1) - VKF);
        ICa = gCa*e(j,1)^2*f(j,1)*(1 + (h(j,1) - 1)*alphaCa)*(V(j,i-1) - VCa);
        IL = gL*(V(j,i-1) - VL);
        
        dCa = -(Ca(j,i-1)/T_Ca + thiCa*ICa);
        Ca(j,i) = Ca(j,i-1) + dCa*deltat;
        
        
        dv = -(I_in(j,i) + IKS + IKF + ICa + IL)/Cmem;
        V(j,i) = V(j,i-1) + dv*deltat;
    end
    plot(xaxis,V(j,:)*1e3,'k');
    hold on
end
ylabel('V_{mem} (mV)')
xlabel('Time (ms)')
