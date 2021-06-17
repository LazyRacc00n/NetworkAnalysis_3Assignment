import matplotlib.pyplot as plt
import networkx as nx
import random

class Labels:
    S = "Susceptible"
    I = "Infected"
    R = "Recovered"

    S_color = "blue" # gray forse meglio
    I_color = "red"
    R_color = "green"
    
    map_color = lambda label: S_color if label == S else I_color if label == I else R_color



class SIR:

    def __init__(self, graph, p, T_i, q, i_0):
       self.p = p # the disease transmission probability
       self.T_i = T_i # the minimum amount of time a node remains infected
       self.q = q # the recovery probability

       if i_0 > nx.number_of_nodes(graph) or i_0 < 0:
           raise ValueError(" i_0 must be higher than 0 and lower or equal than the total number of nodes.")
       
       self.i_0 = i_0 # number of individuals initially infected
       self.i_list = [] # list of infected
       self.graph = graph # networkx graph
       self.graph_labelled # graph used to process the model (a copy of graph)

       self.state_label = "state"
    
    # label all node of the graph as Susceptible
    def init_graph(self):
        self.graph_labelled = nx.set_node_attributes(self.graph, Labels.S, self.state_label).copy()

    def infect_initial_nodes(self):
        return 

    # plot the graph with the associated colors to the nodes...da decidere come plottare quello big
    def plot_graph(self):  
        
        color_map = [ Labels.map_color(node[self.state_label]) for node in self.graph_labelled]

        nx.draw(self.graph_labelled, node_color=color_map, with_labels=True)
        plt.show()

    # algorithm stops when all nodes are in R state
    def convergence_test(self):
        
        # if node[self.state_label] == Labels.S or node[self.state_label] == Labels.I
        node_list = [ node for node in self.graph_labelled]

        filtered = list(filter(lambda, node_list))
        return len(filtered) == 0
    
    def run(self):
        
        while True: ## Repeat the recovery / contagion until all nodes are in compartment R (e.g., Recovered / Removed)
            for infected_node in self.i_list:
                #from I to R

                #from S to I
                pass
        pass

if __name__ == "__main__":
    pass