% Let A = L^(−1)U. Compute the eigenvalues of A and plot the eigenvalues. Report the plot of the eigenvalues and condition number of A. 
% There is a formula for the exact eigenvalues of A. It is known that the eigenvalues are real, and are all in the interval [0, 1]. 
% What do you observe? Is λ = 0 an eigenvalue of the matrix A?

A= inv(L)*U; %inverse L *U 
e = eig(A) 
condition=cond(A)
plot(e, '.')
