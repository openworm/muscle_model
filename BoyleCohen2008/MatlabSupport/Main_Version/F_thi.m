F = [0.25 0.5 0.75 1 1.25 1.5 1.75 2 2.25 2.5 2.75 3];
thi = (pi/24).*(0:24);

numF = max(size(F))
numthi = max(size(thi))
maxmatrix = zeros(numF,numthi);
meanmatrix = zeros(numF,numthi);

for i = 1:numF
    for j = 1:numthi
        [meanmatrix(i,j),maxmatrix(i,j)] = couplingeffect(F(i),thi(j));
    end
end

save F_thi_data.mat
