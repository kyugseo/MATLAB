A=E; %when A=E
AINV=inv(A); %inverse of matrix (A)
I = eye(6,6); %6X6identity matrix 
M = A*AINV-I; 
AC=inv(AINV); 
N = AC-A;

answer1=norm(M,1)%compute ||A ∗ AINV − I||1 %normalized 
answer2=norm(N,1)%compute ||AC − A||1 %normalized