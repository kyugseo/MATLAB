## A simplified COVID-19 model

The so-called SEIR model is a standard way to model the spread of infectious diseases. It is an example of a compartmental model. We will look at this model in its most basic form, and solve it numerically for various parameters.
The population of N individuals is assigned to different compartments, and individuals can move between compartments. The SEIR model uses four compartments, S, E, I, R, representing segments of the population, so S + E + I + R = N (a simplification, meaning the total population is constant, with some leeway in interpreting the term “total population”).

 * S. Susceptible individuals. Those are healthy, and not immune individuals who may become infected upon contact with an infected individual.
 
 * E. Exposed individuals. These are individuals who have been infected, but because of the incubation period of the virus are not yet infectious themselves. They will     transition to the infected group;
 
 * I. Infected individuals. These are individuals who have been infected, and can pass on the infection to susceptible individuals.
 
 * R. Removed individuals. (In an optimistic scenario referred to as recovered individuals.) These include people who have recovered and are now immune, and people who     have deceased.


Note that for Covid-19, it is still not clear yet whether recovered people are immune to the virus and its variants, and if so, by how much and for how long. 

## DATA
[BCCDC_COVID19](https://github.com/kyugseo/Programming/blob/cbd302b59700e1301cafcbd182f57e64a0f65811/matlab/covid19analysis/BCCDC_COVID19_Dashboard_Case_Details.csv)

## Implementation
1. Write [Matlab code](https://github.com/kyugseo/Programming/blob/cbd302b59700e1301cafcbd182f57e64a0f65811/matlab/covid19analysis/SEIR.m) to solve the SEIR equation.

2. Run the code with the following parameters and initial conditions for t = 180 days and report a plot of the S, E, I, R curves.
![plot](https://github.com/kyugseo/Programming/blob/cbd302b59700e1301cafcbd182f57e64a0f65811/matlab/covid19analysis/Q1.jpg)

3. Plot the curve for the number of incident cases with [code](https://github.com/kyugseo/Programming/blob/8d5c4a63488dfda70ad4347bde4bd9dd401d511c/matlab/covid19analysis/q1c.m).
![plot](https://github.com/kyugseo/Programming/blob/8d5c4a63488dfda70ad4347bde4bd9dd401d511c/matlab/covid19analysis/Q1c.jpg)

## Time-dependent parameters

We could model the effect of intervention (e.g. social distancing) with data for R0 as follows
(three scenarios are given): ![](https://github.com/kyugseo/Programming/blob/cdee0443e8f4b4ec10d05227fa98c20b9ed7d1b5/matlab/covid19analysis/Scenarios.png)

Let R0 = R0(t), hence, β = β(t) be the time-dependent parameter. According to the model, β is the contact rate, which can be controlled. If we all stayed in a remote log cabin by ourselves, β = R0 = 0; if we practice physical distancing and wear masks when physical distancing is not possible, then R0 might stay below 1; if we hang
out in bars or at large gatherings, then β and R0 will go through the roof – leading to large numbers of Is, infected and infectious people.

![alt-text-1](https://github.com/kyugseo/Programming/blob/e4bfcbded44e747e9c68e36297ef933f6d128edc/matlab/covid19analysis/Q2-1.jpg "title-1") ![alt-text-2](https://github.com/kyugseo/Programming/blob/e4bfcbded44e747e9c68e36297ef933f6d128edc/matlab/covid19analysis/Q2-1n.jpg "title-2")
