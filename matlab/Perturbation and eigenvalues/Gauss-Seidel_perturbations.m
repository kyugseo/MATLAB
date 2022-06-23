% Compute the eigenvalues of A + (epsilon)Qi for the 100 perturbations created in Question 1. 
% Note that these eigenvalues may be complex numbers. Plot all the eigenvalues of the 100 matrices (i.e. A + Qi) on one plot by the command plot(eigenvalues, ’.’). 
% Report the plot and your observations.

n=50;
v =ones(1,n-1);
J = diag(v,1);
A = 4*J+4*J*J;
for i = 1:100;
    B = A+eQi(:,:,i);
    
end
condition= cond(A)
e = eig(B)
plot(e, '.')
