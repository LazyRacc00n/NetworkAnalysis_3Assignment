import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation, PillowWriter
import networkx as nx
import collections
from networkx.algorithms.tree.operations import join
import numpy as np
import random
import imageio
import os
import shutil
import pickle

IMAGES_FOLDER = "images"
DATA_FOLDER = "data"
MAX_NODE_DRAW = 5000


class Labels:
    S = "Susceptible"
    I = "Infected"
    R = "Recovered"

    S_color = "blue"  # gray forse meglio
    I_color = "red"
    R_color = "green"

    def map_color(
        label): return Labels.S_color if label == Labels.S else Labels.I_color if label == Labels.I else Labels.R_color


def load_dataset(sample=False, K=None):

    # if sample == True then only K randomly selected nodes are loaded

    # create graph
    G = nx.Graph()

    N = 0

    with open("dataset/facebook_combined.edges") as edges:

        for row in edges:
            if len(row.split(" ")) == 1:
                continue

            source, target = row.split(" ")[:2]
            source = int(source)
            target = int(target)

            # add nodes if not in yet
            if source not in G:
                G.add_node(source)

            if target not in G:
                G.add_node(target)

            # add edge
            G.add_edge(source, target)

        # total number of nodes
        N = nx.number_of_nodes(G)

        # remove nodes so that to mantain the graph connected (N - K nodes to remove)
        if sample:

            # deepcopy
            G_c = G.copy()

            # choose randomly node
            remove = random.sample([node for node, degree in G.degree()], N-K)
            G_c.remove_nodes_from(remove)
            G = G_c

        return G


