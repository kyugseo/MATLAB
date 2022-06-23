n=50; % in this case n = 50
v =ones(1,n-1);  
J = diag(v,1); % one on the first super diagonal
A = 4*J;
for i = 1:100; %100 iterations
    B = A+eQi(:,:,i); %eQi from Q1
    
end
condition= cond(A) %condition number
e = eig(B) %eigenvalue
plot(e,'.') %plot eigenval