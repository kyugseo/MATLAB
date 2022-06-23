% Compute the eigenvalues of A and compare the eigenvalues with r1, r2, ..., rn. 
% Report the observations about eigenvalues and condition number of A. 
% Compute the eigenvalues of A +(\epsilon)Qi for the 100 perturbations created in Question 1. 
% Note that these eigenvalues may be complex numbers. 
% Plot all the eigenvalues of the 100 matrices (i.e. A + Qi) on one plot by the command plot(eigenvalues, ’.’). 
% Report the plot and your observations. z^n with r_{1}, r_{2}, ..., r_{n} as its roots by the Matlab command poly.

n=50; 
r = linspace(-2,2,n);
eQi= zeros(n,n,100) % for store the Qi value in 3D array
eQiQt=zeros(n,n,100)
v =ones(1,n-1);
J = diag(v,1);
A = 4*J+4*J*J;
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


