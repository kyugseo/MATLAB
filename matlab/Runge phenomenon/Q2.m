n = 1001;
V = zeros(n+1,n+1);
x = linspace(-1,1,n+1);
for i=1:n+1
% Set up row i.
    for j=1:n+1
    V(i,j) = x(i)^(j-1);
    end
end
