import networkx as nx
import random

class Labels:
    S = "Susceptible"
    I = "Infected"
    R = "Recovered"

    S_color = "blue"
    I_color = "red"
    R_color = "green"



class SIR:

    def __init__(self, graph, p, Ti, q):
       self.p = p # the disease transmission probability
       self.Ti = Ti # the minimum amount of time a node remains infected
       self.q = q # the recovery probability
       self.i_0 = 0

       self.graph = graph # networkx graph
    
    # label all node of the graph as Susceptible
    def init_graph(self):

        

        return 
    
    def method2(self):
        pass

if __name__ == "__main__":
    pass