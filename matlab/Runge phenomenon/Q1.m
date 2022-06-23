%Q1
clear
clf
n=100
z = linspace(-1,1,n);
f = @(x) 1 ./ (1 + 30.*x.^2);
plot(z,f(z))
title('The Runge Function a=30')
grid on
axis tight