clc
f=@(x)x^5-x^4+x^3-x^2+1;
a =-1;
b = 0;
n=11
fprintf('\n Itr. No.\t a\t\t\t b \t\t\t xr')
for i=1:n
    xr=(a+b)/2;
    fprintf('\n %d \t\t %f\t %f \t %f', i,a,b,xr);
    if (f(xr)*f(b)<0)
        a=xr;
    else
        b=xr;
    end
    
end
fprintf('\n');
fprintf('\n Root of equation is =%f',xr);


