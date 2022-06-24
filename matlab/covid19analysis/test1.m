%Q4

%(a)

T = readtable('BCCDC_COVID19_Dashboard_Case_Details.csv');

time = T(:,1);
date = unique(time);
date = table2array(date);
time = table2array(time);

c = groupsummary(table(time),1);
count = c(:,2);
count = table2array(count);
scatter(date,count)
hold on

%(b)
t = 500; 


N = 200000;
alpha = 0.2;
gamma = 0.02;



S = zeros(t,1);
E = zeros(t,1);
I = zeros(t,1);
R = zeros(t,1);
New = zeros(t,1);

R(1) = 0;
I(1) = 40;
E(1) = 0*I(1);
S(1) = N-I(1)-E(1)-R(1);


for i = 2:t
    if i >=2 & i <= 12;
        R0 = 0.0;
    end
    if i >= 13 & i <= 22;
        R0 = 0.3;
    end
    if i >= 23 & i <= 109;
        R0 = 0.3;
    end
    if i >= 110 & i <= 156;
        R0 = 0.7;
    end
    if i >= 157 & i <= 212;
        R0 = 1.4;
    end
    if i >= 212 & i <= 271;
        R0 = 2.6;
    end
    if i >= 272 & i  <= 349;
        R0 = 1.1;
    end
    if i >= 350 & i <= 404;
        R0 = 1.72;
    end
    if i >= 405 & i <= 423;
        R0 = 0.7;
    end
    if i >= 423 & i <= 491;
        R0 = 0.2;
    end
    if i >= 493
        R0 = 1.12;
    end
    beta = R0 *gamma;
    
    S(i) = S(i-1) - beta*I(i-1)*S(i-1)/N;
    E(i) = E(i-1) + beta*I(i-1)*S(i-1)/N - alpha*E(i-1);
    I(i) = I(i-1) + alpha*E(i-1) - gamma*I(i-1);
    R(i) = R(i-1) + gamma*I(i-1);
    New(i) = alpha*E(i-1)*(t-1);
end

% plot(1:t,S,'LineWidth',2)
% hold on
% plot(1:t,E,'LineWidth',2)
% hold on
% plot(1:t,I,'LineWidth',2)
% hold on
% plot(1:t,R,'LineWidth',2)
plot(40:t+39,New,'LineWidth',2)
%35:t+34
grid on


title('Incident cases and Model')
legend("New cases","Model")
xlabel("Time")
ylabel("Population")