%Muscle arm paramaters, assuming 5 arms per cell (but only simulating one)
%and compartments of 1um length
cm = 47e-15;
rm = 950e9;
Rl = 570e3;
Rg = 66e9;
arm_length = 10e-6;
segment_length = 1e-6;
num_segs = round(arm_length/segment_length);

Istim = 10e-12;

%Muscle body paramaters
Cbody = 30e-12;
Rbody = 1.5e9;%100e6;%

%Simulation paramaters
dt_plot = 1.0e-3;   %To avoid excessive memory requirements, the simulation and plot time steps are different
duration = 0.3;
plot_length = round(duration/dt_plot);

dt_sim = 0.01e-6;
sim_length = round(dt_plot/dt_sim) + 1;

onset = round(0.1/dt_plot);
offset = round(0.2/dt_plot);

%Variables
V_plot_L = zeros(num_segs + 1,plot_length);
V_plot_R = zeros(num_segs + 1,plot_length);
V_sim = zeros(2,num_segs + 1,sim_length);

Iin = zeros(2,num_segs + 1);
Iout = zeros(2,num_segs + 1);
Ic = zeros(2,num_segs + 1);
Im = zeros(2,num_segs + 1);
Irl = 0;
Inmj = zeros(2,plot_length);

Cm = zeros(1,num_segs + 1);
Rm = zeros(1,num_segs + 1);
Cm(1:num_segs) = cm;
Cm(num_segs + 1) = Cbody;
Rm(1:num_segs) = rm;
Rm(num_segs + 1) = Rbody;

xaxis = dt_plot:dt_plot:duration;

%Setup inputs
for i = onset:offset
    Inmj(1,i) = 0;
    Inmj(2,i) = Istim;
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
        Irl = (V_sim(1,1,i_s-1) - V_sim(2,1,i_s-1))/Rg;
        Iin(1,1) = -Irl + Inmj(1,i_p);  %NOTE we have added in the NMJ current HERE!
        Iin(2,1) = Irl + Inmj(2,i_p);
        
            
        %This loop does basic calculations for each segment
        for j = 1:num_segs + 1           
            for k = 1:2
                Im(k,j) = V_sim(k,j,i_s-1)/Rm(j);
                Ic(k,j) = Iin(k,j) - Iout(k,j) - Im(k,j);
                dV = Ic(k,j)/Cm(j);
                V_sim(k,j,i_s) = V_sim(k,j,i_s-1) + dV*dt_sim;
            end            
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
end

%{
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
%}