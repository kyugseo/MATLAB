%Q3_c :random number
x = -2 + (1+1)*rand(1,1000)
n = [10,15,25,40];

for i = 1:length(n)
    z = -1:2/n(i):1;
    y1 = 1 ./ (1 + 30.*z.^2);
    s=spline(z,y1);
    y2= spline(z,y1,x);
    plot(x,y2,'Linewidth',1.5);
    hold on
    end 


title('The random points with Runge Function a=30 n=10,15,25,40')
legend({'Runge','n=10','n=15','n=25','n=40'},'Location','southwest')
axis tight