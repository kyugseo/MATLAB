T = readtable('BCCDC_COVID19_Dashboard_Case_Details.csv');

time = T(:,1);
date = unique(time);
date = table2array(date);
time = table2array(time);

c = groupsummary(table(time),1);
count = c(:,2);
count = table2array(count);

scatter(date,count)
%%%%%
title('number of incident cases in British Columbia')
xlabel("Time")
ylabel("Population")