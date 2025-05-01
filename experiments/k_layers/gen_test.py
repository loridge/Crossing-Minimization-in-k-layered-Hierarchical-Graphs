from k_layered import generate_k_layered_sparse_graph, visualize_k_layered_graph

nodes, formatted_edges, G, layers = generate_k_layered_sparse_graph(5, 4, 7)
visualize_k_layered_graph(G, layers, "K-Layered Sparse Graph")



