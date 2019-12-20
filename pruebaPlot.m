
t = 0:20;
x = 20*sin(t) + t.^2;
y = detrend(x,2);
plot(t,x,t,y,t,x-y,':k')
legend('Input Data','Detrended Data','Trend','Location','northwest') 
