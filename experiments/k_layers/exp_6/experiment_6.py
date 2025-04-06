# experiment6.py
import json
import ctypes
import winsound
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from k_layered_heuristics import hybrid_2
from k_layer_crossing import total_crossing_count_k_layer
from k_layered import generate_k_layered_sparse_graph

# === CONFIG ===
num_samples = 20
k = 10                     # Number of layers in the graph
n_range = range(6, 11)     # Number of nodes in each layer (n = m: odd and even layers have equal size)

# === Initialize result collector ===
all_results = {}

for n in n_range:
    # n is used for both odd and even layers (n = m)
    reductions = {f"cutoff_{cutoff}": [] for cutoff in range(k)}

    for run in range(num_samples):
        # Generate a k-layered graph with equal number of nodes per layer
        nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, n)  # n = m
        crossings_orig = total_crossing_count_k_layer(layers, edges)

        for cutoff in range(k):
            new_layers = hybrid_2(layers, edges, cutoff)
            new_crossings = total_crossing_count_k_layer(new_layers, edges)
            reduction = 100 * (crossings_orig - new_crossings) / crossings_orig if crossings_orig else 0
            reductions[f"cutoff_{cutoff}"].append(reduction)

    # Store average reduction per cutoff for current n
    all_results[f"n={n}"] = {cutoff: np.mean(values) for cutoff, values in reductions.items()}

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

plot_filename = "experiment_6.png"
plt.savefig(plot_filename, dpi=300)  # high-res PNG
print(f"Plot saved as '{plot_filename}'.")

with open("experiment_6.json", "w") as f:
    json.dump(reductions, f, indent=4)

# To CSV
df = pd.DataFrame.from_dict(reductions)
df.to_csv("experiment_6.csv", index=False)

# Play a loud sound
winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

# Show a Windows message box
ctypes.windll.user32.MessageBoxW(
    0,
    "Your k-layered graph analysis is done!",
    "Execution Complete ✅",
    0x40  # MB_ICONINFORMATION
)