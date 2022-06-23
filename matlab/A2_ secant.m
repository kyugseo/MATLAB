clear, clc;
f = @(x) x^5-x^4+x^3-x^2+1;
x0 = 0;
x1 = 1;
e = 10^-10;
n = 11;

for i=1:n
    x2 = (x0*f(x1)-x1*f(x0))/(f(x1)-f(x0));
    fprint('x%d = %.50f\n',i,x2)
end
