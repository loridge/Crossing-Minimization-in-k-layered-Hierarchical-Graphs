# experiment6.py
print("does it work")
import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, os
import pprint

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from k_layered_heuristics import hybrid_2
from k_layer_crossing import total_crossing_count_k_layer
from k_layered import generate_k_layered_sparse_graph
from exp_8_hybrids import BaseCutoffHybrid, PermuBaryCutoffHybrid, PermuSiftingCutoffHybrid, SiftingBaryCutoffHybrid, BarySiftingCutoffHybrid

# links
# https://www.geeksforgeeks.org/python-unzip-a-list-of-tuples/

# === CONFIG ===
num_samples = 20
# num_samples=1
k = 10
n_range = [8] # 8 dapat, pero 5 muna para pangtest
methods = ['bary_sift', 'sift_bary', 'permu_sift', 'permu_bary']
# n_range = range(6, 11)  # n = m
##### not yet done
# === Initialize result collectors ===
all_results = {}
timing_data = {}
reductions_full = {}  # for boxplot
ear_data = {method: [] for method in methods}  # keys like bary_sift, permu_sift, etc.

print("Experiment 8 starting")
for n in n_range:
    print(f"Executing {n}")
    reductions = {f"{method}_cutoff_{cutoff}": [] for cutoff in range(k) for method in methods} 
    timings_produced = {f"{method}_cutoff_{cutoff}": [] for cutoff in range(k) for method in methods} 
    crossings_produced = {f"{method}_cutoff_{cutoff}": [] for cutoff in range(k) for method in methods} # array due to many samples per hybrid-cutoff algo
    crossings_produced['crossings_orig'] = []
    #be considerate for the permu thing
    for run in range(num_samples):
        print(f"Generating sample {run}")
        nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, n)
        crossings_orig = total_crossing_count_k_layer(layers, edges)
        crossings_produced['crossings_orig'].append(crossings_orig)
        parsed_data = BaseCutoffHybrid.parse_layers_edges(layers, edges)

        for cutoff in range(k):
            bary_sift = BarySiftingCutoffHybrid(layers, edges, l_cutoff=cutoff, parsed_layer_edge_data=parsed_data, comment_out=1, capture = 0)
            bary_sift_reordered, time_data_bary_sift = bary_sift.execute()
            count_bary_sift = total_crossing_count_k_layer(bary_sift_reordered, edges)
            crossings_produced[f"{methods[0]}_cutoff_{cutoff}"].append(count_bary_sift)
            timings_produced[f"{methods[0]}_cutoff_{cutoff}"].append(time_data_bary_sift)
            reduction = 100 * (crossings_orig - count_bary_sift) / crossings_orig if crossings_orig else 0
            reductions[f"{methods[0]}_cutoff_{cutoff}"].append(reduction)
            
            # --- SiftBary Hybrid ---
            sift_bary = SiftingBaryCutoffHybrid(layers, edges, l_cutoff=cutoff, parsed_layer_edge_data=parsed_data, comment_out=1)
            sift_bary_reordered, time_data_sift_bary = sift_bary.execute()
            count_sift_bary = total_crossing_count_k_layer(sift_bary_reordered, edges)
            crossings_produced[f"{methods[1]}_cutoff_{cutoff}"].append(count_sift_bary)
            timings_produced[f"{methods[1]}_cutoff_{cutoff}"].append(time_data_sift_bary)
            reduction = 100 * (crossings_orig - count_sift_bary) / crossings_orig if crossings_orig else 0
            reductions[f"{methods[1]}_cutoff_{cutoff}"].append(reduction)

            # --- PermuSift Hybrid ---
            permusifting = PermuSiftingCutoffHybrid(layers, edges, l_cutoff=cutoff, parsed_layer_edge_data=parsed_data, comment_out=1)
            permusifting_reordered, time_data_permu_sift = permusifting.execute()
            count_permu_sift = total_crossing_count_k_layer(permusifting_reordered, edges)
            crossings_produced[f"{methods[2]}_cutoff_{cutoff}"].append(count_permu_sift)
            timings_produced[f"{methods[2]}_cutoff_{cutoff}"].append(time_data_permu_sift)
            reduction = 100 * (crossings_orig - count_permu_sift) / crossings_orig if crossings_orig else 0
            reductions[f"{methods[2]}_cutoff_{cutoff}"].append(reduction)

            # --- PermuBary Hybrid ---
            permubary = PermuBaryCutoffHybrid(layers, edges, l_cutoff=cutoff, parsed_layer_edge_data=parsed_data, comment_out=1)
            permubary_reordered, time_data_permu_bary = permubary.execute()
            count_permu_bary = total_crossing_count_k_layer(permubary_reordered, edges)
            crossings_produced[f"{methods[3]}_cutoff_{cutoff}"].append(count_permu_bary)
            timings_produced[f"{methods[3]}_cutoff_{cutoff}"].append(time_data_permu_bary)
            reduction = 100 * (crossings_orig - count_permu_bary) / crossings_orig if crossings_orig else 0
            reductions[f"{methods[3]}_cutoff_{cutoff}"].append(reduction)

    avg_crossings_produced = {
        key: float(np.mean(val)) if val else None
        for key, val in crossings_produced.items()
    }

    # pprint.pprint(avg_crossings_produced, indent =3, width =200)
    # pprint.pprint(crossings_produced, indent = 4, width =200)
    
    
    # Calculating EAR vs Cutoff
    
    optimal = avg_crossings_produced[f'permu_sift_cutoff_{k-1}']
    
    # Build EAR per method per cutoff
    for method in methods:
        for cutoff in range(k):
            key = f"{method}_cutoff_{cutoff}"
            val = avg_crossings_produced.get(key)
            if val is not None and optimal:
                ear = val / optimal
            else:
                ear = None
            ear_data[method].append(ear)
    
    # Graphing
    # Step 3: Plot line graph
    plt.figure(figsize=(10, 6))
    for method in methods:
        plt.plot(range(k), ear_data[method], marker='o', label=method.replace('_', ' ').title())

    plt.title("Empirical Approximation Ratio (EAR) of Averages vs Cutoff Value")
    plt.xlabel("Cutoff Value")
    plt.ylabel("Average EAR (lower is better)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("ear_vs_cutoff_lineplot.png", dpi=300)
    plt.show()
    
    
    # === Aggregate average times per method ===
    bar_width = 0.08
    spacing = 1.0

    # Color setup
    colors = {
        "algo1": "skyblue",
        "algo2": "lightgreen",
        "extra": "salmon"
    }

    fig, ax = plt.subplots(figsize=(18, 6))

    x_labels = []
    x_ticks = []
    x_base = 0

    for method_index, method in enumerate(methods):
        algo1_vals, algo2_vals, extra_vals = [], [], []

        for cutoff in range(k):
            key = f"{method}_cutoff_{cutoff}"
            if timings_produced[key]:
                arr = np.array(timings_produced[key])
                a1 = np.mean(arr[:, 1])
                a2 = np.mean(arr[:, 2])
                total = np.mean(arr[:, 0])
                ex = total - (a1 + a2)
            else:
                a1 = a2 = ex = 0

            xpos = x_base + cutoff * bar_width
            algo1_vals.append(a1)
            algo2_vals.append(a2)
            extra_vals.append(ex)

            # Plot stacked bar
            ax.bar(xpos, a1, width=bar_width, color=colors["algo1"])
            ax.bar(xpos, a2, width=bar_width, bottom=a1, color=colors["algo2"])
            ax.bar(xpos, ex, width=bar_width, bottom=a1 + a2, color=colors["extra"])

            x_ticks.append(xpos)
            x_labels.append(f"{method}\ncut{cutoff}")

        # Move to next algorithm group
        x_base += (k + 2) * bar_width

    # Formatting
    ax.set_title("Stacked Average Time by Cutoff (Grouped by Algorithm)")
    ax.set_ylabel("Time (seconds)")
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=90)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.legend(["Algo 1", "Algo 2", "Overhead"], loc='upper right')
    plt.tight_layout()

    # Save and display
    plt.savefig("stacked_time_by_algorithm_cutoff.png", dpi=300)
    plt.show()
    
    plt.figure(figsize=(10, 6))


    # === Scatterplot with cutoff labels ===
    # General color map for consistency
    color_map = {
        "bary_sift": "orange",
        "sift_bary": "blue",
        "permu_sift": "green",
        "permu_bary": "purple"
    }

    # === 1. General Combined Scatter Plot ===
    plt.figure(figsize=(10, 6))
    for method in methods:
        for cutoff in range(k):
            key = f"{method}_cutoff_{cutoff}"
            times = timings_produced.get(key, [])
            ear = ear_data[method][cutoff]
            if times and ear is not None:
                avg_time = np.mean([entry[0] for entry in times])
                plt.scatter(avg_time, ear, color=color_map[method], label=method if cutoff == 0 else "")
                plt.text(avg_time, ear, f"{cutoff}", fontsize=7, ha='left', va='bottom')

    plt.title("All Methods: EAR vs Total Time (Cutoff Labeled)")
    plt.xlabel("Average Total Time (s)")
    plt.ylabel("EAR (lower is better)")
    plt.grid(True)
    plt.legend(title="Method", loc='upper left')
    plt.tight_layout()
    plt.savefig("scatter_all_methods.png", dpi=300)
    plt.show()

    # === 2–5. Individual Plots per Method ===
    for method in methods:
        plt.figure(figsize=(8, 5))
        for cutoff in range(k):
            key = f"{method}_cutoff_{cutoff}"
            times = timings_produced.get(key, [])
            ear = ear_data[method][cutoff]
            if times and ear is not None:
                avg_time = np.mean([entry[0] for entry in times])
                plt.scatter(avg_time, ear, color=color_map[method])
                plt.text(avg_time, ear, f"{cutoff}", fontsize=8, ha='left', va='bottom')

        plt.title(f"{method.replace('_', ' ').title()}: EAR vs Total Time")
        plt.xlabel("Average Total Time (s)")
        plt.ylabel("EAR")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"scatter_{method}.png", dpi=300)
        plt.show()

print("Experiment 8 Concluded")