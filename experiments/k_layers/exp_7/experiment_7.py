# Hybrid 1 vs Full Permutation on increasing m values (as % of full permu)

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
)

# Parameters
m_values = [4, 6, 8]         # Number of vertices m
num_samples = 20             # Number of trials per m
k = 10                       # Number of layers
n = 8                        # Number of vertices n

# Store results
raw_crossings = {
    "m": [],
    "avg_crossings_hybrid": [],
    "avg_crossings_full_permu": [],
    "hybrid_vs_full_percent": []
}

# Run experiments
for m in m_values:
    total_hybrid = 0
    total_full = 0

    for _ in range(num_samples):
        nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, m)
        # Run Hybrid 1
        new_layers_hybrid = hybrid_1_permu_bary(layers, edges)
        crossings_hybrid = total_crossing_count_k_layer(new_layers_hybrid, edges)

        # Run Full Permutation (Patarasuk)
        new_layers_full = permu_multi_sweep_patarasuk(layers, edges)
        crossings_full = total_crossing_count_k_layer(new_layers_full, edges)

        total_hybrid += crossings_hybrid
        total_full += crossings_full

    avg_hybrid = total_hybrid / num_samples
    avg_full = total_full / num_samples
    percent = avg_hybrid / avg_full * 100 if avg_full else 0

    # Store results
    raw_crossings["m"].append(m)
    raw_crossings["avg_crossings_hybrid"].append(avg_hybrid)
    raw_crossings["avg_crossings_full_permu"].append(avg_full)
    raw_crossings["hybrid_vs_full_percent"].append(percent)

# Create DataFrame
df = pd.DataFrame({
    "m": raw_crossings["m"],
    "avg_crossings_hybrid": raw_crossings["avg_crossings_hybrid"],
    "avg_crossings_full_permu": raw_crossings["avg_crossings_full_permu"]
})

# Add normalized percentages relative to Full Permutation (as optimal)
df["percent_hybrid"] = df["avg_crossings_hybrid"] / df["avg_crossings_full_permu"] * 100
df["percent_full"] = df["avg_crossings_full_permu"] / df["avg_crossings_full_permu"] * 100  # Always 100

# Save to CSV for inspection
df.to_csv("hybrid_vs_full_data.csv", index=False)

# Plotting
plt.figure(figsize=(10, 6))
x = df["m"]
y_hybrid = df["percent_hybrid"]
y_full = df["percent_full"]

# Compute y-limits with padding (5% of the range)
y_min_raw = min(y_hybrid.min(), y_full.min())
y_max_raw = max(y_hybrid.max(), y_full.max())
padding = (y_max_raw - y_min_raw) * 0.05
y_min = y_min_raw - padding
y_max = y_max_raw + padding
plt.ylim(y_min, y_max)

# X-axis: show integer ticks only
plt.xticks(sorted(df["m"].unique()))


# Plot
plt.plot(x, y_hybrid, label="Hybrid 1", marker="o", color="steelblue")
plt.plot(x, y_full, label="Full Permutation (Optimal)", linestyle="--", color="gray")

plt.title(f"Hybrid 1 vs Full Permutation\nExperiment 7:  n = {n}", fontsize=14)
plt.xlabel("Number of vertices (m)", fontsize=12)
plt.ylabel("In percentage of minimum number of crossings", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("hybrid_vs_full_percentage_plot_corrected.png", dpi=300)
plt.show()