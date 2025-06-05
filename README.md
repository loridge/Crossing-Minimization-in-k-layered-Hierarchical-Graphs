# Crossing-Minimization-in-k-layered-Hierarchical-Graphs

An undergraduate thesis project for CS 198/199 under the Algorithms and Complexity Laboratory - UP Diliman. 

Abstract: 

Minimizing edge crossings in graph drawings is crucial for improving readability in applications such as circuit schematics and transportation maps. One important variant is the `k-layered hierarchical crossing minimization` problem, which seeks optimal vertex orderings across all layers of a k-layered graph to reduce edge crossings. In this study, we explore a hybrid layer-by-layer approach that combines two one-sided bipartite crossing minimization (OSCM) heuristics, specifically, barycenter, permutation, and sifting algorithms. These heuristics are applied above and below a specified `cut-off index`, effectively dividing the graph into upper and lower regions. 

Using Python and the `NetworkX` library, we implemented six hybrid cut-off algorithms and tested them on sparse k-layered graphs with ten (10) layers, layer widths $b = 7$ and $b = 8$, and edge counts defined as $|E| = 2 \cdot (k - 1) \cdot b$. We evaluated each method in terms of empirical approximation ratio (EAR), the ratio of the heuristic solution to a baseline solution, and computational time. Results demonstrate a clear trade-off: heuristics with higher solution quality generally incur higher computational cost. For time-sensitive applications, faster hybrids like `bary_sift` and `sift_bary` are preferable, whereas `permu_sift` and `sift_permu` are more suitable when solution quality is prioritized. Our findings suggest that selecting the appropriate hybrid and cut-off value is key to balancing performance and efficiency.

## How to run the code
To run a Python file, make sure that the current working directory is the directory of the Python file.

Then, run `python filename.py` in the terminal


## Required dependencies/libraries
To run the files, you need to have the latest version of [Python](https://www.python.org/downloads/) installed on your system.

To install the libraries: run `pip install -r requirements.txt` in the topmost directory, in the terminal.
- NetworkX: For graph generation and graph utility functions
- Pandas: For data processing
- Numpy: For data processing 
- Matplotlib: For data visualization

## Naming Conventions

### File naming convention:
- snake case (e.g. crossing_util.py, cross.py)

### Element naming conventions:
- variables, package names, functions: snake_case
- classes: CamelCase
- constants: UPPERCASE

## Brief description of file structure and purpose


## Scripts for data preprocessing, training, evaluation, and visualization
Some of the code that do data postprocessing and visualization are found within the files that execute experiments or in adjacent Python files.

## Configuration files (e.g., .json, .yaml, .ini) for reproducibility
No configuration files are relevant. 