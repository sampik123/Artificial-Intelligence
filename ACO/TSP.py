# TSP : The goal is to find the shortest path that visits each city exactly once and returns to the starting city. 
# The distance between cities is represented as a distance matrix.


import networkx as nx                                 # To handle graph-based problems.
import numpy as np                                    # For numerical operations.
import matplotlib.pyplot as plt                       # For visualization.
import random, copy, time                             # Utilities for randomness, deep copying, and time measurement.
from scipy.spatial import distance                    # For calculating Euclidean distances.
from collections import Counter                       # To count unique paths.


start_time = time.time()

def print_matrix(m):
    for i in m:
        print(i)
    print("")


def gen_rand_coordinates(n):
    coordinates = []
    for i in range(n):
        a = random.randint(0, 2 * n)
        b = random.randint(0, 2 * n)
        if ((a, b)) not in coordinates:
            coordinates.append((a, b))

    print("\nCoordinates:", coordinates, "\n")
    return coordinates



no_of_cities = 20
no_of_ants = 40
pheromone_evaporation_level = 0.1
alpha = 4
beta = 6


coordinates = gen_rand_coordinates(no_of_cities)


distance_matrix = []


for i in range(no_of_cities):
    a = []
    for k in range(no_of_cities):
        # print(i, k, coordinates[i], coordinates[k], distance.euclidean(coordinates[i], coordinates[k]))
        a.append(int(distance.euclidean(coordinates[i], coordinates[k])))
    distance_matrix.append(a)


print("Distance Matrix")
print_matrix(distance_matrix)


G = nx.Graph()
for p in range(len(coordinates)):
    G.add_node(p, pos=[coordinates[p][0], coordinates[p][1]])
pos = nx.get_node_attributes(G, 'pos')


pheromone_level = list(np.zeros((no_of_cities, no_of_cities)))


plm = [-1, -1]
history_ant_his = []


iteration = 1
while len(plm) > 1:
    ant_history = []
    for i in range(no_of_ants):

        allowed_cites = list(range(no_of_cities))

        ant_choice = []
        distance = 0
        antchoice = 0
        ant_choice.append(antchoice)
        allowed_cites.remove(antchoice)

        prev_choice = antchoice

        while allowed_cites:

            denominator = 0

            i_node = ant_choice[len(ant_choice) - 1]

            probs = []

            # Calculate probabilities for each unvisited city
            for j_node in allowed_cites:
                prob = (pheromone_level[i_node][j_node] ** alpha) * \
                       ((1.0 / distance_matrix[i_node][j_node]) ** beta)
                probs.append(prob)
                denominator += prob

            # Normalize probabilities, avoiding division by zero
            if denominator == 0:
                # Handle the zero case by assigning equal probabilities to remaining cities
                probs = [1 / len(allowed_cites) for _ in allowed_cites]
            else:
                probs = [p / denominator for p in probs]


            if iteration == 0:
                antchoice = random.choice(allowed_cites)
            else:
                antchoice = np.random.choice(allowed_cites, p=probs)
            ant_choice.append(antchoice)
            allowed_cites.remove(antchoice)
            distance += distance_matrix[ant_choice[len(ant_choice) - 1]][ant_choice[len(ant_choice) - 2]]


        ant_choice.append(ant_choice[0])
        distance += distance_matrix[ant_choice[len(ant_choice) - 1]][ant_choice[len(ant_choice) - 2]]

        ant_history.append((ant_choice, distance))


    G_dash = copy.deepcopy(G)

    cal_edges = []

    for an in ant_history:
        path = an[0]
        for nod in range(len(path) - 1):
            if (path[nod], path[nod + 1]) and (path[nod + 1], path[nod]) not in cal_edges:
                cal_edges.append((path[nod], path[nod + 1]))
            elif (path[nod], path[nod + 1]) in cal_edges:
                cal_edges.append((path[nod], path[nod + 1]))
            else:
                cal_edges.append((path[nod + 1], path[nod]))

    weighted_edges = Counter(cal_edges)

    for pher_i in range(len(pheromone_level)):
        for pher_j in range(len(pheromone_level)):
            pheromone_level[pher_i][pher_j] = (1 - pheromone_evaporation_level) * pheromone_level[pher_i][pher_j]
            pheromone_level[pher_j][pher_i] = pheromone_level[pher_i][pher_j]

    # print_matrix(pheromone_level)

    for k in ant_history:
        l = k[1]
        path = k[0]

        for i in range(len(path) - 1):
            G_dash.add_edge(path[i], path[i + 1], weight=(weighted_edges[(path[i], path[i + 1])] + weighted_edges[(path[i + 1], path[i])]) / (no_of_ants / 4))
            pheromone_level[path[i]][path[i + 1]] += (1.0 / l)
            pheromone_level[path[i + 1]][path[i]] = pheromone_level[path[i]][path[i + 1]]

    # print_matrix(ant_history)

    history_ant_his = ant_history

    coun = []

    for ck in ant_history:
        coun.append(ck[1])

    plm = Counter(coun)

    print("Unique Paths:")
    print(len(plm))

    # Updated drawing block
    # Updated drawing block with thin lines
    if G_dash.number_of_edges() > 0:  # Ensure there are edges to plot
        weights = [G_dash[u][v]['weight'] for u, v in G_dash.edges()]  # Extract weights for styling edges

        # Draw the graph with thin lines
        nx.draw_networkx(
            G_dash,
            pos,
            node_size=300,
            width=1,               # Set edge thickness to a thin, fixed value
            edge_color='black',    # Use a visible color for edges
            node_color='orange',   # Node color for better visualization
            font_size=8            # Font size for labels
        )
    else:
        print("No edges to display in this iteration.")

    # Show the graph
    plt.title(f"Iteration {iteration}")
    plt.show()


    iteration += 1


print(history_ant_his[0])
print("Iterations:", iteration)
print("Time %s" % (time.time() - start_time))













'''
Traveling Salesman Problem (TSP):

The objective is to find the shortest route that visits all cities exactly once and returns to the starting city.
Represented using a distance matrix, where each cell indicates the distance between two cities.


Ant Colony Optimization (ACO):
A metaheuristic inspired by the behavior of real ants seeking the shortest path between their colony and food sources.


Key ACO Concepts:

Ants: Simulated agents that build solutions iteratively.

Pheromone Trails: Memory of previously taken paths; ants prefer paths with higher pheromone levels.

Evaporation: Reduces pheromone levels over time to avoid convergence to local optima.
Heuristic Information: Represents the desirability of a move (e.g., inverse of distance for TSP).

Graph Representation:
Cities are represented as nodes and distances as weighted edges in a graph.

Probability-Based Decisions:
Ants probabilistically select the next city based on pheromone levels and heuristic desirability.


'''