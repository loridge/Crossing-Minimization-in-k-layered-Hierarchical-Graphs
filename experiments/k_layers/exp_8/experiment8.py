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
from exp_8_hybrids import Exp8Utility, BaseCutoffHybrid, PermuBaryCutoffHybrid, PermuSiftingCutoffHybrid, SiftingBaryCutoffHybrid, BarySiftingCutoffHybrid

# === CONFIG ===
num_samples = 20
k = 10
n_range = range(6, 11)  # n = m
n_range = 8
##### not yet done
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