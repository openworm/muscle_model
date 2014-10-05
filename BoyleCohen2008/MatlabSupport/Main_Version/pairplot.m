load LRdata.mat

Vdiff_uncoupled = V_uncoupled(:,1,:) - V_uncoupled(:,2,:);
Vdiff_coupled = V_coupled(:,1,:) - V_coupled(:,2,:);

percentdiff = zeros(numruns,1);

for i = 1:numruns
    %plot(Vdiff_coupled(i,:))
    %hold all
    %plot(Vdiff_uncoupled(i,:))
    %pause(1)
    percentdiff(i) = (mean(abs(Vdiff_uncoupled(i,:))) - mean(abs(Vdiff_coupled(i,:))))/mean(abs(Vdiff_uncoupled(i,:))) * 100;
end


plot(att(2:end),percentdiff(2:end),'k*','markersize',6)
xlim([5 105])
xlabel('\delta A (%)','fontsize',12,'fontweight','demi')
ylabel('\epsilon (%)','fontsize',12,'fontweight','demi')
set(gca,'fontweight','demi')

%{
V1 = zeros(1,numpoints);
V2 = zeros(1,numpoints);
V3 = zeros(1,numpoints);
V4 = zeros(1,numpoints);

for i = 1:numpoints
V1(i) = V_uncoupled(11,1,i);
V2(i) = V_uncoupled(11,2,i);
V3(i) = V_coupled(11,1,i);
V4(i) = V_coupled(11,2,i);
end

subplot(311),plot(xaxis./1e3,I_in(1,:).*-1e12,'r','linewidth',2)
ylim([0 550])
ylabel('Iin_{Left} (pA)')
subplot(312),plot(xaxis./1e3,V3,'k','linewidth',2)
ylim([-30 20])
ylabel('V_{Left} (mV)')
subplot(313),plot(xaxis./1e3,V4,'k','linewidth',2)
%ylim([-30 20])
ylabel('V_{Right} (mV)')
xlabel('Time (s)')
%}