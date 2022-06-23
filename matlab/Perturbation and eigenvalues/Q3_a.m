% Gauss-Seidel
% a) Create the following n × n matrices S, U and L from the matrix J in Matlab with n ≥ 50
n=50
v =ones(1,n-1);
S = diag(v,-1) % 1: first subdiagonal
v= ones(1,50);
S = S + diag(v)*-2; % -2: diagonal
U = J
L = S
