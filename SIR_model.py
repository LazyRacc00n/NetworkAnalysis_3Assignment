import matplotlib.pyplot as plt
import networkx as nx
import random
import os
class Labels:
    S = "Susceptible"
    I = "Infected"
    R = "Recovered"

    S_color = "blue" # gray forse meglio
    I_color = "red"
    R_color = "green"
    
    map_color = lambda label: Labels.S_color if label == Labels.S else Labels.I_color if label == Labels.I else Labels.R_color



class SIR:

    def __init__(self, graph, p, q, Ti, i_0, name_exp):

        if p > 1 or p < 0:
            raise ValueError(" p is a probability from 0 to 1.")

        self.p = p # the disease transmission probability

        if Ti <= 0:
            raise ValueError(" the minimum amount of time a node remains infected should be greater than zero")

        self.Ti = Ti # the minimum amount of time a node remains infected

        if q > 1 or q < 0:
            raise ValueError(" q is a probability from 0 to 1.")

        self.q = q # the recovery probability

        if i_0 > nx.number_of_nodes(graph) or i_0 < 0:
            raise ValueError(" i_0 must be higher than 0 and lower or equal than the total number of nodes.")
       
        
        self.i_0 = i_0 # number of individuals initially infected
        self.current_infected_list = [] # list of infected
        self.current_recovered_list = [] # list of recovered
        
        self.graph = graph # networkx graph
        self.graph_labelled = None # graph used to process the model (a copy of graph)

        # name of the experiment
        self.name_experiment = name_exp

        # current time in the experiment
        self.time_step = 1

        self.state_label = "state"
        self.Ti_label = "Ti"

        # save layout for draw
        self.pos = nx.kamada_kawai_layout(self.graph)

        # create the dir for the images if they not exists
        if not os.path.isdir("images"):
            os.mkdir("images")
        
        if not os.path.isdir(os.path.join("images",self.name_experiment)):
            os.mkdir(os.path.join("images", self.name_experiment))    
    
    def init_graph(self):
        # label all node of the graph as Susceptible
        self.graph_labelled = self.graph.copy()
        nx.set_node_attributes(self.graph_labelled , Labels.S, self.state_label)

        # set the Ti for each node to 0
        nx.set_node_attributes(self.graph_labelled, 0, self.Ti_label)

    def infect_initial_nodes(self):
        
        # randomly selected nodes
        infected_nodes = random.sample(list(self.graph_labelled), self.i_0)

        self.change_state(infected_nodes, Labels.I, self.Ti)

        self.current_infected_list = infected_nodes

    # plot the graph with the associated colors to the nodes...da decidere come plottare quello big
    def plot_graph(self):  
    

        # color map according to the status
        color_map = [ Labels.map_color(self.graph_labelled.nodes[node][self.state_label]) for node in self.graph_labelled]

        nx.draw(self.graph_labelled, node_color=color_map, with_labels=True, pos=self.pos)
        
        plt.savefig(os.path.join("images", self.name_experiment, str(self.time_step) + ".png"))

        plt.clf()

    # algorithm stops when all nodes are in R state
    # return true if all nodes are in state R
    def convergence_test(self):
        
        # get all nodes
        node_list = [ self.graph_labelled.nodes[node] for node in self.graph_labelled]

        # filter all nodes in state R
        filtered = list(filter(lambda node: node[self.state_label] not in [Labels.R, Labels.S]  , node_list))

        return len(filtered) == 0

    # if a minimum of TI time steps have elapsed, move the node to the compartment R with probability q
    # for nodes that are infected the T is decreased
    # return True if the node recovered
    def I_to_R(self, node):

        if self.graph_labelled.nodes[node][self.Ti_label] > 0:
            self.graph_labelled.nodes[node][self.Ti_label] -= 1
            return False
            
        # sample a random number and, if the result is less than q, move the node to the compartment R
        random_value  = random.random()

        if random_value < self.q:

            self.change_state([node], Labels.R, 0)

            return True

        return False
            

    #  look at their neighbors and spread the contagion with probability p
    def S_to_I(self, node):

        if self.graph_labelled.nodes[node][self.state_label] != Labels.I:
            return []
        
        # list of nodes that are infected
        node_list = []

        # for each neighbor of an infected node, sample a random number and
        #  if the result is less than p, a contagion occurs and the neighbor moves to the compartment I
        for neigh in self.graph_labelled.neighbors(node):

            if self.graph_labelled.nodes[neigh][self.state_label] == Labels.S:
                random_value  = random.random()

                if random_value < self.p:
                    node_list.append(neigh)

        return node_list

    # from recovered to susceptible 
    # return True if the node is now Susceptible
    #def R_to_S(self, node):

        #if self.graph_labelled.nodes[node][self.state_label] != Labels.R:
            #return False

        # transition state from R to S
        #map_attr = { node : { self.state_label : Labels.S , self.Ti_label : 0 }}        
        #nx.set_node_attributes(self.graph_labelled, map_attr)

        #return True

    # change the state into new_state and Ti into new_Ti for all node in node_list
    def change_state(self, node_list, new_state, new_Ti):

        map_attr = { node : { self.state_label : new_state , self.Ti_label : new_Ti } for node in node_list}  

        nx.set_node_attributes(self.graph_labelled, map_attr)

    
    def run(self):
        
        # init the graph
        self.init_graph()
        
        # init the nodes
        self.infect_initial_nodes()

        # plot the first time step
        self.plot_graph()
        
        self.time_step = 2
    
        
        while not self.convergence_test(): 
            
            new_recovered_list = []
            new_infected_list = []
            new_susceptible_list = []
            
            for infected in self.current_infected_list:
                is_recovered = self.I_to_R(infected)

                # if recovered it is remove from current_infected
                if is_recovered:
                    new_recovered_list.append(infected)

            # TRANSITION
            # from I to R, remove from the list
            self.change_state(new_recovered_list, Labels.R, 0)
            self.current_infected_list = list( set(self.current_infected_list) - set(new_recovered_list) )

            # the list is updated...if a node is Recovered in the previuos for cicle it cannot spread the contagion
            for infected in self.current_infected_list:
                new_infected_list  +=  self.S_to_I(infected)
                
            # Transition from R to S
            #for recovered in self.current_recovered_list:
                #is_susceptible = self.R_to_S(recovered)

                # if it's not recovered anymore it is removed from current_recovered
                #if is_susceptible:
                    #new_susceptible_list.append(recovered)

            # TRANSITIONS

            # add the new current infected
            self.current_infected_list += new_infected_list
            self.change_state(new_infected_list, Labels.I, self.Ti)

            # from R to S, remove from the list
            #self.change_state(new_susceptible_list, Labels.S, 0)
            self.current_recovered_list += new_recovered_list

            #self.current_recovered_list = list( set(self.current_recovered_list) - set(new_susceptible_list))

            # at the end of the transition...plot
            self.plot_graph()

            self.time_step = self.time_step + 1


if __name__ == "__main__":

    G = nx.karate_club_graph()

    model = SIR(G, 0.3, 0.5, 5, 2, "Exp1" )

    model.run()
   