class SIR:

    def __init__(self, graph, p, q, Ti, i_0, name_exp):

        if p > 1 or p < 0:
            raise ValueError(" p is a probability from 0 to 1.")

        self.p = p  # the disease transmission probability

        if Ti <= 0:
            raise ValueError(
                " the minimum amount of time a node remains infected should be greater than zero")

        self.Ti = Ti  # the minimum amount of time a node remains infected

        if q > 1 or q < 0:
            raise ValueError(" q is a probability from 0 to 1.")

        self.q = q  # the recovery probability

        if i_0 > nx.number_of_nodes(graph) or i_0 < 0:
            raise ValueError(
                " i_0 must be higher than 0 and lower or equal than the total number of nodes.")

        self.i_0 = i_0  # number of individuals initially infected
        self.current_infected_list = []  # list of infected
        self.current_recovered_list = []  # list of recovered

        self.graph = graph  # networkx graph
        # graph used to process the model (a copy of graph)
        self.graph_labelled = None

        # name of the experiment
        self.name_experiment = name_exp

        # current time in the experiment
        self.time_step = 0

        self.state_label = "state"
        self.Ti_label = "Ti"

        # create folders to store data
        self.create_folders()

        # save layout for draw
        if len(self.graph) < MAX_NODE_DRAW:

            if self.name_experiment.split("_")[0] == "Facebook":
                if not os.path.isfile(os.path.join(DATA_FOLDER, "Facebook_Config", "facebook_cfg.pkl")):
                    print("Starting plot configuration for " + self.name_experiment+"...")
                    pos = nx.kamada_kawai_layout(self.graph)
                    print("Configuration for " + self.name_experiment+" termianted.")
                    pickle.dump(pos, open(os.path.join(
                        DATA_FOLDER, "Facebook_Config", "facebook_cfg.pkl"), 'wb'))

            elif self.name_experiment.split("_")[0] == "Karate":
                
                if not os.path.isfile(os.path.join(DATA_FOLDER, "Karate_Club_Config", "karate_club_cfg.pkl")):
                    print("Starting plot configuration for " +
                        self.name_experiment+"...")
                    pos = nx.kamada_kawai_layout(self.graph)
                    print("Configuration for " +
                        self.name_experiment+" termianted.")
                    pickle.dump(pos, open(os.path.join(
                        DATA_FOLDER, "Karate_Club_Config", "karate_club_cfg.pkl"), 'wb'))
         

    def create_folders(self):

        if os.path.isdir(os.path.join(IMAGES_FOLDER, self.name_experiment)):
            print("Removing existing IMAGES folder of experiment: " +
                  self.name_experiment)
            shutil.rmtree(os.path.join(IMAGES_FOLDER, self.name_experiment))

        if os.path.isdir(os.path.join(DATA_FOLDER, self.name_experiment)):
            print("Removing existing DATA folder of experiment: " +
                  self.name_experiment)
            shutil.rmtree(os.path.join(DATA_FOLDER, self.name_experiment))

        # create the dir for the images if they not exists
        if not os.path.isdir(IMAGES_FOLDER):
            os.mkdir(IMAGES_FOLDER)

        if not os.path.isdir(os.path.join(IMAGES_FOLDER, self.name_experiment)):
            os.mkdir(os.path.join(IMAGES_FOLDER, self.name_experiment))

        # create the dir for the data if they not exists
        if not os.path.isdir(DATA_FOLDER):
            os.mkdir(DATA_FOLDER)

        if not os.path.isdir(os.path.join(DATA_FOLDER, self.name_experiment)):
            os.mkdir(os.path.join(DATA_FOLDER, self.name_experiment))

        if not os.path.isdir(os.path.join(DATA_FOLDER, "Facebook_Config")):
            os.mkdir(os.path.join(DATA_FOLDER, "Facebook_Config"))

        if not os.path.isdir(os.path.join(DATA_FOLDER, "Karate_Club_Config")):
            os.mkdir(os.path.join(DATA_FOLDER, "Karate_Club_Config"))

    def init_graph(self):
        # label all node of the graph as Susceptible
        self.graph_labelled = self.graph.copy()
        nx.set_node_attributes(self.graph_labelled, Labels.S, self.state_label)

        # set the Ti for each node to 0
        nx.set_node_attributes(self.graph_labelled, 0, self.Ti_label)

    def infect_initial_nodes(self):

        # randomly selected nodes
        infected_nodes = random.sample(list(self.graph_labelled), self.i_0)

        self.change_state(infected_nodes, Labels.I, self.Ti)

        self.current_infected_list = infected_nodes

    # for each time step draw the graph and save the data

    def process_time_step(self):

        # plot only  small graph
        if len(self.graph_labelled) < MAX_NODE_DRAW:
            self.plot_graph()

        # save data about time step
        self.save_time_step()

    # plot the graph with the associated colors to the nodes
    def plot_graph(self):

        # color map according to the status
        color_map = [Labels.map_color(
            self.graph_labelled.nodes[node][self.state_label]) for node in self.graph_labelled]

        if self.name_experiment.split("_")[0] == "Facebook":
            path_cfg = os.path.join(
                DATA_FOLDER, "Facebook_Config", "facebook_cfg.pkl")
        else:
            path_cfg = os.path.join(
                DATA_FOLDER, "Karate_Club_Config", "karate_club_cfg.pkl")

        with open(path_cfg, 'rb') as file:
            pos = pickle.load(file)

       
        if self.name_experiment.split("_")[0] == "Facebook":
            nx.draw(self.graph_labelled, node_color=color_map,
                        with_labels=False, pos=pos, edge_color="gray", node_size=100, width=0.5)
            
            plt.savefig(os.path.join(IMAGES_FOLDER,
                                 self.name_experiment, str(self.time_step) + ".png"), dpi=30)
        else:
            nx.draw(self.graph_labelled, node_color=color_map,
                        with_labels=False, pos=pos, edge_color="gray", width=0.5)
            
            plt.savefig(os.path.join(IMAGES_FOLDER,
                                    self.name_experiment, str(self.time_step) + ".png"))


        plt.clf()

    # save the data about a time step inside the file txt
    def save_time_step(self):

        # lines are in the form time_step,num_S,num_R,num_I

        with open(os.path.join(DATA_FOLDER, self.name_experiment, "data.txt"), "a" if self.time_step > 0 else "w") as f:

            num_I = len(self.current_infected_list)
            num_R = len(self.current_recovered_list)
            num_S = len(self.graph_labelled) - num_R - num_I

            f.write(str(self.time_step) + "," + str(num_S) +
                    "," + str(num_R) + "," + str(num_I) + "\n")

    # plot the epidemic curves
    def plot_curve(self, every_nth=5):

        plt.figure()
        # total number of nodes
        n = len(self.graph_labelled)

        time_list = []

        # list of normalized numbers
        S_list = []
        R_list = []
        I_list = []

        # read file
        with open(os.path.join(DATA_FOLDER, self.name_experiment, "data.txt"), "r") as f:

            for line in f:
                time, num_S, num_R, num_I = line.split(",")
                time_list.append(time)
                S_list.append(int(num_S)/n)
                R_list.append(int(num_R)/n)
                I_list.append(int(num_I)/n)

        # plot curves
        plt.plot(time_list, S_list,  label="Susceptible", c=Labels.S_color)
        plt.plot(time_list, R_list, label="Recovered", c=Labels.R_color)
        plt.plot(time_list, I_list, label="Infected", c=Labels.I_color)

        ax = plt.gca()

        for n, label in enumerate(ax.xaxis.get_ticklabels()):

            if n % 2 != 0:
                label.set_visible(False)

        ax.xaxis.set_ticks(ticks=list(
            np.arange(0, len(time_list)-1, every_nth)))

        plt.title(self.name_experiment)
        plt.xlabel('Time')
        plt.ylabel('Relative number of nodes')
        plt.legend()

        plt.xticks(fontsize=6)
        plt.savefig(os.path.join(IMAGES_FOLDER,
                                 self.name_experiment,  "curves.png"))

        plt.clf()

    # algorithm stops when all nodes are in R state
    # return true if all nodes are in state R

    def convergence_test(self):

        # get all nodes
        node_list = [self.graph_labelled.nodes[node]
                     for node in self.graph_labelled]

        # filter all nodes in state R
        filtered = list(filter(lambda node: node[self.state_label] not in [
                        Labels.R, Labels.S], node_list))

        return len(filtered) == 0

    # if a minimum of TI time steps have elapsed, move the node to the compartment R with probability q
    # for nodes that are infected the T is decreased
    # return True if the node recovered
    def I_to_R(self, node):

        if self.graph_labelled.nodes[node][self.state_label] != Labels.I:
            return None

        if self.graph_labelled.nodes[node][self.Ti_label] > 0:
            self.graph_labelled.nodes[node][self.Ti_label] -= 1
            return False

        # sample a random number and, if the result is less than q, move the node to the compartment R
        random_value = random.random()

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
                random_value = random.random()

                if random_value < self.p:
                    # change state
                    self.change_state([neigh], Labels.I, self.Ti)
                    node_list.append(neigh)

        return node_list

    # change the state into new_state and Ti into new_Ti for all node in node_list

    def change_state(self, node_list, new_state, new_Ti):

        map_attr = {node: {self.state_label: new_state,
                           self.Ti_label: new_Ti} for node in node_list}

        nx.set_node_attributes(self.graph_labelled, map_attr)

    def save_gif(self):
        path_images = os.path.join("images", self.name_experiment)
        img_list = os.listdir(path=path_images)

        img_list.remove("curves.png")

        try:
            img_list.remove("gif")
        except ValueError:
            os.makedirs(os.path.join(path_images, "gif"))

        img_list.sort(key=lambda x: int(x.split(".")[0]))
        images = [imageio.imread(os.path.join(path_images, img))
                  for img in img_list]
        if len(images) > 0:
            imageio.mimsave(os.path.join(path_images, "gif",
                                         "anim.gif"), images, duration=0.7)

    def run(self):

        # init the graph
        self.init_graph()

        print("SIMULATION START: " + self.name_experiment)
        
        if self.name_experiment.split("_")[0] == "Facebook":
            plt.figure(figsize=(25,25))

        # plot the time zero: no infection
        self.process_time_step()

        self.time_step += 1

        # init the nodes
        self.infect_initial_nodes()

        # plot the first time step: start the contagion
        self.process_time_step()

        self.time_step += 1

        while not self.convergence_test():

            new_recovered_list = []
            new_infected_list = []

            for infected in self.current_infected_list:
                is_recovered = self.I_to_R(infected)

                # if recovered it is remove from current_infected
                if is_recovered:
                    new_recovered_list.append(infected)

            # TRANSITION
            # from I to R, remove from the list
            self.change_state(new_recovered_list, Labels.R, 0)
            self.current_recovered_list += new_recovered_list
            self.current_infected_list = list(
                filter(lambda node: node not in new_recovered_list, self.current_infected_list))

            # the list is updated...if a node is Recovered in the previuos for cicle it cannot spread the contagion
            for infected in self.current_infected_list:
                new_infected_list += self.S_to_I(infected)

            # TRANSITIONS

            # add the new current infected
            self.current_infected_list += new_infected_list

            # at the end of the transition...plot
            self.process_time_step()

            self.time_step = self.time_step + 1

        # at the end of the simulation plot and save epidemic curve
        self.plot_curve()

        self.save_gif()
        print("SIMULATION END " + self.name_experiment)


