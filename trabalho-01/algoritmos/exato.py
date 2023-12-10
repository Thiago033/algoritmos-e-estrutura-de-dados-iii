# Importing necessary libraries
import os
import sys
import time

# Function to solve the Traveling Salesman Problem using Brute Force algorithm
def tsp_brute_force(graph):
    # Get the number of nodes in the graph
    n = len(graph)
    
    # Create a set of all nodes in the graph
    all_nodes = set(range(n))
    
    # Define the starting node for the TSP
    start_node = 0

    # Recursive function to explore all possible paths
    def brute_force_rec(path):
        nonlocal best_path, min_cost

        # If the current path includes all nodes
        if len(path) == n:
            # Calculate the cost of the complete path
            cost = sum(graph[path[i]][path[i + 1]] for i in range(n - 1)) + graph[path[-1]][start_node]
            
            # Update the best path and minimum cost if the current path is better
            if cost < min_cost:
                min_cost = cost
                best_path = path + [start_node]

        # Recursively explore paths by adding one node at a time
        for node in all_nodes - set(path):
            brute_force_rec(path + [node])

    # Initialize variables to store the best path, minimum cost, and execution time
    best_path = []
    min_cost = sys.maxsize  # Assume an initial high cost
    
    # Record the start time for execution time measurement
    start_time = time.time()

    # Start the Brute Force algorithm with the initial path containing only the starting node
    brute_force_rec([start_node])

    # Record the end time for execution time measurement
    end_time = time.time()
    
    # Calculate the execution time
    execution_time = end_time - start_time

    # Return the best path, minimum cost, and execution time
    return best_path, min_cost, execution_time

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
num_iterations = 1

total_execution_time = 0
results_file_name = ""

# Get the chosen file name
file_name = choose_tsp_file()

# Create the results folder if it does not exist
results_folder = os.path.join(os.path.dirname(__file__), 'exact_results')
os.makedirs(results_folder, exist_ok=True)

# Loop for iterations
for iteration in range(num_iterations):
    current_folder = os.path.dirname(__file__)
    target_folder = os.path.join(current_folder, '..', 'adjacency-matrices')
    absolute_path = os.path.abspath(target_folder)

    # Creating the absolute path for the text file
    file_path = os.path.join(absolute_path, file_name)

    # Reading the matrix from the chosen file
    graph = read_matrix_from_file(file_path)

    # Applying the Brute Force algorithm to solve the TSP
    result_path, result_cost, execution_time = tsp_brute_force(graph)

    # Printing the results
    print(f"Iteration {iteration + 1} - {file_name}:")
    print("Minimum Cost:", result_cost)
    print("Execution Time:", execution_time, "seconds")
    print("-" * 30)
    
    # Accumulating the total execution time
    total_execution_time += execution_time

    # Writing the results to a text file for each instance of the TSP
    output_file_path = os.path.join(results_folder, f"exact_results_{file_name[:-4]}.log")
    results_file_name = output_file_path
    
    with open(output_file_path, 'a') as output_file:
        output_file.write(f"Iteration {iteration + 1}:\n")
        output_file.write(f"Minimum Cost: {result_cost}\n")
        output_file.write(f"Execution Time: {execution_time} seconds\n")
        output_file.write("-" * 30 + "\n")

# Calculate the average execution time
average_execution_time = total_execution_time / num_iterations

# Print and append the average execution time to the results file
print(f"\nAverage Execution Time across all iterations: {average_execution_time} seconds")
with open(results_file_name, 'a') as output_file:
    output_file.write(f"\nAverage Execution Time across all iterations: {average_execution_time} seconds\n")
