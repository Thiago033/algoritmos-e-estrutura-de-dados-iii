# Importing necessary libraries
import os
import sys
import time

iter = 0

# Function to read a matrix from a file
def read_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Converting lines from the file to a 2D array (graph)
        graph = [list(map(int, line.split())) for line in lines]
    return graph

# Function to solve the Traveling Salesman Problem using Brute Force algorithm
def tsp_brute_force(graph):
    global iter
    n = len(graph)
    all_nodes = set(range(n))
    start_node = 0

    # Recursive function for the Brute Force algorithm
    def brute_force_rec(path):
        global iter
        nonlocal best_path, min_cost

        if len(path) == n:
            # Calculate the cost of the complete path
            cost = sum(graph[path[i]][path[i + 1]] for i in range(n - 1)) + graph[path[-1]][start_node]
            if cost < min_cost:
                min_cost = cost
                best_path = path + [start_node]

        for node in all_nodes - set(path):
            # print("Best Path: ", best_path)
            
            # Print the current path
            if iter % 1000000 == 0:
                print("Current cost:", min_cost)
            
            # print(iter)
            iter += 1
            brute_force_rec(path + [node])

    best_path = []
    min_cost = sys.maxsize

    # Recording the start time for execution time measurement
    start_time = time.time()

    # Start the Brute Force algorithm with the initial path
    brute_force_rec([start_node])

    # Recording the end time for execution time measurement
    end_time = time.time()
    execution_time = end_time - start_time

    return best_path, min_cost, execution_time

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
num_iterations = 1
total_execution_time = 0
results_file_name = 0

# Get the chosen file name
file_name = choose_tsp_file()

# Criar a pasta de resultados se não existir
resultados_folder = os.path.join(os.path.dirname(__file__), 'resultados_exato')
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

    # Lendo a matriz do arquivo escolhido
    graph = read_matrix_from_file(file_path)

    # Aplicando o algoritmo Brute Force para resolver o TSP
    result_path, result_cost, execution_time = tsp_brute_force(graph)

    # Imprimindo os resultados
    print(f"Iteração {iteration + 1} - {file_name}:")
    print("Custo Mínimo:", result_cost)
    print("Tempo de Execução:", execution_time, "segundos")
    print("-" * 30)

    # Acumulando o tempo total de execução
    total_execution_time += execution_time

    # Escrevendo os resultados em um arquivo de texto para cada instância do TSP
    output_file_path = os.path.join(resultados_folder, f"results_exato_{file_name[:-4]}.log")
    results_file_name = output_file_path

    with open(output_file_path, 'a') as output_file:
        output_file.write(f"Iteração {iteration + 1}:\n")
        output_file.write(f"Custo Mínimo: {result_cost}\n")
        output_file.write(f"Tempo de Execução: {execution_time} segundos\n")
        output_file.write("-" * 30 + "\n")

# Calcular o tempo de execução médio
average_execution_time = total_execution_time / num_iterations

# Imprimir e anexar o tempo de execução médio ao arquivo de resultados
print(f"\nTempo de Execução Médio em todas as iterações: {average_execution_time} segundos")
print("Total iteracoes na funcao: ", iter)
with open(results_file_name, 'a') as output_file:
    output_file.write(f"\nTempo de Execução Médio em todas as iterações: {average_execution_time} segundos\n")
