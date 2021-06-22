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

Therefore we plotted the model with the two types of network, testing different parameters, in order to observe the different behaviors of the model. Therefore, we plotted a graph showing the evolution of the relative number of nodes in the three states S,I,R, for each time step.
For the smaller network ( Karate Club ), we have build also a gif, which shows the evolution of the spread epidemic.

We performed some experiments changing the parameter of the SIR model. In particular, we have taken as reference the value <img src="https://latex.codecogs.com/svg.image?\inline&space;R&space;=&space;p*k"/>, that is the **basic reproduction number**, which is the expected number of new cases caused by a single infected individual, and where *k* is the number of individuals that everyone meet.
So, we have tested the model considering 3 different cases:

- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;<&space;1}" title="\mathbf{R_0 < 1}" />

<figure align=center>
    <img src="./images/Karate_club_smaller_1/curves.png" width="80%" height="80%">
</figure>

- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;=&space;1}" title="\mathbf{R = 1}" />
  

<figure align=center>
    <img src="./images/Karate_club_equal_1/curves.png" width="80%" height="80%" >
</figure>

- <img src="https://latex.codecogs.com/svg.image?\mathbf{R&space;>&space;1}" title="\mathbf{R_0 > 1}" />

<figure align=center>
    <img src="./images/Karate_club_greater_1/curves.png" width="80%" height="80%">
</figure>



### Karate Club Graph

As already mentioned, the first network used to test the SIR model is the Karate Club graph. The model has been created with the disease transmission probability *p=0.1*, a minimum amount of time steps for the infected individuals <img src="https://latex.codecogs.com/svg.image?\inline&space;T_i&space;=&space;10"/>, the transition probability ( from I to R ) *q=0.2*, and only 1 infected individual at the beginning, <img src="https://latex.codecogs.com/svg.image?\inline&space;i_0"/>.
The graph below shows the evolution of the fraction of nodes in S,I,R. As can be seen, the number of susceptible individuals decreases rapidly, and then there is an equally rapid growth in the number of infected individuals. The curve of infected individuals, therefore, grows until it reaches a maximum peak, after which the number of infected individuals begins to decrease until it disappears. The moment this decrease begins, the number begins to increase rapidly until it reaches the total number of individuals. This is because the infected individuals gradually recover from the virus, and thus will no longer be infected.
This algorithm ends when all individuals are in the R state, and thus the virus has been eradicated.

<figure align=center>
    <img src="./images/Karate_club/curves.png" width="80%" height="80%">
    <figcaption> <i> Figure 1 - Karate Club Graph </i> </figcaption>
</figure>

Altre cose belle

<figure align=center>
    <img src="images/Karate_club/gif/anim.gif" style="margin-left: auto; margin-right: auto;" ></img>
    <figcaption> <i> Figure 2 - Karate Club Graph, spread epidemics animation - SIR model </i> </figcaption>
</figure>


### Facebook Circles

We performed some experiments changing the parameter of the SIR model:

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