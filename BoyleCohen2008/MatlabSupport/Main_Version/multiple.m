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


%connectivity paramaters
g_ji = 0;%370e-12;%12.33*Cmem;             %********************       Gj    GJ     GJ    *********************



%Simulation Paramaters
deltat = 0.01e-3;
duration = 8;                %*********************      Duration    Duration   ***************
numpoints = round(duration/deltat);
numcells = 4;   
xaxis = (deltat:deltat:duration)*1e3;

%Variable Declaration
I_in = zeros(numcells,numpoints);
I_noise = zeros(numcells,numpoints);
I_j = zeros(numcells+1,1);
V = zeros(numcells,numpoints);
Ca = zeros(numcells,numpoints);
n = zeros(numcells,1);
p = zeros(numcells,1);
q = zeros(numcells,1);
e = zeros(numcells,1);
f = zeros(numcells,1);
h = zeros(numcells,1);
Psig = zeros(numcells,1);
Pnoise = zeros(numcells,1);

%input initialization
A = -100e-12;
omega = 2*pi*0.5; %frequency of 0.5Hz from Stephano's movies
thi = pi/8;
randn('seed',0);
variance = A.*0.25%[0.25 0.5 0.75 1 1.5 2];
NumVar = length(variance);
T_I = 0.25;

for k = 1:NumVar

for i = 1:numcells
    for j = 1:numpoints
        %I_in(i,j) = 45e-12;
        I_in(i,j) = I_in(i,j) + (A/2)*(cos(omega*j*deltat - thi*(i-1))) + (A/2);
        I_noise(i,j) =  + randn*variance(k);
        %I_in(i,j) = I_in(i,j) + (A/2)*sign(cos(omega*j*deltat - thi*(i-1))-0.5) + (A/2);
        %I_in(i,j) = I_in(i,j) + (A)*max(cos(omega*j*deltat - thi*(i-1)),0);% + (A/2) + randn*variance;  
        %I_in(i,j) = (A/2)*sawtooth(omega*j*deltat - thi*(i-1)) + (A/2);% + randn*variance;  
        %I_in(2,j) = -50e-12;
       
        %these three together make a waveform like John's model produces.
        %Note however that I_in must be multiplied by -2 afterwards
        %I_temp = (A/2)*sign(cos(omega*j*deltat - thi*(i-1))) + (A/2);
        %dI = -I_in(i,j-1)/T_I - I_temp;
        %I_in(i,j) = I_in(i,j-1) + dI*deltat;
        Psig(i) = Psig(i) + I_in(i,j)^2;
        Pnoise(i) = Pnoise(i) + I_noise(i,j)^2;
        
    end
    Psig(i) = Psig(i)/numpoints;
    Pnoise(i) = Pnoise(i)/numpoints;
end
variance(k)
Psig
Pnoise
SNRin_calc = Psig./Pnoise
%I_in = -4.*I_in;
for i = 1:numcells
    for j = 1:numpoints
        I_in(i,j) = I_in(i,j) + I_noise(i,j);
    end
end

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

window = 2^16;

input = downsample(I_in(2,:),100);
Voutput = downsample(V(2,:),100);
Caoutput = downsample(Ca(2,:),100);

Faxis = 1/(100*deltat) * (0:window/2)/window;
deltaF = 1/(100*deltat*window);

transform = fft(input,window);
InputSpectrum = transform.*conj(transform)/window;

transform = fft(Voutput,window);
VSpectrum = transform.*conj(transform)/window;

transform = fft(Caoutput,window);
CaSpectrum = transform.*conj(transform)/window;

subplot(311),plot(Faxis(1:length(Faxis)),InputSpectrum(1:window/2+1),'r')
subplot(312),plot(Faxis(1:length(Faxis)),VSpectrum(1:window/2+1),'k')
subplot(313),plot(Faxis(1:length(Faxis)),CaSpectrum(1:window/2+1),'b')

PsigIn = 0;
PnoiseIn = 0;
PsigV = 0;
PnoiseV = 0;
PsigCa = 0;
PnoiseCa = 0;

n = 0;

