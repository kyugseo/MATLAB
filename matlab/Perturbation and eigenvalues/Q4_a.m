n=50;
r = linspace(-2,2,n);
p = poly(r)
A=compan(p)
r_compare =transpose(r)
e = eig(A)

for i = 1:100;
   B = A+eQi(:,:,i);
end

e = eig(B)
condition=cond(A)
plot(e, '.')