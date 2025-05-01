import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === CONFIG ===
k = 10
methods = ['bary_sift', 'sift_bary', 'permu_sift', 'permu_bary']
color_map = {
    "bary_sift": "orange",
    "sift_bary": "blue",
    "permu_sift": "green",
    "permu_bary": "purple"
}

# === Load Data ===
suffix = "7-7"
crossings_df = pd.read_csv(f"crossings_produced_{suffix}.csv")
timings_df = pd.read_csv(f"timings_produced_{suffix}.csv")

# === Compute EARs ===
avg_crossings = crossings_df.drop(columns=["sample_id"]).mean()
optimal = avg_crossings.get(f'permu_sift_cutoff_{k-1}')

# Build EAR data
ear_data = {method: [] for method in methods}

for method in methods:
    for cutoff in range(k):
        key = f"{method}_cutoff_{cutoff}"
        val = avg_crossings.get(key)
        if val is not None and optimal:
            ear = val / optimal
        else:
            ear = None
        ear_data[method].append(ear)

# === EAR Line Plot ===
plt.figure(figsize=(10, 6))
for method in methods:
    plt.plot(range(k), ear_data[method], marker='o', label=method.replace('_', ' ').title())

plt.title(f"Empirical Approximation Ratio (EAR) of Averages vs Cutoff Value {suffix}")
plt.xlabel("Cutoff Value")
plt.ylabel("Average EAR (lower is better)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"ear_vs_cutoff_lineplot_{suffix}.png", dpi=300)
# plt.show()

# === Scatter Plots: Time vs EAR (All in One) ===
plt.figure(figsize=(10, 6))
for method in methods:
    for cutoff in range(k):
        key = f"{method}_cutoff_{cutoff}"
        total_times = timings_df[f"{key}_total"].dropna()
        avg_time = total_times.mean() if not total_times.empty else None
        ear = ear_data[method][cutoff]
        if avg_time and ear:
            plt.scatter(avg_time, ear, color=color_map[method], label=method if cutoff == 0 else "")
            plt.text(avg_time, ear, str(cutoff), fontsize=7, ha='left', va='bottom')

plt.title(f"All Methods: EAR vs Total Time (Cutoff Labeled) {suffix}")
plt.xlabel("Average Total Time (s)")
plt.ylabel("EAR (lower is better)")
plt.grid(True)
plt.legend(title="Method", loc='upper left')
plt.tight_layout()
plt.savefig(f"scatter_all_methods_{suffix}.png", dpi=300)
# plt.show()

# === Scatter Plots: Per Method ===
for method in methods:
    plt.figure(figsize=(8, 5))
    for cutoff in range(k):
        key = f"{method}_cutoff_{cutoff}"
        total_times = timings_df[f"{key}_total"].dropna()
        avg_time = total_times.mean() if not total_times.empty else None
        ear = ear_data[method][cutoff]
        if avg_time and ear:
            plt.scatter(avg_time, ear, color=color_map[method])
            plt.text(avg_time, ear, str(cutoff), fontsize=8, ha='left', va='bottom')

    plt.title(f"{method.replace('_', ' ').title()}: EAR vs Total Time {suffix}")
    plt.xlabel("Average Total Time (s)")
    plt.ylabel("EAR")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"scatter_{method}_{suffix}.png", dpi=300)
    # plt.show()

# === Stacked Bar Plot (Timing Breakdown) ===
bar_width = 0.08
fig, ax = plt.subplots(figsize=(18, 6))
colors = {"algo1": "skyblue", "algo2": "lightgreen", "extra": "salmon"}

x_labels = []
x_ticks = []
x_base = 0

for method_index, method in enumerate(methods):
    for cutoff in range(k):
        key = f"{method}_cutoff_{cutoff}"
        arr = timings_df[[f"{key}_total", f"{key}_algo1", f"{key}_algo2"]].dropna().to_numpy()
        if len(arr) == 0:
            continue
        a1 = np.mean(arr[:, 1])
        a2 = np.mean(arr[:, 2])
        total = np.mean(arr[:, 0])
        ex = total - (a1 + a2)

        xpos = x_base + cutoff * bar_width
        ax.bar(xpos, a1, width=bar_width, color=colors["algo1"])
        ax.bar(xpos, a2, width=bar_width, bottom=a1, color=colors["algo2"])
        ax.bar(xpos, ex, width=bar_width, bottom=a1 + a2, color=colors["extra"])

        x_ticks.append(xpos)
        x_labels.append(f"{method}\ncut{cutoff}")

    x_base += (k + 2) * bar_width

ax.set_title(f"Stacked Average Time by Cutoff (Grouped by Algorithm) {suffix}")
ax.set_ylabel("Time (seconds)")
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=90)
ax.grid(axis='y', linestyle='--', alpha=0.7)
ax.legend(["Algo 1", "Algo 2", "Overhead"], loc='upper right')
plt.tight_layout()
plt.savefig(f"stacked_time_by_algorithm_cutoff_{suffix}.png", dpi=300)
# plt.show()
