# Importing necessary libraries
import os
import sys
import time

# Class implementing the Union-Find data structure
class UnionFind:
    def __init__(self):
        # Dictionary to store the weights of each object
        self.weights = {}
        
        # Dictionary to store the parent of each object
        self.parents = {}

    # Method to get the root of an object and perform path compression
    def __getitem__(self, object):
        # If the object is not already in the structure, initialize it as a root
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # Find the path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # Compress the path and return the root
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    # Iterator method to iterate over the parents of objects
    def __iter__(self):
        return iter(self.parents)

    # Method to perform the union of sets containing given objects
    def union(self, *objects):
        # Get the roots of the sets containing the given objects
        roots = [self[x] for x in objects]
        
        # Find the heaviest set (based on weights) among the roots
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        
        # Union operation: merge sets and update weights
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest

# Christofides algorithm to solve TSP
def christofides_tsp(graph_distances):
    # Build a graph using the given distances
    G = build_graph(graph_distances)

    # Build a minimum spanning tree using Prim's algorithm
    MSTree = minimum_spanning_tree(G)

    # Find the vertices with odd degrees in the minimum spanning tree
    odd_vertexes = find_odd_vertexes(MSTree)

    # Add minimum weight matching edges to the minimum spanning tree
    minimum_weight_matching(MSTree, G, odd_vertexes)

    # Find an Eulerian tour in the augmented graph
    eulerian_tour = find_eulerian_tour(MSTree, G)

    # Initialize variables for tracking the current node, the path, and the total length
    current = eulerian_tour[0]
    path = [current]
    visited = [False] * len(eulerian_tour)
    visited[eulerian_tour[0]] = True
    length = 0

    # Traverse the Eulerian tour to construct the final path and calculate its length
    for v in eulerian_tour:
        if not visited[v]:
            path.append(v)
            visited[v] = True

            # Update the total length with the distance between the current and next node
            length += G[current][v]
            current = v

    # Add the distance from the last node back to the starting node to complete the tour
    length += G[current][eulerian_tour[0]]
    path.append(eulerian_tour[0])

    # Return the final path and its total length
    return path, length

def build_graph(graph_distances):
    # Initialize an empty graph
    graph = {}

    # Iterate over rows in the distance matrix
    for i in range(len(graph_distances)):
        # Iterate over columns in the distance matrix
        for j in range(len(graph_distances[i])):
            # Ensure not to create edges from a node to itself
            if i != j:
                # If the starting node is not in the graph, add it
                if i not in graph:
                    graph[i] = {}

                # Add an edge from the current node (i) to the target node (j)
                # with the corresponding distance from the distance matrix
                graph[i][j] = graph_distances[i][j]

    # Return the constructed graph
    return graph

def minimum_spanning_tree(G):
    # Initialize an empty list to store the edges of the minimum spanning tree
    tree = []

    # Create a Union-Find data structure to keep track of subtrees
    subtrees = UnionFind()

    # Iterate over the sorted list of edges (sorted by weight) in the graph
    for W, u, v in sorted((G[u][v], u, v) for u in G for v in G[u]):
        # Check if adding the edge (u, v) forms a cycle in the current spanning tree
        if subtrees[u] != subtrees[v]:
            # Add the edge to the minimum spanning tree
            tree.append((u, v, W))
            
            # Merge the subtrees containing nodes u and v
            subtrees.union(u, v)

    # Return the edges of the minimum spanning tree
    return tree

def find_odd_vertexes(MST):
    # Create a temporary graph to count the degree of each vertex
    tmp_g = {}
    
    # List to store vertices with odd degrees
    vertexes = []

    # Iterate over each edge in the minimum spanning tree
    for edge in MST:
        # Update the degree of each vertex in the temporary graph
        if edge[0] not in tmp_g:
            tmp_g[edge[0]] = 0

        if edge[1] not in tmp_g:
            tmp_g[edge[1]] = 0

        tmp_g[edge[0]] += 1
        tmp_g[edge[1]] += 1

    # Check for vertices with odd degrees and add them to the list
    for vertex in tmp_g:
        if tmp_g[vertex] % 2 == 1:
            vertexes.append(vertex)

    # Return the list of vertices with odd degrees
    return vertexes

def minimum_weight_matching(MST, G, odd_vert):
    # Iterate until there are vertices with odd degrees
    while odd_vert:
        # Pop a vertex with an odd degree
        v = odd_vert.pop()
        
        # Initialize variables for tracking the length, closest vertex, and a dummy variable
        length = float("inf")
        closest = 0
        
        # Iterate over remaining odd vertices to find the closest neighbor
        for u in odd_vert:
            # Ensure v and u are distinct and find the minimum weight edge
            if v != u and G[v][u] < length:
                length = G[v][u]
                closest = u

        # Add the minimum weight matching edge to the minimum spanning tree
        MST.append((v, closest, length))
        
        # Remove the closest vertex from the set of odd vertices
        odd_vert.remove(closest)

