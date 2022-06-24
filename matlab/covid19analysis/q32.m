t = 550; 
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

N = 100;
beta = 0.1;
gamma = 0.1;

S = zeros(t,1);
E = zeros(t,1);
I = zeros(t,1);
R = zeros(t,1);
New = zeros(t,1);

R(1) = 0;
I(1) = 5;
E(1) = 2*I(1);
S(1) = N-I(1)-E(1)-R(1);


for i = 2:t
    if i >=2 & i <= 28;
        R0 = 5 ;
    end
    if i >= 101 & i <= 180;
        R0 = 2.2;
    end
    if i >= 181 & i <= 220;
        R0 = 0.7;
    end
    if i >= 321 & i <= 360 ;
        R0 = 0.8;
    end
    if i >= 361 & i <= 400;
        R0 = 1.0;
    end
    if i >= 401 & i <= 550;
        R0 = 0.90;
    end
    if i >= 551;
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



