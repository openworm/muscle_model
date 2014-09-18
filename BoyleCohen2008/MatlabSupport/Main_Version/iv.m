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