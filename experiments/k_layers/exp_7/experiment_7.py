# Hybrid 1 vs Full Permutation on increasing m values (as % of full permu)

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from k_layered_heuristics import (
    hybrid_1_permu_bary,
    permu_multi_sweep,
    permu_multi_sweep_patarasuk,
    barycenter_multi_sweep
)

from k_layer_crossing import (
    total_crossing_count_k_layer,
)

from k_layered import (
    generate_k_layered_sparse_graph,
)

# Parameters
m_values = [4, 5, 6, 7, 8]         # Number of vertices m
num_samples = 20             # Number of trials per m
k = 10                       # Number of layers
n = 8                         # Number of vertices n

# Store results
raw_crossings = {
    "m": [],
    "avg_crossings_hybrid": [],
    "avg_crossings_full_bary": [],
    "avg_crossings_full_permu": [],
    "hybrid_vs_full_percent": []
}

# all_stats = []

# def analyze_graph_properties_per_layer(layers, edges, m):
#     """
#     Analyzes degree, max degree, and density for each layer in the k-layered graph.
    
#     Args:
#         layers (List[List[int]]): The k layers containing node IDs.
#         edges (List[Dict]): List of dictionaries, each containing 'nodes' (a list of two nodes).
#         m (int): Current number of edges used in graph generation.
    
#     Returns:
#         pd.DataFrame: Stats per layer.
#     """
#     layer_stats = defaultdict(list)
    
#     # Build edge lookup to count degrees
#     degree = defaultdict(int)
#     for edge in edges:
#         if 'nodes' in edge and len(edge['nodes']) == 2:
#             u, v = edge['nodes']
#             degree[u] += 1
#             degree[v] += 1
    
#     for i in range(len(layers) - 1):  # For each pair of consecutive layers
#         layer_i = layers[i]
#         layer_j = layers[i + 1]
#         num_nodes = len(layer_i)
        
#         # Degree per node in this layer
#         degrees_in_layer = [degree[node] for node in layer_i]
#         avg_deg = sum(degrees_in_layer) / num_nodes if num_nodes > 0 else 0
#         max_deg = max(degrees_in_layer) if degrees_in_layer else 0

#         # Count edges between layer i and i+1
#         e_count = sum(
#             1 for edge in edges
#             if 'nodes' in edge and len(edge['nodes']) == 2
#             and edge['nodes'][0] in layer_i and edge['nodes'][1] in layer_j
#         )
#         max_possible = len(layer_i) * len(layer_j)
#         density = e_count / max_possible if max_possible else 0
        
#         # Store stats
#         layer_stats["m"].append(m)
#         layer_stats["layer"].append(i)
#         layer_stats["num_nodes"].append(num_nodes)
#         layer_stats["avg_degree"].append(avg_deg)
#         layer_stats["max_degree"].append(max_deg)
#         layer_stats["density"].append(density)
    
#     return pd.DataFrame(layer_stats)


    

# Run experiments
for m in m_values:
    total_hybrid = 0 
    total_bary = 0
    total_full = 0

    for _ in range(num_samples):
        nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, m)

        ## graph properties: degree and density
        # stats_df = analyze_graph_properties_per_layer(layers, edges, m)
        # all_stats.append(stats_df)  

        # Run Hybrid 1
        new_layers_hybrid = hybrid_1_permu_bary(layers, edges)
        crossings_hybrid = total_crossing_count_k_layer(new_layers_hybrid, edges)

        # Run Full Barycenter
        new_layers_full_bary = barycenter_multi_sweep(layers, edges)
        crossings_full_bary = total_crossing_count_k_layer(new_layers_full_bary, edges)

        # Run Full Permutation (Patarasuk)
        new_layers_full = permu_multi_sweep_patarasuk(layers, edges)
        crossings_full = total_crossing_count_k_layer(new_layers_full, edges)

        total_hybrid += crossings_hybrid
        total_bary += crossings_full_bary
        total_full += crossings_full

    avg_hybrid = total_hybrid / num_samples
    avg_bary = total_bary / num_samples
    avg_full = total_full / num_samples
    percent = avg_hybrid / avg_full * 100 if avg_full else 0

    # Store results
    raw_crossings["m"].append(m)
    raw_crossings["avg_crossings_hybrid"].append(avg_hybrid)
    raw_crossings["avg_crossings_full_bary"].append(avg_bary)
    raw_crossings["avg_crossings_full_permu"].append(avg_full)
    raw_crossings["hybrid_vs_full_percent"].append(percent)

# # Combine all stats into one DataFrame (graph properties)
# df_stats = pd.concat(all_stats, ignore_index=True)
# df_stats.to_csv("layer_stats.csv", index=False)

# Create DataFrame
df = pd.DataFrame({
    "m": raw_crossings["m"],
    "avg_crossings_hybrid": raw_crossings["avg_crossings_hybrid"],
    "avg_crossings_full_bary": raw_crossings["avg_crossings_full_bary"],
    "avg_crossings_full_permu": raw_crossings["avg_crossings_full_permu"]
})

# Add normalized percentages relative to Full Permutation (as optimal)
df["percent_hybrid"] = df["avg_crossings_hybrid"] / df["avg_crossings_full_permu"] * 100
df["percent_full_bary"] = df["avg_crossings_full_bary"] / df["avg_crossings_full_permu"] * 100
df["percent_full"] = df["avg_crossings_full_permu"] / df["avg_crossings_full_permu"] * 100  # Always 100


print(df)
# Save to CSV for inspection
df.to_csv("exp_7-test.csv", index=False)

# Plotting
plt.figure(figsize=(10, 6))
x = df["m"]
y_hybrid = df["percent_hybrid"]
y_full_bary = df["percent_full_bary"]
y_full = df["percent_full"]

# Compute y-limits using all three percent series
y_min_raw = min(y_hybrid.min(), y_full.min(), y_full_bary.min())
y_max_raw = max(y_hybrid.max(), y_full.max(), y_full_bary.max())
padding = (y_max_raw - y_min_raw) * 0.05
y_min = y_min_raw - padding
y_max = y_max_raw + padding
plt.ylim(y_min, y_max)

# X-axis: show integer ticks only
plt.xticks(sorted(df["m"].unique()))


# Plot
plt.plot(x, y_hybrid, label="Hybrid 1", marker="o", color="steelblue")
plt.plot(x, y_full_bary, label="Full Barycenter", marker="o", color="orange")
plt.plot(x, y_full, label="Full Permutation (Optimal)", linestyle="--", color="gray")

plt.title(f"Hybrid 1 vs Full Permutation\nExperiment 7:  n = {n}", fontsize=14)
plt.xlabel("Number of vertices (m)", fontsize=12)
plt.ylabel("In percentage of minimum number of crossings", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("exp_7-test.png", dpi=300)
plt.show()