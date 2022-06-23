% Generate n equally spaced points r1, r2, ..., rn on the interval [−2, 2] in Matlab with the command linspace. 
% Find the polynomial p(z) = c_{0} + c_{1}z + · · · c_{n−1}z^{n−1} + z^n with r_{1}, r_{2}, ..., r_{n} as its roots by the Matlab command poly.
   
n=50; 
r = linspace(-2,2,n);  %generate n numbers  interval [−2, 2]
p = poly(r) 
A=compan(p)
r_compare =transpose(r)
e = eig(A)
eQi= zeros(n,n,100)
for i = 1:100;
   B = A+eQi(:,:,i);
end

e = eig(B)
condition=cond(A)
plot(e, '.')
