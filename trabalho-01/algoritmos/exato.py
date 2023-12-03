import sys
# import time
from timeit import default_timer as timer

def read_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        graph = [list(map(int, line.split())) for line in lines]
    return graph

def tsp_branch_and_bound(graph):
    n = len(graph)
    all_nodes = set(range(n))
    start_node = 0

    def calculate_lower_bound(path):
        lower_bound = 0
        for i in range(len(path) - 1):
            lower_bound += min(graph[path[i]][j] for j in all_nodes - set(path))
        return lower_bound

    def branch_and_bound_rec(path, bound):
        nonlocal best_path, min_cost

        if len(path) == n:
            cost = sum(graph[path[i]][path[i + 1]] for i in range(n - 1)) + graph[path[-1]][start_node]
            if cost < min_cost:
                min_cost = cost
                best_path = path + [start_node]

        for node in all_nodes - set(path):
            new_bound = bound + graph[path[-1]][node]
            if new_bound < min_cost:
                branch_and_bound_rec(path + [node], new_bound)

    best_path = []
    min_cost = sys.maxsize

    # start_time = time.time()  # Record the start time
    start = timer()

    branch_and_bound_rec([start_node], calculate_lower_bound([start_node]))

    # end_time = time.time()  # Record the end time
    # execution_time = end_time - start_time
    end = timer()
    execution_time = end - start

    return best_path, min_cost, execution_time

# Matriz de adjacência
adjacency_matrices_path = 'C:\\Repositorio\\algoritmos-e-estrutura-de-dados-iii\\trabalho-01\\adjacency-matrices\\'
file_name = 'tsp1_253.txt'

file_path = adjacency_matrices_path + file_name

graph = read_matrix_from_file(file_path)

result_path, result_cost, execution_time = tsp_branch_and_bound(graph)

print("Melhor caminho:", result_path)
print("Custo mínimo:", result_cost)
print("Tempo de execução:", execution_time, "segundos")