%Program for simulating full model with coupling

%importing data
data = importdata('data/input.csv'); %Not sure if these are the best paramaters...

% Model paramaters

Cmem = 30e-12;%data(1);
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
ICa_max = 6.721*Cmem;


%connectivity paramaters
g_ji = 0;%370e-12;%12.33*Cmem;             %********************       Gj    GJ     GJ    *********************



%Simulation Paramaters
deltat = 0.01e-3;
duration = 4;                %*********************      Duration    Duration   ***************
numpoints = round(duration/deltat);
numcells = 4;   
xaxis = (deltat:deltat:duration)*1e3;

%Variable Declaration
I_in = zeros(numcells,numpoints);
I_j = zeros(numcells+1,1);
V = zeros(numcells,numpoints);
Ca = zeros(numcells,numpoints);
n = zeros(numcells,1);
p = zeros(numcells,1);
q = zeros(numcells,1);
e = zeros(numcells,1);
f = zeros(numcells,1);
h = zeros(numcells,1);

%input initialization
A = -250e-12;
omega = 2*pi*0.5;%*2;% %frequency of 0.5Hz from Stephano's movies
thi = pi/24;%pi/24;%
T_I = 0.25;



for i = 1:numcells
    for j = 2:numpoints
        %I_in(i,j) = A;
        I_in(i,j) = I_in(i,j) + (A/2)*(cos(omega*j*deltat - thi*(i-3) + pi)) + (A/2);  
        %I_in(i,j) = I_in(i,j) + (A/2)*sign(cos(omega*j*deltat - thi*(i-1))-0.5) + (A/2) - 50e-12;
        %I_in(i,j) = I_in(i,j) + (A)*max(cos(omega*j*deltat - thi*(i-1)),0);% + (A/2) + randn*variance;  
        %I_in(i,j) = (A/2)*sawtooth(omega*j*deltat - thi*(i-1)) + (A/2);% + randn*variance;  
        %I_in(i,j) = -75e-12;
       
        %these three together make a waveform like John's model produces.
        %Note however that I_in must be multiplied by -2 afterwards
        %{
        I_temp = (A/2)*sign(cos(omega*j*deltat - thi*(i-1))) + (A/2);
        dI = -I_in(i,j-1)/T_I - I_temp;
        I_in(i,j) = I_in(i,j-1) + dI*deltat;
        %}
    end
end
%I_in = -4.*I_in;

%variable initialization
for j = 1:numcells
    V(j,1) = -27.9e-3;
    Ca(j,1) = 0;
    n(j,1) = x_inf(V(j,1),Vhalf_n,k_n);
    p(j,1) = x_inf(V(j,1),Vhalf_p,k_p);
    q(j,1) = x_inf(V(j,1),Vhalf_q,k_q);
    e(j,1) = x_inf(V(j,1),Vhalf_e,k_e);
    f(j,1) = x_inf(V(j,1),Vhalf_f,k_f);
end

%start of simulation
for i = 2:numpoints
    
    for j = 2:numcells
        I_j(j,1) = g_ji * (V(j-1,i-1) - V(j,i-1)) * Gjss(V(j-1,i-1) - V(j,i-1));
    end
    
    for j = 1:numcells
        
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
        
        
        dv = -(I_in(j,i) + IKS + IKF + ICa + IL - I_j(j,1) + I_j(j+1,1))/Cmem;
        V(j,i) = V(j,i-1) + dv*deltat;
    end
    
end
%{
subplot(411),plot(xaxis,I_in(1,:).*-1e12,'r')
xlim([250 1250])
ylabel('I_{in} (pA)')
subplot(412),plot(xaxis,V(1,:).*1e3,'k')

xlim([250 1250])
ylim([-45 25])
ylabel('V_1 (mV)')
subplot(413),plot(xaxis,V(2,:).*1e3,'k')
ylim([-31 -24])
xlim([250 1250])
ylabel('V_2 (mV)')
subplot(414),plot(xaxis,V(3,:).*1e3,'k')
ylim([-28.5 -27])
xlim([250 1250])
ylabel('V_3 (mV)')
%}

%{
figure(1)
for i = 1:4
    subplot(2,2,i),plot(xaxis,V(i,:)*1e3);
    %ylim([-60 40]);
    %hold all
end
figure(2)
for i = 2:3
    subplot(2,1,i-1),plot(xaxis,Ca(i,:)./(T_Ca*thiCa*ICa_max));
    %ylim([-50 40]);
    hold all
end
%}

if g_ji == 0
    V_uncoupled = V.*1e3;
    Ca_uncoupled = Ca./(T_Ca*thiCa*ICa_max);
    'uncoupled'
else
    V_coupled = V.*1e3;
    Ca_coupled = Ca./(T_Ca*thiCa*ICa_max);
    'coupled'
end

%{
subplot(2,1,1),plot(xaxis,I_in(2,:)*-1e12,'b','LineWidth',2)
hold on
subplot(2,1,1),plot(xaxis,I_in(3,:)*-1e12,'r','LineWidth',2)
ylim([-50 (max(I_in(1,:)*-1e12) + 50)])
ylabel('I_{ in} (pA)')
legend('Muscle k','Muscle k+1','location','NorthEast')
subplot(2,1,2),plot(xaxis,V_coupled(2,:),'b','LineWidth',2)
hold on
subplot(2,1,2),plot(xaxis,V_coupled(3,:),'r','LineWidth',2)
subplot(2,1,2),plot(xaxis,V_uncoupled(2,:),'k--','LineWidth',2)
subplot(2,1,2),plot(xaxis,V_uncoupled(3,:),'k-.','LineWidth',2)
ylim([-35 25])
ylabel('V_{ mem} (mV)')
legend('Muscle k (coupled)','Muscle k+1 (coupled)','Muscle k (uncoupled)','Muscle k+1 (uncoupled)','location','NorthEast')
%}
%{
subplot(4,1,3),plot(xaxis,Ca_coupled(2,:),'b','LineWidth',2)
hold on
subplot(4,1,3),plot(xaxis,Ca_coupled(3,:),'r','LineWidth',2)
subplot(4,1,3),plot(xaxis,Ca_uncoupled(2,:),'g-.','LineWidth',2)
subplot(4,1,3),plot(xaxis,Ca_uncoupled(3,:),'y-.','LineWidth',2)
ylim([0 1])
ylabel('Normalised [Ca^{2+} ]_{i}')
legend('Muscle k (coupled)','Muscle k+1 (coupled)','Muscle k (uncoupled)','Muscle k+1 (uncoupled)','location','NorthEast')
subplot(4,1,4),plot(xaxis,Ca_coupled(2,:) - Ca_uncoupled(2,:),'b','LineWidth',2)
hold on
subplot(4,1,4),plot(xaxis,Ca_coupled(3,:) - Ca_uncoupled(3,:),'r','LineWidth',2)
ylabel('Normalised \Delta [Ca^{2+} ]_{i}')
legend('Muscle k','Muscle k+1','location','NorthEast')
%}