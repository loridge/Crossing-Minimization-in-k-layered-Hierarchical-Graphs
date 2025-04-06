import sys
import os
import random
import json
import copy
import time
import math
import itertools
import pandas as pd
import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from itertools import combinations, permutations
from typing import Dict, Union, List, Set
from concurrent.futures import ProcessPoolExecutor

import ctypes
import winsound

from k_layered_heuristics import (
    hybrid_1_permu_bary,
    hybrid_1_sift_bary,
    hybrid_2
)

from k_layer_crossing import (
    total_crossing_count_k_layer,
)

from k_layered import (
    generate_k_layered_sparse_graph,
    visualize_k_layered_graph,
)

# === CONFIG ===
num_samples = 20
k = 10  # number of layers
n = 8   # nodes per layer (even layer)
m = 4   # nodes per layer (odd layer)

# === Initialize result collector ===
reductions = {
    "hybrid_1_permu_bary": [],
    "hybrid_1_sift_bary": [],
}

for cutoff in range(k):
    reductions[f"hybrid_2_cutoff_{cutoff}"] = []

# === Main loop ===
for run in range(num_samples):
    nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, m)
    crossings_orig = total_crossing_count_k_layer(layers, edges)

    # --- Hybrid 1: permute + barycenter
    new_layers_hybrid_1_1 = hybrid_1_permu_bary(layers, edges)
    hybrid_1_1_crossings = total_crossing_count_k_layer(new_layers_hybrid_1_1, edges)
    percent_reduction_hybrid_1_1 = 100 * (crossings_orig - hybrid_1_1_crossings) / crossings_orig if crossings_orig else 0
    reductions["hybrid_1_permu_bary"].append(percent_reduction_hybrid_1_1)

    # --- Hybrid 1: sift + barycenter
    new_layers_hybrid_1_2 = hybrid_1_sift_bary(layers, edges)
    hybrid_1_2_crossings = total_crossing_count_k_layer(new_layers_hybrid_1_2, edges)
    percent_reduction_hybrid_1_2 = 100 * (crossings_orig - hybrid_1_2_crossings) / crossings_orig if crossings_orig else 0
    reductions["hybrid_1_sift_bary"].append(percent_reduction_hybrid_1_2)

    # --- Hybrid 2: cutoff-based
    for cutoff in range(k):
        new_layers_hybrid_2 = hybrid_2(layers, edges, cutoff)
        hybrid_2_crossings = total_crossing_count_k_layer(new_layers_hybrid_2, edges)
        percent_reduction_hybrid_2 = 100 * (crossings_orig - hybrid_2_crossings) / crossings_orig if crossings_orig else 0
        reductions[f"hybrid_2_cutoff_{cutoff}"].append(percent_reduction_hybrid_2)

# === Plot results ===
plt.figure(figsize=(14, 6))
labels = []
means = []

for key, values in reductions.items():
    labels.append(key)
    means.append(np.mean(values))

plt.bar(labels, means, color='skyblue')
plt.ylabel("Average % Crossing Reduction")
plt.xlabel("Heuristic Type")
plt.title(f"Average % Crossing Reduction of Heuristics over {num_samples} Samples")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(axis='y')
# plt.show()

plot_filename = "crossing_reduction_plot.png"
plt.savefig(plot_filename, dpi=300)  # high-res PNG
print(f"Plot saved as '{plot_filename}'.")

with open("crossing_reductions.json", "w") as f:
    json.dump(reductions, f, indent=4)

# To CSV
df = pd.DataFrame.from_dict(reductions)
df.to_csv("crossing_reductions.csv", index=False)

# Play a loud sound
winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

# Show a Windows message box
ctypes.windll.user32.MessageBoxW(
    0,
    "Your k-layered graph analysis is done!",
    "Execution Complete ✅",
    0x40  # MB_ICONINFORMATION
)