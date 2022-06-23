%when A=E
A = E;
k1= cond(A,1);%1-condition number \kappa_1
k2=1/rcond(A);% estimates the reciprocal
k1 %print 
m=[]; %store e value in this array
for j=1:10; %this is for b 
    for k =1:6; % this is for C
        b = B(:,j); %extract the B column 
        C=BIGC(:,:,k); %extract k-th page
        normc=norm(C,1)%check norm(c) is 1
        x=A\b; %solve for x
        z=(A+epsilon*C)\b; %solve for z
        e=norm(z-x,1)/(epsilon*(norm(x,1)))*norm(A,1); %solve for e using given equation
        m=[m,e]; %store e value into array
    end
end
avg=mean(m)%print average value
med=median(m) %print median value
maxi=max(m) %print maximum value

hold on;
figure;
x = 1:60;
%ylim([10^(-3) 10^4]);
semilogy(m,'.');
y1 = yline(k1,'-','LineWidth',3);
y2 = yline(k2,'--r','LineWidth',2);
legend('Data','k1(A)','1/rcond(A)');
title('A = E');
xlabel('Experiment');
ylabel('Amplification');
text(35,70, {'K1(A) = 6.8296e+03','1/rcond(A)=6.8296e+03', 'Average = 950.4024','Median = 1.0359e+03','Maximum = 2.1835e+03'})