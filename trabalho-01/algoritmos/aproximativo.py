import numpy as np
import time
import os

def read_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        matrix = [list(map(int, line.split())) for line in lines]
    return np.array(matrix)

def nearest_neighbor(matrix):
    num_nodes = len(matrix)
    unvisited_nodes = set(range(1, num_nodes))
    current_node = 0
    tour = [current_node]
    total_cost = 0

    while unvisited_nodes:
        nearest_node = min(unvisited_nodes, key=lambda node: matrix[current_node][node])
        tour.append(nearest_node)
        total_cost += matrix[current_node][nearest_node]
        unvisited_nodes.remove(nearest_node)
        current_node = nearest_node

    tour.append(tour[0])
    total_cost += matrix[current_node][tour[0]]

    return tour, total_cost

# file_name = 'tsp1_253.txt'
file_name = 'tsp2_1248.txt'
# file_name = 'tsp3_1194.txt'
# file_name = 'tsp4_7013.txt'
# file_name = 'tsp5_27603.txt'

# Assuming your current script is in a folder at a certain level
current_folder = os.path.dirname(__file__)

# Navigating to another folder in a different level
target_folder = os.path.join(current_folder, '..', 'adjacency-matrices')

# Getting the absolute path of the target folder
absolute_path = os.path.abspath(target_folder)

# Creating the absolute path for the text file
file_path = os.path.join(absolute_path, file_name)

start_time = time.time()

graph = read_matrix_from_file(file_path)
result_path, result_cost = nearest_neighbor(graph)

end_time = time.time()
execution_time = end_time - start_time

# print("Melhor caminho:", result_path)
print("Custo mínimo:", result_cost)
print("Tempo de execução:", execution_time, "segundos")
