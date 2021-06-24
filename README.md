<center> <h1> Network Analysis: Assignment 3 </h1> </center>
</br>
<h5 style="text-align: right">Simone Campisi s4341240 </h5>
<h5 style="text-align: right">Jacopo Dapueto s4345255 </h5>

</br></br>
In this assignment we have mapped the **SIR model** into a network. First, the SIR model has been applied to a small network, *Karate Club Graph*, then, it is applied with a large network,*Facebook Circles*, that is the one of the other assignments.
The SIR model simplify the mathematical modeling of infectious diseases. We have 3 different states:

- **Susceptible (S)**. The healthy individuals, who have not yet contacted the virus.
- **Infectious (I)**. Contagious individuals who have contacted the virus and hence they can infects other individuals.
- **Recovered (R)**. Individuals who have recovered from the disease, not more infectious.

In this model there are several parameters:

- The **disease transmission probability p**, which defines the probability of an individual being infected.
- <img src="https://latex.codecogs.com/svg.image?\inline&space;\mathbf{T_i}"/>, which represent minimum amount of time steps, of an individual, in the state *I ( infectious)*. After these time steps, an Individual could pass from the state *I* to the state *R (recovered)* with a certain probability <img src="https://latex.codecogs.com/svg.image?\inline&space;\mathbf{q}"/>.
- The number of individual, which are infected at the beginning, <img src="https://latex.codecogs.com/svg.image?\inline&space;\mathbf{i_0}"/> .

Once all the previous parameters are set, all the nodes are initialized to *S* (no one infected ). Then, the algorithm is executed until convergence, i.e., until all the individuals are in the state *R*: for each infected node are checked the neighbors, a random number is sampled, and if the result is less than *p*, a contagion occurs and those neighbor is moved to the state I. Then, if for an infected  node, a minimum of <img src="https://latex.codecogs.com/svg.image?\inline&space;T_i"/> time steps have elapsed, it is moved to the state *R* with probability *q*.

Hence, we have plotted the model with the two types of network, testing different parameters, in order to observe the different behaviors of the model. Therefore, we plotted a graph showing the evolution of the relative number of nodes in the three states S,I,R, for each time step.
For the smaller network ( Karate Club ), we have build also a gif, which shows the evolution of the spread epidemic.

### Karate Club Graph

As already mentioned, the first network used to test the SIR model is the Karate Club graph. The model has been created with the disease transmission probability *p=0.1*, a minimum amount of time steps for the infected individuals <img src="https://latex.codecogs.com/svg.image?\inline&space;T_i&space;=&space;10"/>, the transition probability ( from I to R ) *q=0.2*, and only 1 infected individual at the beginning, <img src="https://latex.codecogs.com/svg.image?\inline&space;i_0"/>.
The graph below shows the evolution of the fraction of nodes in S,I,R. As can be seen, the number of susceptible individuals decreases rapidly, and then there is an equally rapid growth in the number of infected individuals. The curve of infected individuals, therefore, grows until it reaches a maximum peak, after which the number of infected individuals begins to decrease until it disappears. The moment this decrease begins, the number begins to increase rapidly until it reaches the total number of individuals. This is because the infected individuals gradually recover from the virus, and thus will no longer be infected. The algorithm ends when all individuals are in the R state, and thus the virus has been eradicated.
The graphic and the animation below show how the state of the nodes changes during the execution of the SIR model.
<table><tr>
<td>  <img src="./images/Karate_club/curves.png"/> </td>
<td> <img src="./images/Karate_club/gif/anim.gif"/> </td>
</tr></table>

We performed some experiments changing the parameter of the SIR model. In particular, we have taken as reference the value <img src="https://latex.codecogs.com/svg.image?\inline&space;R&space;=&space;p*k"/>, that is the **basic reproduction number**, which is the expected number of new cases caused by a single infected individual, and where *k* is the number of individuals that everyone meet, and it is obtained computing the mean degree of the network. Hence knowing the mean degree *k* and fixing R, it is possible get the probability*p*.

So, we have tested the model considering 3 different cases, R < 1, R = 1, R > 1, using this parameters:

| *R*   | *< K >*   |  *p*       |  *q*  | *i0*  | *T0*  |
|  ---  |    ---    |  ---       |  ---  |  ---  |  ---  |
| 0.45  |   4.58    | 0.015      |  0.2  |  1    |  15   |
|  1    |   4.58    | 1 / *< K >*|  0.2  |  1    |  15   |
| 1.376 |   4.58    |  0.05      |  0.2  |  1    |  15   |

- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;<&space;1}" title="\mathbf{R_0 < 1}" />. This, as showed by the graphic below, is the best case, because when *R < 1* the disease dies out faster, because we have that not all people infect one. In fact after reaching peak ( more or less the 90% of the population ) infections the contagion curve immediately starts to decrease. In this regime the epidemic is contained.

