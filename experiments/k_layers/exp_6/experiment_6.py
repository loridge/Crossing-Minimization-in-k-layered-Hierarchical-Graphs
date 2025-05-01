# experiment6.py
import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from k_layered_heuristics import hybrid_2
from k_layer_crossing import total_crossing_count_k_layer
from k_layered import generate_k_layered_sparse_graph

# === CONFIG ===
num_samples = 20
k = 10
n_range = range(6, 11)  # n = m

# === Initialize result collectors ===
all_results = {}
timing_data = {}
reductions_full = {}  # for boxplot

for n in n_range:
    print(f"Executing {n}")
    reductions = {f"cutoff_{cutoff}": [] for cutoff in range(k)}
    timings = {f"cutoff_{cutoff}": [] for cutoff in range(k)}

    for run in range(num_samples):
        nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, n)
        crossings_orig = total_crossing_count_k_layer(layers, edges)

        for cutoff in range(k):
            start = time.perf_counter()
            new_layers = hybrid_2(layers, edges, cutoff)
            end = time.perf_counter()

            elapsed = end - start
            timings[f"cutoff_{cutoff}"].append(elapsed)

            new_crossings = total_crossing_count_k_layer(new_layers, edges)
            reduction = 100 * (crossings_orig - new_crossings) / crossings_orig if crossings_orig else 0
            reductions[f"cutoff_{cutoff}"].append(reduction)

    # Store mean reductions for bar plot
    all_results[f"n={n}"] = {cutoff: np.mean(values) for cutoff, values in reductions.items()}
    # Store full reductions for boxplot
    reductions_full[f"n={n}"] = reductions
    # Store timing data for bar plot
    timing_data[f"n={n}"] = {cutoff: (np.mean(times), np.std(times)) for cutoff, times in timings.items()}

# === Reduction Bar Plot (Average % Reduction per Cutoff) ===
for n_key, data in reductions_full.items():
    means = [np.mean(data[c]) for c in data]
    labels = list(data.keys())

    plt.figure(figsize=(14, 6))
    plt.bar(labels, means, color='skyblue')
    plt.ylabel("Average % Crossing Reduction")
    plt.title(f"Average % Crossing Reduction per Cutoff ({n_key})")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    reduction_bar_filename = f"experiment_6_{n_key}_reduction_barplot.png"
    plt.savefig(reduction_bar_filename, dpi=300)
    print(f"Saved {reduction_bar_filename}")

# === Box Plot ===
for n_key, data in reductions_full.items():
    plt.figure(figsize=(14, 6))
    plt.boxplot(
        [data[c] for c in data],
        labels=[c for c in data],
        patch_artist=True,
        boxprops=dict(facecolor='lightblue', color='blue'),
        medianprops=dict(color='red'),
        whiskerprops=dict(color='gray'),
        capprops=dict(color='gray'),
        flierprops=dict(markerfacecolor='orange', marker='o', markersize=5)
    )
    plt.title(f"Distribution of % Crossing Reduction per Cutoff ({n_key})")
    plt.ylabel("Crossing Reduction (%)")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    box_filename = f"{n_key}_boxplot.png"
    plt.savefig(box_filename, dpi=300)
    print(f"Saved {box_filename}")

# === Timing Bar Plot with Error Bars ===
for n_key, timings in timing_data.items():
    means = [timings[c][0] for c in timings]
    stds = [timings[c][1] for c in timings]
    labels = list(timings.keys())

    plt.figure(figsize=(14, 6))
    plt.bar(labels, means, yerr=stds, capsize=5, color='lightgreen')
    plt.ylabel("Execution Time (s)")
    plt.title(f"Average Execution Time per Cutoff ({n_key}) with Std Dev")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    timing_filename = f"exp_6_{n_key}_timing_barplot.png"
    plt.savefig(timing_filename, dpi=300)
    print(f"Saved {timing_filename}")

# === Save raw reductions and timing ===
with open("experiment_6_reductions.json", "w") as f:
    json.dump(reductions_full, f, indent=4)

with open("experiment_6_timings.json", "w") as f:
    json.dump(timing_data, f, indent=4)

print("All plots and data saved.")
