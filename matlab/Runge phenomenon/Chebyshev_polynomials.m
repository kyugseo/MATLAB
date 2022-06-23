% Set the interpolation points to be Chebyshev on [−1, 1], and n = 10, 15, 25, 40. 
% Plot the four polynomials (with respect to the four values of n) together with the Runge function. 
% Observe the results and report your plots and observations.

clear
clf
m = 2000;
x = linspace(-1,1,m)';

n = [10,15,25,40]


for i = 1:4;
    angles = linspace(0,pi,n(i))';
    ips = cos(angles);
    f = 1./(1 + 30.*ips.^2);
    Cheby = barycentric_form(ips,f,x);
    plot(x,Cheby,'Linewidth',1.5)
    hold on
end 


title('The  Chebyshev with Runge Function a=30 n=10,15,25,40')
legend({'n=10','n=15','n=25','n=40'},'Location','southwest')
axis tight

%% barycentric form
function p = barycentric_form(ips,f,x)

n = size(ips,1);
m = size(x,1);

w = ones(n,1);

for i = 1:n
    
    for k = 1:n
        
        if i ~= k
            w(i) = w(i)*(ips(i)-ips(k));
        end
        
    end
    
    w(i) = 1/w(i);
    
end

numer = zeros(m,1);
denom = zeros(m,1);

for i = 1:n
    
    numer = numer + f(i)*w(i)./(x-ips(i));
    denom = denom + w(i)./(x-ips(i));
    
end

p = numer./denom;

end
