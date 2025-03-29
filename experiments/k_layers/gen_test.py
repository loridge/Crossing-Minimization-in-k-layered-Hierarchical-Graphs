from k_layered import generate_k_layered_sparse_graph, visualize_k_layered_graph

nodes, formatted_edges, G, layers = generate_k_layered_sparse_graph(10, 5, 5)
visualize_k_layered_graph(G, layers, "K-Layered Sparse Graph")



