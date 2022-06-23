A=H8; %when A=H8
AINV=inv(A); %inverse of matrix (A)
I = eye(8,8); %8X8 identity matrix 
M = A*AINV-I;
AC=inv(AINV);
N = AC-A;
P = AINV - HI8;
answer1=norm(M,1)%compute ||A ∗ AINV − I||1 %normalized 
answer2=norm(N,1)%compute ||AC − A||1 %normalized
answer3=norm(P,1)%compute ||AINV - HI||1 %normalized
k1H8=cond(H8,1) %1-condition number \kappa_1