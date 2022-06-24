%Q2- 2nd case commented part(a) , uncommented plot (b)
t = 180; 


N = 5*10^6;
alpha = 0.2;
gamma = 0.1;



S = zeros(t,1);
E = zeros(t,1);
I = zeros(t,1);
R = zeros(t,1);
New = zeros(t,1);

R(1) = 0;
I(1) = 40;
E(1) = 20*I(1);
S(1) = N-I(1)-E(1)-R(1);


for i = 2:t
    if i >=2 & i <= 20;
        R0 = 3 ;
    end
    if i >= 21 & i <= 70;
        R0 = 2.2;
    end
    if i >= 71 & i <= 84;
        R0 = 0.7;
    end
    if i >= 85 & i <= 90;
        R0 = 0.8;
    end
    if i >= 91 & i <= 110;
        R0 = 1.0;
    end
    if i >= 111 & i <= 180;
        R0 = 0.90;
    end
    if i >= 181;
        R0 = 0.5;
    end
    beta = R0 *gamma;
    
    S(i) = S(i-1) - beta*I(i-1)*S(i-1)/N;
    E(i) = E(i-1) + beta*I(i-1)*S(i-1)/N - alpha*E(i-1);
    I(i) = I(i-1) + alpha*E(i-1) - gamma*I(i-1);
    R(i) = R(i-1) + gamma*I(i-1);
    New(i) = alpha*E(i-1)*(t-1);
end
%%% 
% plot(1:t,S,'LineWidth',2)
% hold on
% plot(1:t,E,'LineWidth',2)
% hold on
% plot(1:t,I,'LineWidth',2)
% hold on
% plot(1:t,R,'LineWidth',2)
%hold on 
plot(1:t,New,'LineWidth',2)

grid on


title('incident cases with scenario two')
%legend("Susceptible","Exposed","Infected","Removed")
xlabel("Time")
ylabel("Population")