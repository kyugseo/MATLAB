
t = 180; 

R0 = 2.5;
N = 5*10^6;
alpha = 0.2;
gamma = 0.1;
beta = R0 *gamma;


S = zeros(t,1);
E = zeros(t,1);
I = zeros(t,1);
R = zeros(t,1);

R(1) = 0;
I(1) = 40;
E(1) = 20*I(1);
S(1) = N-I(1)-E(1)-R(1);

for i = 2:t
    S(i) = S(i-1) - beta*I(i-1)*S(i-1)/N;
    E(i) = E(i-1) + beta*I(i-1)*S(i-1)/N - alpha*E(i-1);
    I(i) = I(i-1) + alpha*E(i-1) - gamma*I(i-1);
    R(i) = R(i-1) + gamma*I(i-1);
    
end

plot(1:t,S,'LineWidth',2)
hold on
plot(1:t,E,'LineWidth',2)
hold on
plot(1:t,I,'LineWidth',2)
hold on
plot(1:t,R,'LineWidth',2)
grid on


title('SEIR')
legend("Susceptible","Exposed","Infected","Removed")
xlabel("Time")
ylabel("Population")