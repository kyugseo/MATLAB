n=50;
M = 2*rand(n) - 1;
[W,R] = qr(M); 
B = W*diag(r)*W';
for i = 1:100;
    C = B+eQi(:,:,i);
    D = B+eQiQt(:,:,i); 
end

ec = eig(C)
ed = eig(D)
eA = eig(A)
eB = eig(B)

