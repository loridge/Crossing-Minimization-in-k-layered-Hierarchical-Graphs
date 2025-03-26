import pandas as pd
import numpy as np
import math
import networkx as nx 
import matplotlib.pyplot as plt

def plot_results_percentage_outliers(df, message=""):
    """
    Plots the experiment results. Also includes optional message for the title.
    Each combination of n1 and n2 will have its own line for each heuristic,
    using graph density instead of edge probability on the x-axis.
    """
    # Group by n1, n2 for clarity
    for n1 in df["n1"].unique():
        for n2 in df["n2"].unique():
            subset = df[(df["n1"] == n1) & (df["n2"] == n2)]
            if not subset.empty:
                plt.figure(figsize=(10, 6))
                
                # Compute graph density: Density = p
                density = subset["density"]  # In this case, density = 
                
                # X-axis: Graph density
                x = density
                
                y_barycenter = subset["avg_crossings_barycenter"] / subset["avg_crossings_optimal"] * 100
                y_median = subset["avg_crossings_median"] / subset["avg_crossings_optimal"] * 100
                y_sifting = subset["avg_crossings_sifting"] / subset["avg_crossings_optimal"] * 100
                y_optimal = subset["avg_crossings_optimal"] / subset["avg_crossings_optimal"] * 100
                
                y_barycenter = np.where(
                    subset["avg_crossings_optimal"] == 0, 
                    (subset["avg_crossings_barycenter"] + 1) / 1 * 100,  # Avoid zero division
                    (subset["avg_crossings_barycenter"] / subset["avg_crossings_optimal"]) * 100
                )
                y_median = np.where(
                    subset["avg_crossings_optimal"] == 0, 
                    (subset["avg_crossings_median"] + 1) / 1 * 100,  # Avoid zero division
                    (subset["avg_crossings_median"] / subset["avg_crossings_optimal"]) * 100
                )
                y_sifting = np.where(
                    subset["avg_crossings_optimal"] == 0, 
                    (subset["avg_crossings_sifting"] + 1) / 1 * 100,  # Avoid zero division
                    (subset["avg_crossings_sifting"] / subset["avg_crossings_optimal"]) * 100
                )
                y_optimal = np.where(
                    subset["avg_crossings_optimal"] == 0, 
                    (subset["avg_crossings_optimal"] + 1) / 1 * 100,  # Avoid zero division
                    (subset["avg_crossings_optimal"] / subset["avg_crossings_optimal"]) * 100
                )
                
                # print(y_barycenter)
                # print(y_median)
                # print(y_sifting)
                # print(y_optimal)
                # Find min and max y-values
                y_min = max(100, min(y_barycenter.min(), y_median.min(), y_sifting.min(), y_optimal.min()))
                y_max = max(y_barycenter.max(), y_median.max(), y_sifting.max(), y_optimal.max())
            
                # Round min/max to nearest 0.5
                y_min = np.floor(y_min * 2) / 2
                y_max = np.ceil(y_max * 2) / 2

                # Ensure there is at least a 0.5 difference
                if y_max - y_min < 0.5:
                    y_max = y_min + 0.5
                # Set y-axis ticks with 0.5 increments
                plt.yticks(np.arange(y_min, y_max + 0.5, 0.5))
                
                # Y-axis: Number of crossings
                # plt.plot(x, subset["avg_crossings_original"], label="Original Layout", marker="o")
                plt.plot(x,  y_barycenter, label="Barycenter Heuristic", marker="s")
                plt.plot(x, y_median, label="Median Heuristic", marker="^")
                plt.plot(x, y_sifting, label="Sifting Heuristic", marker="x")
                plt.plot(x, y_optimal, label="Optimal (Brute Force)", marker="x")
                plt.yscale('log')
                # Add labels and title
                plt.title(f"Crossings for n1 = {n1}, n2 = {n2}, {message}")
                plt.xlabel("Graph Density")
                plt.ylabel("In percentage of the minimum number of crossings")
                plt.legend()
                plt.grid(True)
                
                # Save result
                plt.savefig(f"exp3_results_{n1}+{n2}.png")
                
                # Show the plot
                plt.show()