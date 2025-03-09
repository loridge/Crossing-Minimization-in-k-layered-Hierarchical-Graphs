"""
This module performs experiments on bipartite graphs using various heuristics to minimize edge crossings.

The module generates bipartite graphs with specified parameters, applies different heuristics (Barycenter, Median, Sifting),
and calculates the number of edge crossings for each heuristic. The results are stored in a DataFrame and saved to a CSV file.
"""

import sys
import os

# # Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

from utility.bipartite_graph_generator import generate_bipartite_graph, visualize_bipartite_graph, count_crossings, update_positions, plot_results
from bary_med.two_layer_barycenter import barycenter, parse_edges, median, draw_horizontal_bipartite
# from edgedensity import generator_bip_graph
from sifting.sifting_2 import sifting
from sifting.crossing_function.crossing_func import cross_count
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
import time

# Parameters for experimentation
n1_values = [40] # Top-layer node counts
n2_values = [30]  # Bottom-layer node counts
p_values = [0.1, 0.2, 0.3, 0.4, ]  # Edge probabilities
# p_values = [0.1]
# Results list to store experiment outcomes
results = []

# Start the timer
start_time = time.time()

# Experiment loop
for n1 in n1_values:
    for n2 in n2_values:
        for p in p_values:
            # Generate bipartite graph
            nodes, edges, B, top_nodes, bottom_nodes = generate_bipartite_graph(n1, n2, p)
            # nodes, edges, B, top_nodes, bottom_nodes = generator_bip_graph(n1, n2, p)

            # Calculate density, not yet bipartite
            # density = nx.density(B)
            density = bipartite.density(B, set(top_nodes))
            # Visualize the graph (optional, for small graphs)
            #visualize_bipartite_graph(B, bottom_nodes)
            
            # Original layout
            pos_original = nx.bipartite_layout(B, top_nodes, align="horizontal")
            crossings_original = count_crossings(B, pos_original)

            # Parse the edges into (top_node, bottom_node) tuples before passing to the barycenter function
            parsed_edges = parse_edges(edges, top_nodes, bottom_nodes)
            
            # Apply Barycenter heuristic to reorder bottom nodes
            bottom_nodes_bary = barycenter(bottom_nodes, top_nodes, parsed_edges)

            #visualize_bipartite_graph(B, bottom_nodes_bary)

            # Update positions: top nodes fixed, bottom nodes reordered
            pos_barycenter = update_positions(top_nodes, bottom_nodes_bary)
            print("DEBUG: pos_barycenter =>", B, pos_barycenter)
            crossings_barycenter = count_crossings(B, pos_barycenter)
            
            # Apply Median heuristic to reorder bottom nodes
            bottom_nodes_median = median(bottom_nodes, top_nodes, parsed_edges)

            # Update positions: top nodes fixed, bottom nodes reordered
            pos_median = update_positions(top_nodes, bottom_nodes_median)
            # print("POS_MEDIAN", pos_median) 
            crossings_median = count_crossings(B, pos_median)

            #visualize_bipartite_graph(B, bottom_nodes_median)

            # Apply Simple Sifting heuristic to reorder bottom nodes
            sifting_heuristic = sifting(bottom_nodes, top_nodes, edges, verbose=0, )

            # draw_horizontal_bipartite(B, top_nodes, sifting_heuristic, "After Sift Algorithm") ## bug spotted, i also commented a code out in sifting
            pos_sifting = update_positions(top_nodes, sifting_heuristic) # the sifting_heuristic is 1,2,3,4,5 while the previous ones have 'u1, u2,..' 
            
            # print("POS_SIFTING", pos_sifting)
            
            crossings_sifting = count_crossings(B, pos_sifting)
            # crossings_sifting = cross_count(top_nodes, sifting_heuristic,edges)
            
            # Store results
            results.append({
                "n1": n1,
                "n2": n2,
                "p": p,
                "density": density,
                "crossings_original": crossings_original,
                "crossings_barycenter": crossings_barycenter,
                "crossings_median": crossings_median,
                "crossings_sifting": crossings_sifting
            })

# End the timer and print the total execution time
end_time = time.time()
total_time = end_time - start_time
print(f"Total execution time: {total_time:.2f} seconds")
# Convert results to a DataFrame for analysis
df = pd.DataFrame(results)

# Display results
print(df)

# Save the dataframe to a CSV file
df.to_csv('experiment_results.csv', index=False)

print("Results saved to '2_exp_results.csv'.")

# Call the plot function after results are stored
plot_results(df)
