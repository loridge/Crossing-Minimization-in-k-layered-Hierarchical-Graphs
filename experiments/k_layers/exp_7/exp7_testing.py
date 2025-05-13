
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from k_layered_heuristics import (
    hybrid_1_permu_bary,
    permu_multi_sweep,
    permu_multi_sweep_patarasuk
)

from k_layer_crossing import (
    total_crossing_count_k_layer,
)

from k_layered import (
    generate_k_layered_sparse_graph,
    visualize_k_layered_graph
)

# Parameters
m_values = [4, 5, 6, 7, 8]         # Number of vertices m
num_samples = 1             # Number of trials per m
k = 10                       # Number of layers
n = 8                        # Number of vertices n
m = 4

#  m = 4
nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, 4)
visualize_k_layered_graph(G, layers, "Initial Graph, m = 4")
print("Initial crossings:", total_crossing_count_k_layer(layers, edges))

# Run Hybrid 1
new_layers_hybrid = hybrid_1_permu_bary(layers, edges)
crossings_hybrid = total_crossing_count_k_layer(new_layers_hybrid, edges)
visualize_k_layered_graph(G, new_layers_hybrid, "Hybrid 1 Permutation Barycenter")
print("Hybrid 1 crossings:", crossings_hybrid)


# Run Full Permutation (Patarasuk)
new_layers_full = permu_multi_sweep_patarasuk(layers, edges)
crossings_full = total_crossing_count_k_layer(new_layers_full, edges)
visualize_k_layered_graph(G, new_layers_full, "Full Permutation (Patarasuk)")
print("Full Permutation crossings:", crossings_full)

print("#### ------------------------------------------- ####")
#  m = 8
nodes_L, edges_L, G_L, layers_L = generate_k_layered_sparse_graph(k, n, 8)
visualize_k_layered_graph(G_L, layers_L, "Initial Graph, m = 8")
print("Inital crossings:", total_crossing_count_k_layer(layers_L, edges_L))

# Run Hybrid 1
new_layers_hybrid = hybrid_1_permu_bary(layers_L, edges_L)
crossings_hybrid = total_crossing_count_k_layer(new_layers_hybrid, edges_L)
visualize_k_layered_graph(G_L, new_layers_hybrid, "Hybrid 1 Permutation Barycenter")
print("Hybrid 1 crossings:", crossings_hybrid)


# Run Full Permutation (Patarasuk)
new_layers_full = permu_multi_sweep_patarasuk(layers_L, edges_L)
crossings_full = total_crossing_count_k_layer(new_layers_full, edges_L)
visualize_k_layered_graph(G_L, new_layers_full, "Full Permutation (Patarasuk)")
print("Full Permutation crossings:", crossings_full)