if __name__ == "__main__":

    # experiment with karate club graph to test the code
    G = nx.karate_club_graph()
    model = SIR(G, 0.1, 0.2, 10, 1, "Karate_club")
    model.run()

    
    # expected number of links of a node
    degree = [d for n, d in G.degree()]
    degreeCount = collections.Counter(degree)
    deg, cnt = zip(*degreeCount.items())
    deg = np.array(deg)  # degree
    cnt = np.array(cnt)  # counts per degree
    k = np.average(deg, weights=cnt/cnt.sum())
    print("Expected degree: ", k)

    # R < 1
    p = 0.1
    R = k * p
    print("R = ", R)
    model = SIR(G, p, 0.2, 15, 1, "Karate_club_smaller_1")
    model.run()

    # R = 1
    p = 1/k
    R = k * p
    print("R = ", R)
    model = SIR(G, p, 0.2, 15, 1, "Karate_club_equal_1")
    model.run()

    # R > 1
    p = 0.3
    R = k * p
    print("R = ", R)
    model = SIR(G, p, 0.2, 15, 1, "Karate_club_greater_1")
    model.run()

    # experiment with facebook dataset
    G = load_dataset()

    # expected number of links of a node
    degree = [d for n, d in G.degree()]
    degreeCount = collections.Counter(degree)
    deg, cnt = zip(*degreeCount.items())
    deg = np.array(deg)  # degree
    cnt = np.array(cnt)  # counts per degree
    k = np.average(deg, weights=cnt/cnt.sum())

    print("Expected degree: ", k)

    # R < 1
    p = 0.015
    R = k * p
    print("R = ", R)
    model = SIR(G, p, 0.2, 15, 1, "Facebook_R_smaller_1")
    model.run()

    # R = 1
    p = 1/k
    R = k * p
    print("R = ", R)
    model = SIR(G, p, 0.2, 15, 1, "Facebook_R_equal_1")
    model.run()

    # R > 1
    p = 0.05
    R = k * p
    print("R = ", R)
    model = SIR(G, p, 0.2, 15, 1, "Facebook_R_greater_1")
    model.run()
    