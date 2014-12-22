
%importing data
data = importdata('data/input.csv'); %Not sure if these are the best paramaters...

% Model paramaters

Cmem = 30e-12;
gKS = data(2)*Cmem;
gKF = data(3)*Cmem;
gCa = data(4)*Cmem;
gL = data(5)*Cmem;
VKS = data(6);
VKF = data(7);
VCa = data(8);
VL = 10e-3;
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

x = (-60:0.1:80).*1e-3;
numpoints = length(x);
y = zeros(3,numpoints);

for i = 1:numpoints
    IKF = gKF*x_inf(x(i),Vhalf_p,k_p)^4*x_inf(x(i),Vhalf_q,k_q)*(x(i) - VKF);
    IKS = gKS*x_inf(x(i),Vhalf_n,k_n)*(x(i) - VKS);
    ICa = gCa*x_inf(x(i),Vhalf_e,k_e)^2*(x(i) - VCa);
   
    
    y(1,i) = IKF + IKS;
    y(2,i) = ICa;
    y(3,i) = y(1,i) + y(2,i);
end

subplot(122),plot(x*1e3,y(1,:)/Cmem,'k')
hold on
grid on
xlabel('V_{ mem} (mV)')
ylabel('IK (A/F)')
xlim([-70 50])
ylim([-5 40])
subplot(121),plot(x*1e3,y(2,:)/Cmem,'k')
hold on
grid on
xlabel('V_{ mem} (mV)')
ylabel('ICa (A/F)')
xlim([-40 80])
ylim([-8 6])
%plot(x*1e3,y(2,:)/Cmem,'k')