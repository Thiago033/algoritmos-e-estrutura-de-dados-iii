import os
from pathlib import Path


# Matriz de adjacência
adjacency_matrices_path = '/home/thiago/Repositorio/algoritmos-e-estrutura-de-dados-iii/trabalho-01/adjacency-matrices/'

file_name = '\\tsp1_253.txt'
# file_name = 'tsp2_1248.txt'
# file_name = 'tsp3_1194.txt'
# file_name = 'tsp4_7013.txt'
# file_name = 'tsp5_27603.txt'

file_path = adjacency_matrices_path + file_name

print("path 1:")
print(file_path)

print("path 2:")
print(Path().absolute().parent)
