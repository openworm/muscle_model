%Muscle arm paramaters, assuming 5 arms per cell (but only simulating one)
%and compartments of 1um length
cm = 47e-15;
rm = 950e9;
Rl = 570e3;
Rg = 66e9;
arm_length = 10e-6;
segment_length = 1e-6;
num_segs = round(arm_length/segment_length);

Istim = 100e-12;

%importing data
data = importdata('../New_Coupled/data/input.csv'); %Not sure if these are the best paramaters...

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

Vrest = -27.9e-3;

%Simulation paramaters
dt_plot = 1.0e-3;   %To avoid excessive memory requirements, the simulation and plot time steps are different
duration = 0.2;
plot_length = round(duration/dt_plot);

dt_sim = 0.01e-6;
sim_length = round(dt_plot/dt_sim) + 1;

onset = round(0.01/dt_plot);
offset = round(0.11/dt_plot);

%Variables
V_plot_L = zeros(num_segs + 1,plot_length);
V_plot_R = zeros(num_segs + 1,plot_length);
V_sim = zeros(2,num_segs + 1,sim_length);
Ca = zeros(2,sim_length);
n = zeros(2,1);
p = zeros(2,1);
q = zeros(2,1);
e = zeros(2,1);
f = zeros(2,1);
h = zeros(2,1);

Iin = zeros(2,num_segs + 1);
Iout = zeros(2,num_segs + 1);
Ic = zeros(2,num_segs + 1);
Im = zeros(2,num_segs + 1);
Irl = 0;
Inmj = zeros(2,plot_length);

Cm = zeros(1,num_segs);
Rm = zeros(1,num_segs);
Cm(1:num_segs) = cm;
Rm(1:num_segs) = rm;

xaxis = dt_plot:dt_plot:duration;

%Setup inputs
for i = onset:offset
    Inmj(1,i) = 0;
    Inmj(2,i) = Istim;
end
for i = 1:num_segs+1
    for k = 1:2
        V_sim(k,i,1) = Vrest;
    end
end
for j = 1:2
    n(j,1) = x_inf(Vrest,Vhalf_n,k_n);
    p(j,1) = x_inf(Vrest,Vhalf_p,k_p);
    q(j,1) = x_inf(Vrest,Vhalf_q,k_q);
    e(j,1) = x_inf(Vrest,Vhalf_e,k_e);
    f(j,1) = x_inf(Vrest,Vhalf_f,k_f);
end

%Start of simulation
%Start of outer loop with plot segments
for i_p = 1:plot_length
    %Start of inner loop, with simulation segments
    for i_s = 2:sim_length
        %This loop determines Iout for most compartments
        for j = 1:num_segs
            for k = 1:2
                Iout(k,j) = (V_sim(k,j,i_s-1) - V_sim(k,j+1,i_s-1))/Rl;
            end
        end
        %And Iin for most compartments
        for j = 2:num_segs + 1
            for k = 1:2
                Iin(k,j) = Iout(k,j-1);
            end
        end
        %No current flows out of last (muscle) compartment
        for k = 1:2
            Iout(k,num_segs + 1) = 0;
        end
        %This deals with gap junction current
        Irl = 5*(V_sim(1,1,i_s-1) - V_sim(2,1,i_s-1))/Rg;
        Iin(1,1) = -Irl + Inmj(1,i_p);  %NOTE we have added in the NMJ current HERE!
        Iin(2,1) = Irl + Inmj(2,i_p);
        
            
        %This loop does basic calculations for each segment
        for j = 1:num_segs           
            for k = 1:2
                Im(k,j) = (V_sim(k,j,i_s-1) - VL)/Rm(j);
                Ic(k,j) = Iin(k,j) - Iout(k,j) - Im(k,j);
                dV = Ic(k,j)/Cm(j);
                V_sim(k,j,i_s) = V_sim(k,j,i_s-1) + dV*dt_sim;
            end            
        end
        
        for k = 1:2 %here we must do the muscle body simulations
            dn = (x_inf(V_sim(k,num_segs + 1,i_s-1),Vhalf_n,k_n) - n(k,1))/T_n;
            n(k,1) = n(k,1) + dn*dt_sim;
            dp = (x_inf(V_sim(k,num_segs + 1,i_s-1),Vhalf_p,k_p) - p(k,1))/T_p;
            p(k,1) = p(k,1) + dp*dt_sim;
            dq = (x_inf(V_sim(k,num_segs + 1,i_s-1),Vhalf_q,k_q) - q(k,1))/T_q;
            q(k,1) = q(k,1) + dq*dt_sim;
            de = (x_inf(V_sim(k,num_segs + 1,i_s-1),Vhalf_e,k_e) - e(k,1))/T_e;
            e(k,1) = e(k,1) + de*dt_sim;
            df = (x_inf(V_sim(k,num_segs + 1,i_s-1),Vhalf_f,k_f) - f(k,1))/T_f;
            f(k,1) = f(k,1) + df*dt_sim;
            h(k,1) = x_inf(Ca(k,i_s-1),Cahalf_h,k_h);
        
            IKS = gKS*n(k,1)*(V_sim(k,num_segs + 1,i_s-1) - VKS);
            IKF = gKF*p(k,1)^4*q(k,1)*(V_sim(k,num_segs + 1,i_s-1) - VKF);
            ICa = gCa*e(k,1)^2*f(k,1)*(1 + (h(k,1) - 1)*alphaCa)*(V_sim(k,num_segs + 1,i_s-1) - VCa);
            IL = gL*(V_sim(k,num_segs + 1,i_s-1) - VL);
        
            dCa = -(Ca(k,i_s-1)/T_Ca + thiCa*ICa);
            Ca(k,i_s) = Ca(k,i_s-1) + dCa*dt_sim;
        
        
            dv = (Iin(k,num_segs + 1) - IKS - IKF - ICa - IL)/Cmem;
            V_sim(k,num_segs + 1,i_s) = V_sim(k,num_segs + 1,i_s-1) + dv*dt_sim;
        end
        
    end
    
    %After finishing sim segment, must copy value to plot data, and loop
    %back to beginning of simdata, to be used as initial value
    for j = 1:num_segs + 1        
        for k = 1:2
            V_sim(k,j,1) = V_sim(k,j,sim_length);
        end 
         V_plot_L(j,i_p) = V_sim(1,j,sim_length);
         V_plot_R(j,i_p) = V_sim(2,j,sim_length);            
    end
    for k = 1:2
        Ca(k,1) = Ca(k,sim_length);
    end
end


subplot(221),plot(xaxis,V_plot_L(1,:),'r')
hold on
subplot(222),plot(xaxis,V_plot_R(1,:),'r')
hold on
for j = 2:num_segs
    subplot(221),plot(xaxis,V_plot_L(j,:),'k')
    subplot(222),plot(xaxis,V_plot_R(j,:),'k')
end
subplot(221),plot(xaxis,V_plot_L(num_segs + 1,:),'b')
subplot(222),plot(xaxis,V_plot_R(num_segs + 1,:),'b')

subplot(223),plot(xaxis,Inmj(1,:),'k')
subplot(224),plot(xaxis,Inmj(2,:),'k')