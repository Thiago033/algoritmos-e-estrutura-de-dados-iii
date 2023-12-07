import time
import networkx as nx
from scipy.spatial.distance import euclidean
from itertools import combinations
import numpy as np

def euclidean_distance(city1, city2):
    return euclidean(city1, city2)

def generate_complete_graph(distance_matrix):
    G = nx.Graph()
    for i in range(len(distance_matrix)):
        for j in range(i + 1, len(distance_matrix[i])):
            G.add_edge(i, j, weight=distance_matrix[i][j])
    return G

def minimum_spanning_tree(graph):
    return nx.minimum_spanning_tree(graph)

def find_odd_degree_nodes(graph):
    odd_nodes = [node for node, degree in graph.degree if degree % 2 == 1]
    return odd_nodes

def minimum_matching_weight(graph, nodes):
    subgraph = graph.subgraph(nodes)
    # Find minimum weight matching using blossom algorithm
    edges = nx.algorithms.max_weight_matching(subgraph, weight='weight')
    matching_graph = nx.Graph(edges)
    return matching_graph


def eulerian_graph(spanning_tree, matching):
    eulerian_graph = nx.MultiGraph(spanning_tree)
    for edge in matching.edges:
        eulerian_graph.add_edge(*edge)
    return eulerian_graph

def eulerian_tour(graph):
    return list(nx.eulerian_circuit(graph))

def christofides_algorithm(distance_matrix):
    graph = generate_complete_graph(distance_matrix)
    spanning_tree = minimum_spanning_tree(graph)
    odd_nodes = find_odd_degree_nodes(spanning_tree)
    matching = minimum_matching_weight(graph, odd_nodes)
    eulerian = eulerian_graph(spanning_tree, matching)
    tour = eulerian_tour(eulerian)

    # Convert Eulerian tour to Hamiltonian cycle
    hamiltonian_cycle = []
    for edge in tour:
        if edge[0] not in hamiltonian_cycle:
            hamiltonian_cycle.append(edge[0])

    return hamiltonian_cycle

def minimum_matching_weight(graph, nodes):
    subgraph = graph.subgraph(nodes)
    # Find minimum weight matching using blossom algorithm
    edges = nx.algorithms.max_weight_matching(subgraph, weight='weight')
    matching = nx.Graph(edges)
    return matching

def calculate_path_cost(distance_matrix, path):
    cost = sum(distance_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1))
    # Add the cost of the last edge to complete the cycle
    cost += distance_matrix[path[-1]][path[0]]
    return cost


# Function to read a matrix from a file
def read_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Converting lines from the file to a 2D array (matrix)
        matrix = [list(map(int, line.split())) for line in lines]
    return np.array(matrix)



# Given TSP graph
# graph_distances = [
#     [0, 64, 378, 519, 434, 200],
#     [64, 0, 318, 455, 375, 164],
#     [378, 318, 0, 170, 265, 344],
#     [519, 455, 170, 0, 223, 428],
#     [434, 375, 265, 223, 0, 273],
#     [200, 164, 344, 428, 273, 0]
# ]

file_path = "/home/thiago/Repositorio/algoritmos-e-estrutura-de-dados-iii/trabalho-01/adjacency-matrices/tsp1_253.txt"
graph_distances = read_matrix_from_file(file_path)


# Function to measure the execution time
def measure_execution_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

# Run the algorithm and measure the time
result, execution_time = measure_execution_time(christofides_algorithm, graph_distances)
print("Hamiltonian Cycle:", result)

# Calculate and print the cost of the path
path_cost = calculate_path_cost(graph_distances, result)
print("Cost of the Path:", path_cost)

# Print the execution time
print("Execution Time:", execution_time, "seconds")

