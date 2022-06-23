%when A=E
A = E;
k1= cond(A,1); %1-condition number \kappa_1
m=[]; %store e value here
for j =1:10; %this is for extracting column of B
    for k =1:10; %this is for extracting column of D
        b=B(:,j);
        d= D(:,k);
        x=A\b; %solving matrix for x
        y=A\(b+(epsilon*d)); %solving matrix for y
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
title('A = E');
ylabel('Amplification');
xlabel('Experiment');
text(65,90, {'K1(A) = 6.8296e+03', 'Average = 258.2577','Median = 1.9622','Maximum = 3.4880e+03'})