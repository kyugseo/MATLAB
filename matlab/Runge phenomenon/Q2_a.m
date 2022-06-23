%Q2_a
n=1000;
x = linspace(-1,1,n);
f = @(x) 1 ./ (1 + 30.*x.^2);
y = f(x);
V=vander(x);
a = V/y;
aa=a(end:-1:1);
xx=linspace(min(x),max(x));
yy=polyval(aa,xx);                   % polyval
                                     % Input: aa -> coefficients
                                     % xx -> vector of points where polynomial is evaluated
                                     % Output: yy -> values of polynomial
plot(xx,yy)

