from bipartite_graph_generator import generate_bipartite_graph, visualize_bipartite_graph, count_crossings, update_positions
from two_layer_barycenter import barycenter
import pandas as pd
import networkx as nx

# Parameters for experimentation
n1_values = [3] # Top-layer node counts
n2_values = [3]  # Bottom-layer node counts
p_values = [0.1]  # Edge probabilities

# Results list to store experiment outcomes
results = []

# Experiment loop
for n1 in n1_values:
    print("N1 VALUE", n1)
    for n2 in n2_values:
        for p in p_values:
            # Generate bipartite graph
            nodes, edges, B, top_nodes, bottom_nodes = generate_bipartite_graph(n1, n2, p)
            print("The nodes are", nodes)
            print("The top nodes are " + str(top_nodes))
            print("The bottom nodes are " + str(bottom_nodes))
            print("The nodes are ", nodes)
            print("The edges are ", edges)
            print("type of edges is " + str(type(edges)))
            print(edges)
            
            # Visualize the graph (optional, for small graphs)
            visualize_bipartite_graph(B, top_nodes)
            
            # Original layout
            pos_original = nx.bipartite_layout(B, top_nodes, align="horizontal")
            
            print("pos", pos_original)
            
            crossings_original = count_crossings(B, pos_original)
            
            # # Apply Barycenter heuristic to reorder bottom nodes
            bottom_nodes_bary = barycenter(bottom_nodes, top_nodes, edges)
            print("The bottom nodes after barycenter is " + str(bottom_nodes_bary))

            # # Update positions: top nodes fixed, bottom nodes reordered
            pos_barycenter = update_positions(top_nodes, bottom_nodes_bary)
            crossings_barycenter = count_crossings(B, pos_barycenter)
            
            #print("output of generator" + str(top_nodes) + str(edges))
            # Apply Barycenter heuristic
            # print("The edges passed to barycenter is " + str(edges))
            # print("Top nodes passed to barycenter is " + str(top_nodes))
            #stop_bary, bottom_bary = barycenter(top_nodes, edges)
            # pos_barycenter = update_positions(top_bary, bottom_bary)    ## !!!!!!!!1THIS IS WHERE U ENDED
            # crossings_barycenter = count_crossings(B, pos_barycenter)
            
            # Apply Median heuristic
            # top_med, bottom_med = median_heuristic(B, top_nodes)
            # pos_median = update_positions(top_med, bottom_med)
            # crossings_median = count_crossings(B, pos_median)
            
            # Calculate density
            density = nx.density(B)
            
            # Store results
            results.append({
                "n1": n1,
                "n2": n2,
                "p": p,
                "density": density,
                "crossings_original": crossings_original,
                "crossings_barycenter": crossings_barycenter,
                #"crossings_median": crossings_median
            })

# Convert results to a DataFrame for analysis
df = pd.DataFrame(results)

# Display results
print(df)

# Save the dataframe to a CSV file
df.to_csv('experiment_results.csv', index=False)

print("Results saved to 'experiment_results.csv'.")

