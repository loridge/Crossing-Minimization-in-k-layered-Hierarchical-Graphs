# Experiments Section

## Relevant Files
- exp1_v1_v2_sparse.ipynb: implementation of experiment 1 in parallelized computing
    - **helper file**: exp1_v1_v2_sparse_helper.py
- exp2_increasing_density.ipynb - implementation of experiment 2
- exp3_parallel_9.py - imple of experiment 3 in parallelized computing
- exp3.ipynb - imple of experiment 3
- leley_experiments.py - testbed for the singleton cases for bipartite graphs.
- plot_outlier_new.py - refactored function to accommodate zero division errors in the previous version
- summary_to_tabular.py - ran to summarize the result files in one large table 
- summary_to_graphs.py - to visualize the summary files from tabular form.

LA changed the ff files for the singleton
 experiments/exp1_v1_v2_sparse_helper.py   |  19 ++---
 experiments/exp2_increasing_density.ipynb |  16 ++---
 experiments/exp3.ipynb                    |  16 ++---
 experiments/exp3_parallel_9.py            |  14 ++--
 experiments/leley.py                      | 116 +++++++++++++++++++++++++-----