def find_eulerian_tour(MatchedMSTree, G):
    # Create a dictionary to store neighbors for each vertex
    neighbours = {}
    
    # Iterate over edges in the matched minimum spanning tree
    for edge in MatchedMSTree:
        # Initialize neighbor lists for each vertex
        if edge[0] not in neighbours:
            neighbours[edge[0]] = []

        if edge[1] not in neighbours:
            neighbours[edge[1]] = []

        # Add each vertex to the neighbor list of the other
        neighbours[edge[0]].append(edge[1])
        neighbours[edge[1]].append(edge[0])

    # Initialize the Eulerian path with the starting vertex
    start_vertex = MatchedMSTree[0][0]
    EP = [neighbours[start_vertex][0]]

    # Iterate until all edges in the matched minimum spanning tree are used
    while len(MatchedMSTree) > 0:
        i = 0
        v = 0

        # Find the first vertex in the Eulerian path with remaining neighbors
        for i, v in enumerate(EP):
            if len(neighbours[v]) > 0:
                break

        # Extend the Eulerian path by removing matched edges
        while len(neighbours[v]) > 0:
            w = neighbours[v][0]

            # Remove the edge from the matched minimum spanning tree
            remove_edge_from_matchedMST(MatchedMSTree, v, w)

            # Remove vertices from each other's neighbor lists
            del neighbours[v][(neighbours[v].index(w))]
            del neighbours[w][(neighbours[w].index(v))]

            i += 1
            EP.insert(i, w)

            v = w

    # Return the Eulerian path
    return EP

def remove_edge_from_matchedMST(MatchedMST, v1, v2):
    # Iterate over edges in the matched minimum spanning tree
    for i, item in enumerate(MatchedMST):
        # Check if the edge connects v1 and v2 or v2 and v1
        if (item[0] == v2 and item[1] == v1) or (item[0] == v1 and item[1] == v2):
            # Remove the edge from the matched minimum spanning tree
            del MatchedMST[i]

    # Return the updated matched minimum spanning tree
    return MatchedMST

# Function to read a matrix from a file
def read_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Converting lines from the file to a 2D array (graph)
        graph = [list(map(int, line.split())) for line in lines]
    return graph

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
num_iterations = 1000

total_execution_time = 0
results_file_name = ""

# Get the chosen file name
file_name = choose_tsp_file()

# Create the results folder if it does not exist
results_folder = os.path.join(os.path.dirname(__file__), 'approximate_results')
os.makedirs(results_folder, exist_ok=True)

# Loop for iterations
for iteration in range(num_iterations):
    current_folder = os.path.dirname(__file__)
    target_folder = os.path.join(current_folder, '..', 'adjacency-matrices')
    absolute_path = os.path.abspath(target_folder)

    # Creating the absolute path for the text file
    file_path = os.path.join(absolute_path, file_name)

    # Reading the matrix from the chosen file
    matrix = read_matrix_from_file(file_path)
    
    # Recording the start time for execution time measurement
    start_time = time.time()

    # Get TSP tour and tour length
    tsp_tour, tour_length = christofides_tsp(matrix)

    # Recording the end time for execution time measurement
    end_time = time.time()

    # Calculating the execution time
    execution_time = end_time - start_time

    # Printing the results
    print(f"Iteration {iteration + 1} - {file_name}:")
    print("Minimum Cost:", tour_length)
    print("Execution Time:", execution_time, "seconds")
    print("-" * 30)
    
    # Accumulating the total execution time
    total_execution_time += execution_time

    # Writing the results to a text file for each instance of the TSP
    output_file_path = os.path.join(results_folder, f"results_approximate_{file_name[:-4]}.log")
    results_file_name = output_file_path
    
    with open(output_file_path, 'a') as output_file:
        output_file.write(f"Iteration {iteration + 1}:\n")
        output_file.write(f"Minimum Cost: {tour_length}\n")
        output_file.write(f"Execution Time: {execution_time} seconds\n")
        output_file.write("-" * 30 + "\n")

# Calculate the average execution time
average_execution_time = total_execution_time / num_iterations

# Print and append the average execution time to the results file
print(f"\nAverage Execution Time across all iterations: {average_execution_time} seconds")
with open(results_file_name, 'a') as output_file:
    output_file.write(f"\nAverage Execution Time across all iterations: {average_execution_time} seconds\n")
