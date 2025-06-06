# Crossing-Minimization-in-k-layered-Hierarchical-Graphs

An undergraduate thesis project for CS 198/199 2024-2025 under the Algorithms and Complexity Laboratory - UP Diliman. 
| Researchers                  | Advisers                        |
|-----------------------------|----------------------------------|
| Loridge Anne A. Gacho            | Asst Prof. Nestine Hope S. Hernandez |
| Zandrew Peter C. Garais       | Asst Prof. Jhoirene B. Clemente               |

## Abstract

Minimizing edge crossings in graph drawings is crucial for improving readability in applications such as circuit schematics and transportation maps. One important variant is the `k-layered hierarchical crossing minimization` problem, which seeks optimal vertex orderings across all layers of a k-layered graph to reduce edge crossings. In this study, we explore a hybrid layer-by-layer approach that combines two one-sided bipartite crossing minimization (OSCM) heuristics, specifically, barycenter, permutation, and sifting algorithms. These heuristics are applied above and below a specified `cut-off index`, effectively dividing the graph into upper and lower regions. 

Using Python and the `NetworkX` library, we implemented six hybrid cut-off algorithms and tested them on sparse k-layered graphs with ten (10) layers, layer widths $b = 7$ and $b = 8$, and edge counts defined as $|E| = 2 \cdot (k - 1) \cdot b$. We evaluated each method in terms of empirical approximation ratio (EAR), the ratio of the heuristic solution to a baseline solution, and computational time. Results demonstrate a clear trade-off: heuristics with higher solution quality generally incur higher computational cost. For time-sensitive applications, faster hybrids like `bary_sift` and `sift_bary` are preferable, whereas `permu_sift` and `sift_permu` are more suitable when solution quality is prioritized. Our findings suggest that selecting the appropriate hybrid and cut-off value is key to balancing performance and efficiency.

## How to run the code
To run a Python file, make sure that the current working directory is the directory of the Python file.

Then, run `python filename.py` in the terminal


## Required dependencies/libraries
To run the files, you need to have the latest version of [Python](https://www.python.org/downloads/) installed on your system.

It is recommended that the Python programs be run in a Python virtual environment, so that packages may not conflict with the Python libraries installed globally. However, this is not required. This can be set up as follows:

1. Run the command `python -m venv venv` in the main folder.
2. To run the virtual environment, run the command `/venv/Scripts/activate`

Once the virtual environment is active, to install the libraries, run `pip install -r requirements.txt` in the topmost directory, in the terminal.
- NetworkX: For graph generation and graph utility functions.
- Pandas: For data processing.
- Numpy: For data processing. 
- Matplotlib: For data visualization.

## Naming Conventions

### File naming convention:
- snake case (e.g. crossing_util.py, cross.py)

### Element naming conventions:
- variables, package names, functions: snake_case
- classes: CamelCase
- constants: UPPERCASE

## Brief description of file structure and purpose

The project tree is structured below. Result files and unused files are omitted for brevity.  

```bash
.
├── LICENSE
├── README.md
├── experiments
│   ├── 2_layers
│   │   ├── deprecated_feature_testing
│   │   ├── exp_1
│   │   │   ├── 2_layer_exp_parallel.py
│   │   │   ├── exp1_v1_v2_sparse.ipynb
│   │   │   └── exp1_v1_v2_sparse_helper.py
│   │   ├── exp_1-2-3_results
│   │   │   ├── README.md
│   │   │   ├── exp_1
│   │   │   ├── exp_2
│   │   │   ├── exp_3
│   │   │   └── unused
│   │   ├── exp_2
│   │   │   ├── exp2_increasing_density.ipynb
│   │   │   ├── summary_to_graphs.py
│   │   │   └── summary_to_tabular.py
│   │   ├── exp_3
│   │   │   └── exp3_parallel_9.py
│   │   ├── exp_3_final_results
│   │   ├── exp_4
│   │   │   └── exp4_n-m_20.py
│   │   ├── exp_4_results
│   │   │   ├── exp4_n-m_1
│   │   │   │   └── visualize_mid_density_results_n10.py
│   │   │   └── exp4_n-m_20
│   │   ├── old_heuristic_visualization_test
│   │   ├── slurm_logs
│   │   └── unused
│   ├── experiments.md
│   └── k_layers
│       ├── __init___.py
│       ├── animated_k_layer
│       ├── exp_5
│       │   ├── exp_5_boxplot.py
│       │   ├── exp_5_result_raw
│       │   ├── exp_5_result_visuals
│       │   └── experiment_5.py
│       ├── exp_6
│       │   └── experiment_6.py
│       ├── exp_7
│       │   ├── exp7_4-6-8_test_results
│       │   ├── exp7_test_results
│       │   ├── experiment_7.py
│       │   ├── final_exp7_results
│       │   └── init_exp7_results
│       ├── exp_8
│       │   ├── experiment8.py
│       │   ├── inherit.py
│       ├── exp_9
│       │   ├── exp_9.md
│       │   ├── experiment9.py
│       │   ├── networkx_to_json
│       │   ├── result-2-2-20
│       │   ├── result-3-3-20
│       │   ├── result-8-8-20
│       │   ├── result-8-8-20-Copy1
│       │   └── some_slurm_hpc_stale_logs
│       ├── hybrid_algorithms.py
│       ├── k_layer_crossing.py
│       ├── k_layered.py
│       ├── k_layered_heuristics.py
│       └── unused
│           ├── README.md
└── two_layer_functions
    ├── README.md
    ├── __init__.py
    ├── bipartite_graph_generator.py
    ├── crossing_func.py
    ├── crossing_utils.py
    ├── sifting_2.py
    ├── sifting_util2.py
    ├── two_layer_barycenter.py
    ├── unused
    └── visualize_test.py
```
### Folder: two_layer_functions
The folder `two_layer_functions` contain the necessary functions that are used for other functions and code in the two-layer and k-layer crossing minimization sectors. It includes crossing minimization heuristics, graph visualizers, and graph generators. The most notable files and some of the relevant functions within are outlined below:

- two_layer_barycenter.py
  - sss

### Folder: experiments
This folder generally contains all the code for the experimental setups (either used or not in the final paper) and the file of their results. It is divided into two parts: `2_layers` and `k_layers`. 

#### 2_layers

#### k_layers

## Scripts for data preprocessing, training, evaluation, and visualization
Some of the code that do data postprocessing and visualization are found within the files that execute experiments or in adjacent Python files.

## Configuration files (e.g., .json, .yaml, .ini) for reproducibility
No configuration files are relevant. 
