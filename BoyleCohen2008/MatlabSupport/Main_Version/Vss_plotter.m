Iaxis = [0 20 40 60 80 100 150 200 250 300 350 400 450 500 550 600 650 700 750].*-1e-12;

numI = max(size(Iaxis))

V = zeros(1,numI);

for i = 1:numI
    V(i) = Vss(Iaxis(i));
end

plot(Iaxis.*-1e9,V.*1e3,'ko','markersize',8)
xlabel('I_{stim}  (nA)','FontSize',14,'FontWeight','demi')
ylabel('V_{ss}  (mV)','FontSize',14,'FontWeight','demi')
set(gca,'fontweight','demi','fontsize',13)
xlim([-0.05 0.8])

