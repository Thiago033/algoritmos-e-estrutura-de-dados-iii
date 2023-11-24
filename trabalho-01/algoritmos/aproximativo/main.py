import numpy as np

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

# Matriz de adjacência

adjacency_matrices_path = 'C:\\Repositorio\\algoritmos-e-estrutura-de-dados-iii\\trabalho-01\\adjacency-matrices\\'
file_name = 'tsp1_253.txt'
# file_name = 'tsp2_1248.txt'
# file_name = 'tsp3_1194.txt'
# file_name = 'tsp4_7013.txt'
# file_name = 'tsp5_27603.txt'

file_path = adjacency_matrices_path + file_name

graph = read_matrix_from_file(file_path)

result_path, result_cost = nearest_neighbor(graph)

print("Melhor caminho:", result_path)
print("Custo mínimo:", result_cost)