<table><tr>
<td>  <img src="./images/Karate_club_smaller_1/curves.png"/> </td>
<td> <img src="./images/Karate_club_smaller_1/gif/anim.gif"/> </td>
</tr></table>

- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;=&space;1}" title="\mathbf{R = 1}" />. This is the *endemic* regime, where, respect to the previous case, there is a fester increase of infections at the beginning, reaching quickly the 100% of individuals infected, because everyone infect one people. Respect to the previous case, the number of total infected remains at its maximum remains stable for some time steps and and doesn't immediately start to decrease.
  

<table><tr>
<td>  <img src="./images/Karate_club_equal_1/curves.png" /> </td>
<td> <img src="./images/Karate_club_equal_1/gif/anim.gif"/> </td>
</tr></table>


- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;>&space;1}" title="\mathbf{R_0 > 1}" />. This is the *epidemic* regime, and it is the worst case. Here every one infects more than one people. For this reason, we have a exponential growth, rapidly leading to the entire population becoming infected. All the population remain infected for a large amount of time steps, then the curve starts the degrowth.

<table><tr>
<td>  <img src="./images/Karate_club_greater_1/curves.png" /> </td>
<td> <img src="./images/Karate_club_greater_1/gif/anim.gif"/> </td>
</tr></table>


Looking at the three previous graphics, in the first experiment, R < 1, in order to reach the convergence of the algorithm (all the nodes in the the state *R*), were necessary run it for 45 time steps. It is the slowest case, in fact, the other cases R = 1 and R > 1, require less time steps to reach the convergence criterion, since, require less time to achieve the maximum number of the contagions ( respectively 35 and 33 time steps), and also less time in reaching all the individuals in the state *R*. So, the larger the value of R is, the faster the curve of contagions grows, infecting more people

### Facebook Circles

The model has been tested  the real network, Facebook Circles, repeating also the experiments performed with the smaller one.
Also for this network we have repeated the experiments testing the model in the 3 different cases, R < 1, R = 1, R > 1. The parameters chosen are similar to the one used for the Karate Club, in fact, are all the same except for the parameter *p*, which choice depends on *k* being much larger. The parameters are reported in the following table:

| *R*   |  *< K >*  |  *p*       |  *q*  | *i0*  | *T0*  |
|  ---  |    ---    |  ---       |  ---  |  ---  |  ---  |
| 0.655 |   43.69   |  0.015     |  0.2  |   1   |  15   |
|  1    |   43.69   | 1 / *< K >*|  0.2  |   1   |  15   |
| 2.184 |   43.69   |  0.05      |  0.2  |   1   |  15   |

</br>

- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;<&space;1}" title="\mathbf{R < 1}" />.In this case we have a not too fast growth of infections, and here we have at maximum the 60% of population infected, and after this peak the number of infections decreases rapidly, so, as in the case of the Karate club, with *R < 1* the spread epidemic is contained.

<table><tr>
<td>  <img src="./images/Facebook_R_smaller_1/curves.png" width="900" /> </td>
<td> <img src="./images/Facebook_R_smaller_1/gif/anim.gif"/> </td>
</tr></table>

- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;=&space;1}" title="\mathbf{R = 1}" />. Here, the growth of the contagion curve is a little faster than in the previous case, and reaches its peak, more or less, at 65% of the population.

<table><tr>
<td>  <img src="./images/Facebook_R_equal_1/curves.png" width="900" /> </td>
<td> <img src="./images/Facebook_R_equal_1/gif/anim.gif"/> </td>
</tr></table>

- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;>&space;1}" title="\mathbf{R > 1}" />. As in the case of the Karate Club network, this is the worst situation. In fact, observing the graphic, you can notice that the growth of the infected individuals is much faster than the previous case, reaching in few time steps, the 80% of the population infected. Also here, after the peak of the contagions the curve starts the decrease, with a consequent increase of the recovered individuals.

<table><tr>
<td>  <img src="./images/Facebook_R_greater_1/curves.png" width="900" /> </td>
<td> <img src="./images/Facebook_R_greater_1/gif/anim.gif"/> </td>
</tr></table>

Comparing these experiments with the previous of the Karate Club network, we can say that the trend of the curves, for the 3 R cases, is quite similar. Also here the number of iterations required in reaching the convergence, decrease with higher R. A clearly visible fact, is that, different network structures can be more or less conductive to the spread of a diseases. In fact, in the case of Karate Club, even with R < 1, the peak of the contagions is reached with the 90% of the population infected, and with R = 1, all the population meet the disease. Instead, with the bigger network, with R < 1, and R = 1, it is reached respectively the 60% and the 65% of the population infected. Hence, this shows how a different network structure greatly affects how, and how much, the disease is spread among people.
Also in the worst case, R > 1, with a R large enough ( more or less 2.1 ), we have a fast increase of the contagions, reaching quickly the peak, but the disease does not succeed in affecting the entire population, arriving to infect, at most, just over 80% of the population, and also this fact is due to the network structure.