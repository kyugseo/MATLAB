% Set up and plot the Runge function f(x) = 1/{1 + a*x^2} on [−1, 1] in Matlab for a = 30.
% Report your plot.

clear
clf
n=100
z = linspace(-1,1,n);
f = @(x) 1 ./ (1 + 30.*x.^2);
plot(z,f(z))
title('The Runge Function a=30')
grid on
axis tight
