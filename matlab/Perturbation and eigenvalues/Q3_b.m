A= inv(L)*U; %inverse L *U 
e = eig(A) 
condition=cond(A)
plot(e, '.')
