%when A=H
A = H;
k1= cond(A,1); %1-condition number κ1
m=[]; %store e value here
for j =1:10; %this is for extracting column of B
    for k =1:10; %this is for extracting column of D
        b=B(:,j);
        d= D(:,k);
        x=A\b; %solving matrix for x
        y=A\(b+(epsilon*d));  %solving matrix for y
        e=norm(y-x,1)/(epsilon*(norm(x,1))); %calculating amplification of rel. error
        m=[m,e]; %store e values to m
    end
end
avg=mean(m)%calculating mean
med=median(m) %calculating median
maxi=max(m) %calcuating max

hold on;
figure;
x = 1:100;
ylim([10^(-3) 10^4]);
semilogy(m,'.');
y1 = yline(k1,'-','K_1(A)','LineWidth',3);
title('A = H');
ylabel('Amplification');
xlabel('Experiment');
text(65,500, {'K1(A) = 2.9070e+07', 'Average = 7.4294e+05','Median = 2.5611','Maximum = 1.4951e+07'})