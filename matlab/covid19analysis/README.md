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
1. Write [Matlab code](https://github.com/kyugseo/Programming/blob/cbd302b59700e1301cafcbd182f57e64a0f65811/matlab/covid19analysis/SEIR.m) to solve the SEIR equation
2. Run the code with the following parameters and initial conditions for t = 180 days and report a [plot](https://github.com/kyugseo/Programming/blob/cbd302b59700e1301cafcbd182f57e64a0f65811/matlab/covid19analysis/Q1.jpg) of the S, E, I, R curves.
