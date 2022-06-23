eps= 10^(-8) 
n=50;
[Q,R] = qr(randn(n,n));
eQi= zeros(n,n,100) % for store the Qi value in 3D array
eQiQt=zeros(n,n,100) % for store the Qi value in 3D array (for Q4)
for i = 1:100; %iterate 100 time
    [Q,R] = qr(randn(n,n)); %QR fact. Q is orthonormal
    QT=transpose(Q) %this is for Q4
     eQi(:,:,i) = Q*eps;
     eQiQt(:,:,i) = (Q+QT)*eps; 
end
