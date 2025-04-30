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
from exp_8_hybrids import BaseCutoffHybrid, PermuBaryCutoffHybrid, PermuSiftingCutoffHybrid, SiftingBaryCutoffHybrid, BarySiftingCutoffHybrid

# === CONFIG ===
num_samples = 20
k = 10
n_range = 8
methods = ['bary_sift', 'sift_bary', 'permu_sift', 'permu_bary']
# n_range = range(6, 11)  # n = m
##### not yet done
# === Initialize result collectors ===
all_results = {}
timing_data = {}
reductions_full = {}  # for boxplot

for n in n_range:
    print(f"Executing {n}")
    reductions = {f"{method}_cutoff_{cutoff}": [] for cutoff in range(k) for method in methods} 
    timings = {f"{method}_cutoff_{cutoff}": [] for cutoff in range(k) for method in methods} 


    for run in range(num_samples):
        print(f"Generating sample {run}")
        nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, n)
        crossings_orig = total_crossing_count_k_layer(layers, edges)

        parsed_data = BaseCutoffHybrid.parse_layers_edges(layers, edges)
        
        for cutoff in range(k):
            bary_sift = BarySiftingCutoffHybrid(layers, edges, l_cutoff=cutoff, parsed_layer_edge_data=parsed_data, comment_out=1, capture = 0)
            start = time.perf_counter()
            bary_sift_reordered = bary_sift.execute()
            end = time.perf_counter()
            new_crossings = total_crossing_count_k_layer(bary_sift_reordered, edges)
            elapsed = end - start
            timings[f"bary_sift_cutoff_{cutoff}"].append(elapsed)
            reduction = 100 * (crossings_orig - new_crossings) / crossings_orig if crossings_orig else 0
            reductions[f"{methods[0]}_cutoff_{cutoff}"].append(reduction)

            sift_bary = SiftingBaryCutoffHybrid(layers, edges, l_cutoff=cutoff, parsed_layer_edge_data=parsed_data, comment_out=1)
            start = time.perf_counter()
            sift_bary_reordered = sift_bary.execute()
            end = time.perf_counter()
            new_crossings = total_crossing_count_k_layer(bary_sift_reordered, edges)
            elapsed = end - start
            timings[f"{methods[1]}_cutoff_{cutoff}"].append(elapsed)
            reduction = 100 * (crossings_orig - new_crossings) / crossings_orig if crossings_orig else 0
            reductions[f"{methods[1]}_cutoff_{cutoff}"].append(reduction)


            permusifting = PermuSiftingCutoffHybrid(layers, edges, l_cutoff=cutoff, parsed_layer_edge_data=parsed_data, comment_out=1)
            start = time.perf_counter()
            permusifting_reordered = permusifting.execute()
            end = time.perf_counter()
            new_crossings = total_crossing_count_k_layer(bary_sift_reordered, edges)
            elapsed = end - start
            timings[f"bary_sift_cutoff_{cutoff}"].append(elapsed)
            reduction = 100 * (crossings_orig - new_crossings) / crossings_orig if crossings_orig else 0
            reductions[f"{methods[0]}_cutoff_{cutoff}"].append(reduction)


            permubary = PermuBaryCutoffHybrid(layers, edges, l_cutoff=cutoff, parsed_layer_edge_data=parsed_data, comment_out=1)
            start = time.perf_counter()
            permubary_reordered = permubary.execute()
            end = time.perf_counter()
            new_crossings = total_crossing_count_k_layer(bary_sift_reordered, edges)
            elapsed = end - start
            timings[f"bary_sift_cutoff_{cutoff}"].append(elapsed)
            reduction = 100 * (crossings_orig - new_crossings) / crossings_orig if crossings_orig else 0
            reductions[f"{methods[0]}_cutoff_{cutoff}"].append(reduction)

