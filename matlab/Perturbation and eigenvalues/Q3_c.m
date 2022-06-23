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