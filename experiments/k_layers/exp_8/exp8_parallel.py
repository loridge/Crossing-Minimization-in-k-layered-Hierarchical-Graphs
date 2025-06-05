import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, os
import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from k_layered_heuristics import hybrid_2
from k_layer_crossing import total_crossing_count_k_layer
from k_layered import generate_k_layered_sparse_graph
from experiments.k_layers.hybrid_algorithms import BaseCutoffHybrid, PermuBaryCutoffHybrid, PermuSiftingCutoffHybrid, SiftingBaryCutoffHybrid, BarySiftingCutoffHybrid

def process_sample(run, k, n, methods):
    result = {
        "crossings_orig": None,
        "crossings": {},
        "reductions": {},
        "timings": {},
    }

    nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, n)
    crossings_orig = total_crossing_count_k_layer(layers, edges)
    parsed_data = BaseCutoffHybrid.parse_layers_edges(layers, edges)
    result["crossings_orig"] = crossings_orig

    hybrid_classes = {
        "bary_sift": BarySiftingCutoffHybrid,
        "sift_bary": SiftingBaryCutoffHybrid,
        "permu_sift": PermuSiftingCutoffHybrid,
        "permu_bary": PermuBaryCutoffHybrid
    }

    for method in methods:
        for cutoff in range(k):
            key = f"{method}_cutoff_{cutoff}"
            cls = hybrid_classes[method]
            instance = cls(layers, edges, l_cutoff=cutoff, parsed_layer_edge_data=parsed_data, comment_out=1, capture=0)
            reordered, timing = instance.execute()
            count = total_crossing_count_k_layer(reordered, edges)
            reduction = 100 * (crossings_orig - count) / crossings_orig if crossings_orig else 0

            result["crossings"][key] = count
            result["reductions"][key] = reduction
            result["timings"][key] = timing

    return result

# === CONFIG ===
if __name__ == "__main__":
    num_samples = 20
    k = 10
    n_range = [7]
    methods = ['bary_sift', 'sift_bary', 'permu_sift', 'permu_bary']

    # print("Experiment 8 starting")
    for n in n_range:
        crossings_produced = {f"{method}_cutoff_{cutoff}": [] for cutoff in range(k) for method in methods}
        crossings_produced["crossings_orig"] = []
        timings_produced = {f"{method}_cutoff_{cutoff}": [] for cutoff in range(k) for method in methods}
        reductions = {f"{method}_cutoff_{cutoff}": [] for cutoff in range(k) for method in methods}
        ear_data = {method: [] for method in methods}

        # print(f"Running {num_samples} samples in parallel for n={n}...")
        results_list = []
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(process_sample, run, k, n, methods) for run in range(num_samples)]
            for future in as_completed(futures):
                results_list.append(future.result())

        for result in results_list:
            crossings_produced["crossings_orig"].append(result["crossings_orig"])
            for key, val in result["crossings"].items():
                crossings_produced[key].append(val)
            for key, val in result["reductions"].items():
                reductions[key].append(val)
            for key, val in result["timings"].items():
                timings_produced[key].append(val)

        avg_crossings_produced = {
            key: float(np.mean(val)) if val else None
            for key, val in crossings_produced.items()
        }

        optimal = avg_crossings_produced[f'permu_sift_cutoff_{k-1}']

        for method in methods:
            for cutoff in range(k):
                key = f"{method}_cutoff_{cutoff}"
                val = avg_crossings_produced.get(key)
                ear = val / optimal if val and optimal else None
                ear_data[method].append(ear)

        # === EXPORT TO CSV ===
        crossings_df = pd.DataFrame(crossings_produced)
        crossings_df.insert(0, "sample_id", crossings_df.index)
        crossings_df.to_csv(f"crossings_produced_{n}-{n}.csv", index=False)
        print("✅ crossings_produced.csv saved.")

        timing_rows = []
        for i in range(num_samples):
            row = {"sample_id": i}
            for key, values in timings_produced.items():
                if i < len(values) and values[i]:
                    row[f"{key}_total"] = values[i][0]
                    row[f"{key}_algo1"] = values[i][1]
                    row[f"{key}_algo2"] = values[i][2]
                else:
                    row[f"{key}_total"] = None
                    row[f"{key}_algo1"] = None
                    row[f"{key}_algo2"] = None
            timing_rows.append(row)

        timings_df = pd.DataFrame(timing_rows)
        timings_df.to_csv(f"timings_produced_{n}-{n}.csv", index=False)
        print("✅ timings_produced.csv saved.")

    print("Experiment 8 completed.")
