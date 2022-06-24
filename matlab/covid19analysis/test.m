
t = 550; 


N = 1500;
alpha = 0.02;
gamma = 0.01;



S = zeros(t,1);
E = zeros(t,1);
I = zeros(t,1);
R = zeros(t,1);
New = zeros(t,1);

R(1) = 0;
I(1) = 500;
E(1) = 0.6;
S(1) = N-I(1)-E(1)-R(1);


for i = 2:t
    if i >=2 & i <= 25;
        R0 =0.00;
    end
    if i >=26 & i <= 59;
        R0 =0.02;
    end
    if i >= 101 & i <= 184;
        R0 = 0.7;
    end
    if i >= 185 & i <= 190;
        R0 = 0.8;
    end
    if i >= 191 & i <= 210;
        R0 = 1.0;
    end
    if i >= 211 & i <= 380;
        R0 = 0.90;
    end
    if i >= 381;
        R0 = 0.5;
    end
    beta = R0 *gamma;
    
    S(i) = S(i-1) - beta*I(i-1)*S(i-1)/N;
    E(i) = E(i-1) + beta*I(i-1)*S(i-1)/N - alpha*E(i-1);
    I(i) = I(i-1) + alpha*E(i-1) - gamma*I(i-1);
    R(i) = R(i-1) + gamma*I(i-1);
    New(i) = alpha*E(i-1)*(t-1);
end


plot(1:t,New,'LineWidth',2)

grid on


title('incident cases with scenario two')
%legend("Susceptible","Exposed","Infected","Removed")
xlabel("Time")
ylabel("Population")