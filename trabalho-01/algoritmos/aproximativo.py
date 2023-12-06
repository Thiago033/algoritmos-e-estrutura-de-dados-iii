# Importing necessary libraries
import numpy as np
import os
import sys
import time

# Function to read a matrix from a file
def read_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Converting lines from the file to a 2D array (matrix)
        matrix = [list(map(int, line.split())) for line in lines]
    return np.array(matrix)

# Function to find the nearest neighbor solution for the Traveling Salesman Problem (TSP)
def nearest_neighbor(matrix):
    num_nodes = len(matrix)
    unvisited_nodes = set(range(1, num_nodes))
    current_node = 0
    tour = [current_node]
    total_cost = 0

    while unvisited_nodes:
        # Finding the nearest unvisited node
        nearest_node = min(unvisited_nodes, key=lambda node: matrix[current_node][node])
        tour.append(nearest_node)
        total_cost += matrix[current_node][nearest_node]
        unvisited_nodes.remove(nearest_node)
        current_node = nearest_node

    # Completing the tour by going back to the starting node
    tour.append(tour[0])
    total_cost += matrix[current_node][tour[0]]

    return tour, total_cost

# Function to let the user choose a TSP file
def choose_tsp_file():
    print("Choose a TSP file:")
    print("1. tsp1_253.txt")
    print("2. tsp2_1248.txt")
    print("3. tsp3_1194.txt")
    print("4. tsp4_7013.txt")
    print("5. tsp5_27603.txt")

    # Taking user input for the file choice
    choice = int(input("Enter the number corresponding to your choice: "))
    files = ["tsp1_253.txt", "tsp2_1248.txt", "tsp3_1194.txt", "tsp4_7013.txt", "tsp5_27603.txt"]

    # Validating the user's choice
    if 1 <= choice <= 5:
        return files[choice - 1]
    else:
        print("Invalid choice. Exiting.")
        sys.exit()

# Number of iterations
num_iterations = 50

total_execution_time = 0
output_file_path2 = 0

 # Get the chosen file name
file_name = choose_tsp_file()

# Criar a pasta de resultados se não existir
resultados_folder = os.path.join(os.path.dirname(__file__), 'resultados_aproximativo')
os.makedirs(resultados_folder, exist_ok=True)

# Loop para iterações
for iteration in range(num_iterations):
    # Assumindo que o script está em uma pasta em um certo nível
    current_folder = os.path.dirname(__file__)

    # Navegando para outra pasta em um nível diferente
    target_folder = os.path.join(current_folder, '..', 'adjacency-matrices')

    # Obtendo o caminho absoluto da pasta alvo
    absolute_path = os.path.abspath(target_folder)

    # Criando o caminho absoluto para o arquivo de texto
    file_path = os.path.join(absolute_path, file_name)

    # Gravando o tempo de início para medição do tempo de execução
    start_time = time.time()

    # Lendo a matriz do arquivo escolhido
    matrix = read_matrix_from_file(file_path)

    # Encontrando a solução do vizinho mais próximo para o TSP
    result_path, result_cost = nearest_neighbor(matrix)

    # Gravando o tempo de término para medição do tempo de execução
    end_time = time.time()

    # Calculando o tempo de execução
    execution_time = end_time - start_time

    # Imprimindo os resultados
    print(f"Iteração {iteration + 1} - {file_name}:")
    print("Custo Mínimo:", result_cost)
    print("Tempo de Execução:", execution_time, "segundos")
    print("-" * 30)

    # Acumulando o tempo total de execução
    total_execution_time += execution_time

    # Escrevendo os resultados em um arquivo de texto para cada instância do TSP
    output_file_path = os.path.join(resultados_folder, f"results_aproximativo_{file_name[:-4]}.log")
    output_file_path2 = output_file_path
    with open(output_file_path, 'a') as output_file:
        output_file.write(f"Iteração {iteration + 1}:\n")
        output_file.write(f"Custo Mínimo: {result_cost}\n")
        output_file.write(f"Tempo de Execução: {execution_time} segundos\n")
        output_file.write("-" * 30 + "\n")

# Calcular o tempo de execução médio
average_execution_time = total_execution_time / num_iterations

# Imprimir e anexar o tempo de execução médio ao arquivo de resultados
print(f"\nTempo de Execução Médio em todas as iterações: {average_execution_time} segundos")
with open(output_file_path2, 'a') as output_file:
    output_file.write(f"\nTempo de Execução Médio em todas as iterações: {average_execution_time} segundos\n")
