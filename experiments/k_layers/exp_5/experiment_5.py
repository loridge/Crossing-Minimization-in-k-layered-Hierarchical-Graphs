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


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from k_layered_heuristics import (
    hybrid_1_permu_bary,
    hybrid_2,
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
k = 10  
n = 8   
m = 4   

# === Initialize result collector ===
reductions = {
    "hybrid_1_permu_bary": [],
}

for cutoff in range(k):
    reductions[f"hybrid_2_cutoff_{cutoff}"] = []

# === Time collector ===
timings = {
    "hybrid_1_permu_bary": [],
}
for cutoff in range(k):
    timings[f"hybrid_2_cutoff_{cutoff}"] = []
    
# === Main loop ===
for run in range(num_samples):
    nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, m)
    crossings_orig = total_crossing_count_k_layer(layers, edges)

    # --- Hybrid 1: permute + barycenter
    start_time = time.perf_counter()
    new_layers_hybrid_1_1 = hybrid_1_permu_bary(layers, edges)
    end_time = time.perf_counter()
    timings["hybrid_1_permu_bary"].append(end_time - start_time)

    hybrid_1_1_crossings = total_crossing_count_k_layer(new_layers_hybrid_1_1, edges)
    percent_reduction_hybrid_1_1 = 100 * (crossings_orig - hybrid_1_1_crossings) / crossings_orig if crossings_orig else 0
    reductions["hybrid_1_permu_bary"].append(percent_reduction_hybrid_1_1)

    # --- Hybrid 2: cutoff-based
    for cutoff in range(k):
        start_time = time.perf_counter()
        new_layers_hybrid_2 = hybrid_2(layers, edges, cutoff)
        end_time = time.perf_counter()
        timings[f"hybrid_2_cutoff_{cutoff}"].append(end_time - start_time)

        hybrid_2_crossings = total_crossing_count_k_layer(new_layers_hybrid_2, edges)
        percent_reduction_hybrid_2 = 100 * (crossings_orig - hybrid_2_crossings) / crossings_orig if crossings_orig else 0
        reductions[f"hybrid_2_cutoff_{cutoff}"].append(percent_reduction_hybrid_2)
        

# === Bar Plot results ===
plt.figure(figsize=(14, 8))
labels = []
means = []

for key, values in reductions.items():
    labels.append(key)
    means.append(np.mean(values))

plt.bar(labels, means, color='skyblue')
plt.ylabel("Average % Crossing Reduction")
plt.xlabel("Heuristic Type")
# Main title (higher up)
plt.suptitle(f"Experiment 5: Average % Crossing Reduction of Hybrid Algorithms over {num_samples} samples", fontsize = 15)

# Subtitle just below main title, above plot
plt.title(f"n = {n}, m = {m}, k = {k} Sparse k-layered graphs", fontsize=13, y=1.01)


plt.xticks(rotation=45, ha='right')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.grid(axis='y')

plot_filename = "exp_5_bar_plot.png"
plt.savefig(plot_filename, dpi=300)  # high-res PNG
print(f"Plot saved as '{plot_filename}'.")

# === Boxplot version of results ===
plt.figure(figsize=(14, 6))

# Prepare data and labels
data = [values for values in reductions.values()]
labels = [key for key in reductions.keys()]

# Create boxplot
plt.boxplot(data, labels=labels, patch_artist=True,
            boxprops=dict(facecolor='lightblue', color='blue'),
            medianprops=dict(color='red'),
            whiskerprops=dict(color='gray'),
            capprops=dict(color='gray'),
            flierprops=dict(markerfacecolor='orange', marker='o', markersize=5, linestyle='none'))

plt.ylabel("Crossing Reduction (%)")
plt.xlabel("Heuristic Type")
plt.title(f"Exp 5:Distribution of % Crossing Reduction Across {num_samples} Samples")
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the boxplot
boxplot_filename = "exp_5_boxplot.png"
plt.savefig(boxplot_filename, dpi=300)
print(f"Boxplot saved as '{boxplot_filename}'.")

# To JSON
with open("exp_5_bar_plot.json", "w") as f:
    json.dump(reductions, f, indent=4)

# To CSV
df = pd.DataFrame.from_dict(reductions)
df.to_csv("exp_5_bar_plot.csv", index=False)


# === Timing Bar Plot with Error Bars ===
plt.figure(figsize=(14, 8))
labels = []
avg_times = []
std_times = []

for key, values in timings.items():
    labels.append(key)
    avg_times.append(np.mean(values))
    std_times.append(np.std(values))

plt.bar(labels, avg_times, yerr=std_times, capsize=5, color='lightgreen', edgecolor='black')
plt.ylabel("Average Execution Time (seconds)")
plt.xlabel("Heuristic Type")
plt.suptitle("Experiment 5: Average Execution Time of Hybrid Algorithms", fontsize=15)
plt.title(f"n = {n}, m = {m}, k = {k} Sparse k-layered graphs", fontsize=13, y=1.01)
plt.xticks(rotation=45, ha='right')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save timing plot
timeplot_filename = "exp_5_time_bar_plot.png"
plt.savefig(timeplot_filename, dpi=300)

# To JSON
with open("exp_5_timings.json", "w") as f:
    json.dump(timings, f, indent=4)

# To CSV
df_time = pd.DataFrame.from_dict(timings)
df_time.to_csv("exp_5_timings.csv", index=False)
print(f"Time plot saved as '{timeplot_filename}'.")