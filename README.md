# Crossing-Minimization-in-k-layered-Hierarchical-Graphs

A project for CS 198/199 under the Algorithms and Complexity Laboratory - UP Diliman




File naming convention:
- snake case (e.g. crossing_util.py, cross.py)

Element naming conventions:
- variables, package names, functions: snake_case
- classes: CamelCase
- constants: UPPERCASE

## Relevant Files so far
- Barycenter Test.py
- crossing_utils.py
- Graph Visualizer.py
- sifting.py
- 10node toy dataset

the rest are scratch files or whatnot,

## Major Bugs: 
### Crossing Function does not work
- if the fixed and free layer are reversed, the count goes way off.
- EDIT: the crossing function does not work as intended.


- FIX: The bug comes from the fact that the neighbor of a node in the FREE LAYER also includes the nodes of other layers.
- free layers with neighbors are a problem. fix the code! 
- which function is at fault? node_neighbors
- Status: fixed, added a filter to determine if a neighbor belongs to the relevant problem zone. 

- TODO: modularize the graph initialization code
### Crossing Function and its helper is not optimized
- will change implementation as necessary, optimization is last prio for this.