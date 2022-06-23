%Q3_a
clear
clf

x = -1:0.01:1;
f = @(x) 1 ./ (1 + 30.*x.^2);
y = f(x)
plot(x,y,'Linewidth',1.5);
hold on

n = [10,15,25,40];
for i = 1:length(n)
    z = -1:2/n(i):1;
    y1 = 1 ./ (1 + 30.*z.^2);
    s=spline(z,y1);
    y2= spline(z,y1,x);
    plot(x,y2,'Linewidth',1.5);
    hold on
    end 


title('The equidistant with Runge Function a=30 n=10,15,25,40')
legend({'Runge','n=10','n=15','n=25','n=40'},'Location','southwest')
axis tight