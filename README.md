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
The graph below shows the evolution of the fraction of nodes in S,I,R. As can be seen, the number of susceptible individuals decreases rapidly, and then there is an equally rapid growth in the number of infected individuals. The curve of infected individuals, therefore, grows until it reaches a maximum peak, after which the number of infected individuals begins to decrease until it disappears. The moment this decrease begins, the number begins to increase rapidly until it reaches the total number of individuals. This is because the infected individuals gradually recover from the virus, and thus will no longer be infected.
This algorithm ends when all individuals are in the R state, and thus the virus has been eradicated.

<figure align=center>
    <img src="images/Karate_club_smaller_1/curves.png" width="80%" height="80%">
    <figcaption> <i> Figure 1 - Karate Club Graph </i> </figcaption>
</figure>

The gif below shows the evolution of the spread epidemic in the Karate Club network.

<figure align=center>
    <img src="images/Karate_club/gif/anim.gif" style="margin-left: auto; margin-right: auto;" ></img>
    <figcaption> <i> Figure 2 - Karate Club Graph, spread epidemics animation - SIR model </i> </figcaption>
</figure>

We performed some experiments changing the parameter of the SIR model. In particular, we have taken as reference the value <img src="https://latex.codecogs.com/svg.image?\inline&space;R&space;=&space;p*k"/>, that is the **basic reproduction number**, which is the expected number of new cases caused by a single infected individual, and where *k* is the number of individuals that everyone meet, and it is obtained computing the mean degree of the network. Hence knowing the mean degree *k* and fixing R, it is possible get the probability*p*.

So, we have tested the model considering 3 different cases, R < 1, R = 1, R > 1, using this parameters:

| *R*   | *K*   |  *p*   |  *q*  | *i0*  | *T0*  |
|  ---  |  ---  |  ---   |  ---  |  ---  |  ---  |
| 0.45  | 4.58  | 0.015  |  0.2  |  1    |  15   |
|  1    | 4.58  | 1/4.58 |  0.2  |  1    |  15   |
| 1.376 | 4.58  |  0.05  |  0.2  |  1    |  15   |

- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;<&space;1}" title="\mathbf{R_0 < 1}" />. This, as showed by the graphic below, is the best case, because when *R < 1* the disease dies out faster, because we have that not all people infect one. In fact after reaching peak ( more or less the 90% of the population ) infections the contagion curve immediately starts to decrease. In this regime the epidemic is contained.

<figure align=center>
    <img src="./images/Karate_club_smaller_1/curves.png" width="80%" height="80%">
</figure>

- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;=&space;1}" title="\mathbf{R = 1}" />. This is the *endemic* regime, where, respect to the previous case, there is a fester increase of infections at the beginning, reaching quickly the 100% of individuals infected, because everyone infect one people. Respect to the previous case, the number of total infected remains at its maximum remains stable for some time steps and and doesn't immediately start to decrease.
  
<figure align=center>
    <img src="./images/Karate_club_equal_1/curves.png" width="80%" height="80%" >
</figure>

- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;>&space;1}" title="\mathbf{R_0 > 1}" />. This is the *epidemic* regime, and it is the worst case. Here every one infects more than one people. For this reason, we have a exponential growth, rapidly leading to the entire population becoming infected. All the population remain infected for a large amount of time steps, then the curve starts the degrowth.

<figure align=center>
    <img src="./images/Karate_club_greater_1/curves.png" width="80%" height="80%">
</figure>

### Facebook Circles

The model has been tested in the real network, Facebook Circles, repeating also the experiments performed with the smaller one. The evolution of the spread epidemic, in this kind of network, is showed in the below animation



- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;=&space;1}" title="\mathbf{R_0 = 1}" />

<figure align=center>
    <img src="./images/Facebook_R_equal_1/curves.png" width="80%" height="80%" >
</figure>

- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;>&space;1}" title="\mathbf{R_0 > 1}" />

<figure align=center>
    <img src="./images/Facebook_R_greater_1/curves.png" width="80%" height="80%">
</figure>

- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;<&space;1}" title="\mathbf{R_0 < 1}" />

<figure align=center>
    <img src="./images/Facebook_R_smaller_1/curves.png" width="80%" height="80%">

</figure>