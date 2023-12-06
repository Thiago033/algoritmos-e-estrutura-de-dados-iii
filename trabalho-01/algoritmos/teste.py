import os
from pathlib import Path

# Assuming your current script is in a folder at a certain level
current_folder = os.path.dirname(__file__)

# Navigating to another folder in a different level
target_folder = os.path.join(current_folder, '..', 'adjacency-matrices')

# Getting the absolute path of the target folder
absolute_path = os.path.abspath(target_folder)

# Specify the file name
file_name = 'example.txt'

# Creating the absolute path for the text file
file_path = os.path.join(absolute_path, file_name)

print(f"The absolute path of the target folder is:\n {file_path}")