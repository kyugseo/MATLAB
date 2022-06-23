%Q2_b

%for plot
m = 2000;
x = linspace(-1,1,m)';

%function
y =1 ./ (1 + 30.*x.^2);

%barycentric interpolation with equally spaced nodes
n = 1000;
ips = linspace(-1,1,n)';
f = 1./(1 + 30.*ips.^2);

Eq = barycentric_form(ips,f,x);


figure
plot(x,y)
hold on
plot(x,Eq)
title('2-b')
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
