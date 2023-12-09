import numpy as np
import os
import sys
import time

def tsp(graph_distances):
    # build a graph
    G = build_graph(graph_distances)

    # build a minimum spanning tree
    MSTree = minimum_spanning_tree(G)
    
    # find odd vertexes
    odd_vertexes = find_odd_vertexes(MSTree)

    # add minimum weight matching edges to MST
    minimum_weight_matching(MSTree, G, odd_vertexes)

    # find an eulerian tour
    eulerian_tour = find_eulerian_tour(MSTree, G)

    current = eulerian_tour[0]
    path = [current]
    visited = [False] * len(eulerian_tour)
    visited[eulerian_tour[0]] = True
    length = 0

    for v in eulerian_tour:
        if not visited[v]:
            path.append(v)
            visited[v] = True

            length += G[current][v]
            current = v

    length += G[current][eulerian_tour[0]]
    path.append(eulerian_tour[0])

    return path, length

def build_graph(graph_distances):
    graph = {}
    for i in range(len(graph_distances)):
        for j in range(len(graph_distances[i])):
            if i != j:
                if i not in graph:
                    graph[i] = {}

                graph[i][j] = graph_distances[i][j]

    return graph

class UnionFind:
    def __init__(self):
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def __iter__(self):
        return iter(self.parents)

    def union(self, *objects):
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest

def minimum_spanning_tree(G):
    tree = []
    subtrees = UnionFind()
    for W, u, v in sorted((G[u][v], u, v) for u in G for v in G[u]):
        if subtrees[u] != subtrees[v]:
            tree.append((u, v, W))
            subtrees.union(u, v)

    return tree

def find_odd_vertexes(MST):
    tmp_g = {}
    vertexes = []
    for edge in MST:
        if edge[0] not in tmp_g:
            tmp_g[edge[0]] = 0

        if edge[1] not in tmp_g:
            tmp_g[edge[1]] = 0

        tmp_g[edge[0]] += 1
        tmp_g[edge[1]] += 1

    for vertex in tmp_g:
        if tmp_g[vertex] % 2 == 1:
            vertexes.append(vertex)

    return vertexes

def minimum_weight_matching(MST, G, odd_vert):
    while odd_vert:
        v = odd_vert.pop()
        length = float("inf")
        u = 1
        closest = 0
        for u in odd_vert:
            if v != u and G[v][u] < length:
                length = G[v][u]
                closest = u

        MST.append((v, closest, length))
        odd_vert.remove(closest)

def find_eulerian_tour(MatchedMSTree, G):
    # find neigbours
    neighbours = {}
    for edge in MatchedMSTree:
        if edge[0] not in neighbours:
            neighbours[edge[0]] = []

        if edge[1] not in neighbours:
            neighbours[edge[1]] = []

        neighbours[edge[0]].append(edge[1])
        neighbours[edge[1]].append(edge[0])

    # finds the hamiltonian circuit
    start_vertex = MatchedMSTree[0][0]
    EP = [neighbours[start_vertex][0]]

    while len(MatchedMSTree) > 0:
        i = 0
        v = 0
        for i, v in enumerate(EP):
            if len(neighbours[v]) > 0:
                break

        while len(neighbours[v]) > 0:
            w = neighbours[v][0]

            remove_edge_from_matchedMST(MatchedMSTree, v, w)

            del neighbours[v][(neighbours[v].index(w))]
            del neighbours[w][(neighbours[w].index(v))]

            i += 1
            EP.insert(i, w)

            v = w

    return EP

def remove_edge_from_matchedMST(MatchedMST, v1, v2):

    for i, item in enumerate(MatchedMST):
        if (item[0] == v2 and item[1] == v1) or (item[0] == v1 and item[1] == v2):
            del MatchedMST[i]

    return MatchedMST

# Function to read a matrix from a file
def read_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Converting lines from the file to a 2D array (matrix)
        matrix = [list(map(int, line.split())) for line in lines]
    return np.array(matrix)

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

    # Lendo a matriz do arquivo escolhido
    matrix = read_matrix_from_file(file_path)
    
    # Gravando o tempo de início para medição do tempo de execução
    start_time = time.time()

    # Get TSP tour and tour length
    # =======================================
    
    tsp_tour, tour_length = tsp(matrix)
    
    # =======================================

    # Gravando o tempo de término para medição do tempo de execução
    end_time = time.time()

    # Calculando o tempo de execução
    execution_time = end_time - start_time

    # Imprimindo os resultados
    print(f"Iteração {iteration + 1} - {file_name}:")
    print("Custo Mínimo:", tour_length)
    print("Tempo de Execução:", execution_time, "segundos")
    print("-" * 30)

    # Acumulando o tempo total de execução
    total_execution_time += execution_time

    # Escrevendo os resultados em um arquivo de texto para cada instância do TSP
    output_file_path = os.path.join(resultados_folder, f"results_aproximativo_{file_name[:-4]}.log")
    output_file_path2 = output_file_path
    with open(output_file_path, 'a') as output_file:
        output_file.write(f"Iteração {iteration + 1}:\n")
        output_file.write(f"Custo Mínimo: {tour_length}\n")
        output_file.write(f"Tempo de Execução: {execution_time} segundos\n")
        output_file.write("-" * 30 + "\n")

# Calcular o tempo de execução médio
average_execution_time = total_execution_time / num_iterations

# Imprimir e anexar o tempo de execução médio ao arquivo de resultados
print(f"\nTempo de Execução Médio em todas as iterações: {average_execution_time} segundos")
with open(output_file_path2, 'a') as output_file:
    output_file.write(f"\nTempo de Execução Médio em todas as iterações: {average_execution_time} segundos\n")