for i = 1:round(1/deltaF)
    PsigIn = PsigIn + InputSpectrum(i);
    PsigV = PsigV + VSpectrum(i);
    PsigCa = PsigCa + CaSpectrum(i);
    n = n+1;
end
PsigIn = PsigIn/n

n = 0;
for i = (round(1/deltaF)+1):length(Faxis);
    PnoiseIn = PnoiseIn + InputSpectrum(i);
    PnoiseV = PnoiseV + VSpectrum(i);
    PnoiseCa = PnoiseCa + CaSpectrum(i);
    n = n+1;
end
PnoiseIn = PnoiseIn/n

SNRin(1,k) = PsigIn/PnoiseIn
%SNRV(1,k) = PsigV/PnoiseV
%SNRCa(1,k) = PsigCa/PnoiseCa
%plot(xaxis,V(1,:)*1e3);

end

ICa_max = 6.721*Cmem;
%{
figure(1)
for i = 2:3
    subplot(2,1,i-1),plot(xaxis,V(i,:)*1e3);
    ylim([-60 40]);
    hold all
end
figure(2)
for i = 2:3
    subplot(2,1,i-1),plot(xaxis,Ca(i,:)./(T_Ca*thiCa*ICa_max));
    %ylim([-50 40]);
    hold all
end


if g_ji == 0
    V_uncoupled = V.*1e3;
    Ca_uncoupled = Ca./(T_Ca*thiCa*ICa_max);
    'uncoupled'
else
    V_coupled = V.*1e3;
    Ca_coupled = Ca./(T_Ca*thiCa*ICa_max);
    'coupled'
end
%}
%{
subplot(4,1,1),plot(xaxis,I_in(2,:)*-1e12,'k','LineWidth',2)
hold on
subplot(4,1,1),plot(xaxis,I_in(3,:)*-1e12,'k--','LineWidth',2)
ylim([-50 (max(I_in(1,:)*-1e12) + 50)])
set(gca,'FontWeight','demi')
ylabel('I_{ in} (pA)')
legend('k','k+1','location','NorthEast')
subplot(4,1,2),plot(xaxis,V_coupled(2,:),'k','LineWidth',2)
hold on
subplot(4,1,2),plot(xaxis,V_coupled(3,:),'k--','LineWidth',2)
subplot(4,1,2),plot(xaxis(1:2000:end),V_uncoupled(2,(1:2000:end)),'bo','MarkerSize',8,'LineWidth',2)
subplot(4,1,2),plot(xaxis(1:2000:end),V_uncoupled(3,(1:2000:end)),'bx','MarkerSize',8,'LineWidth',2)
ylim([-35 25])
set(gca,'FontWeight','demi')
ylabel('V_{ mem} (mV)')
legend('k (coupled)','k+1 (coupled)','k (uncoupled)','k+1 (uncoupled)','location','NorthEast')
subplot(4,1,3),plot(xaxis,Ca_coupled(2,:),'k','LineWidth',2)
hold on
subplot(4,1,3),plot(xaxis,Ca_coupled(3,:),'k--','LineWidth',2)
subplot(4,1,3),plot(xaxis(1:2000:end),Ca_uncoupled(2,1:2000:end),'bo','MarkerSize',8,'LineWidth',2)
subplot(4,1,3),plot(xaxis(1:2000:end),Ca_uncoupled(3,1:2000:end),'bx','MarkerSize',8,'LineWidth',2)
ylim([0 1])
set(gca,'FontWeight','demi')
ylabel('Normalised [Ca^{2+} ]_{i}')
legend('k (coupled)','k+1 (coupled)','k (uncoupled)','k+1 (uncoupled)','location','NorthEast')
subplot(4,1,4),plot(xaxis,Ca_coupled(2,:) - Ca_uncoupled(2,:),'k','LineWidth',2)
hold on
subplot(4,1,4),plot(xaxis,Ca_coupled(3,:) - Ca_uncoupled(3,:),'k--','LineWidth',2)
set(gca,'FontWeight','demi')
ylabel('Normalised \Delta [Ca^{2+} ]_{i}')
xlabel('Time (ms)')
%axis tight
legend('k','k+1','location','NorthEast')
%}