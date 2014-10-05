
load F_thi_data.mat;

text('interpreter','latex')

subplot(121),surface(F,thi.*(24/pi),maxmatrix')
xlabel('F ({\itHz})','fontsize',13,'fontweight','demi')
set(gca,'fontweight','demi','fontsize',11)
ylim([0 24])
ylabel('\phi (Units of (\pi / 24) rad)','fontsize',13,'fontweight','demi')
zlabel('Peak Difference (mV)','fontsize',13,'fontweight','demi')
title('A','fontsize',14,'fontweight','bold')
grid on
colormap(gray)

subplot(122),surface(F,thi.*(24/pi),meanmatrix')
xlabel('F ({\itHz})','fontsize',13,'fontweight','demi')
set(gca,'fontweight','demi','fontsize',11)
ylabel('\phi (Units of (\pi / 24) rad)','fontsize',13,'fontweight','demi')
ylim([0 24])
zlabel('Mean Difference (mV)','fontsize',13,'fontweight','demi')
title('B','fontsize',14,'fontweight','bold')
grid on
colormap(gray)