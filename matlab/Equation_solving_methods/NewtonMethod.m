%Newton's Method
clear, clc;
f = @(x) x^5-x^4+x^3-x^2+1;
fdiff = @(x) 5*x^4-4*x^3+3*x^2-2*x;
x0 = -0.5;
N = 11;
xi= x0;
fprintf('iter \t xi \t\t f(xi)\t \n');
for i=1:N
    xi = xi - f(xi)/fdiff(xi);
    
    fprintf('%5d\t%10.8f\t%10.8f \n',[i xi f(xi) ]');
    
end
