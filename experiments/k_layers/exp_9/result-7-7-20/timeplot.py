import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re

# === Settings ===
n = 7
m = 7
csv_file = f"exp-9_timings_produced_{n}-{m}.csv"
methods = ['bary_sift', 'sift_bary', 'permu_sift', 'permu_bary', 'bary_permu', 'sifting_permu']
colors = {
    "algo1": "skyblue",
    "algo2": "lightgreen",
    "extra": "salmon"
}

# === Load and Parse CSV ===
df = pd.read_csv(csv_file)

# Determine maximum cutoff value automatically
cutoff_pattern = re.compile(r'_cutoff_(\d+)_')
all_cutoffs = set()
for col in df.columns:
    match = cutoff_pattern.search(col)
    if match:
        all_cutoffs.add(int(match.group(1)))
k = max(all_cutoffs) + 1  # number of cutoff levels

# === Group and Plot ===
output_dir = f"plots-{n}-{m}"
os.makedirs(output_dir, exist_ok=True)

for method in methods:
    algo1_name, algo2_name = method.split('_')
    algo1_vals = []
    algo2_vals = []
    extra_vals = []
    cutoff_labels = []

    for cutoff in range(k):
        # Column names
        prefix = f"{method}_cutoff_{cutoff}"
        total_col = f"{prefix}_total"
        a1_col = f"{prefix}_algo1"
        a2_col = f"{prefix}_algo2"

        if total_col in df.columns and a1_col in df.columns and a2_col in df.columns:
            total = df[total_col].mean()
            a1 = df[a1_col].mean()
            a2 = df[a2_col].mean()
            extra = total - (a1 + a2)

            algo1_vals.append(a1)
            algo2_vals.append(a2)
            extra_vals.append(extra)
            cutoff_labels.append(f"Cutoff {cutoff}")
        else:
            algo1_vals.append(0)
            algo2_vals.append(0)
            extra_vals.append(0)
            cutoff_labels.append(f"Cutoff {cutoff}")

    # Plotting
    x = np.arange(k)
    bar_width = 0.6

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, algo1_vals, width=bar_width, color=colors["algo1"], label=f"{method}: {algo1_name}")
    ax.bar(x, algo2_vals, width=bar_width, bottom=algo1_vals, color=colors["algo2"], label=f"{method}: {algo2_name}")
    ax.bar(x, extra_vals, width=bar_width, bottom=np.array(algo1_vals)+np.array(algo2_vals),
           color=colors["extra"], label="Overhead")

    ax.set_title(f"Stacked Timing Breakdown for {method}")
    ax.set_xlabel("Cutoff Value")
    ax.set_ylabel("Average Time (s)")
    ax.set_xticks(x)
    ax.set_xticklabels(cutoff_labels, rotation=45)
    ax.legend(loc='upper left')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    output_file = os.path.join(output_dir, f"{method}_stacked_timing_plot-{n}-{m}.png")
    plt.savefig(output_file, dpi=300)
    plt.close()

print(f"✅ Plots saved in: {output_dir}")
