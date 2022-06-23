% For n + 1 interpolation points x0, x1, ..., xn, implement the following forms of the interpolating polynomial.
% Write a Matlab function that solves the interpolation problem by the Vandermonde matrix

n = 1001;
V = zeros(n+1,n+1);
x = linspace(-1,1,n+1);
for i=1:n+1
% Set up row i.
    for j=1:n+1
    V(i,j) = x(i)^(j-1)
    end
end
