from typing import Dict, List



# Example usage
edges = [
    {"nodes": ["u1", "u7"]},
    {"nodes": ["u1", "u6"]},
    {"nodes": ["u1", "u8"]},
    {"nodes": ["u5", "u6"]},
    {"nodes": ["u5", "u7"]},
    {"nodes": ["u1", "u2"]},
    {"nodes": ["u1", "u3"]},
    {"nodes": ["u1", "u4"]},
    {"nodes": ["u5", "u3"]},
    {"nodes": ["u5", "u2"]}
]

layered_pos = {1: ['u1', 'u5'], 2: ['u2', 'u3', 'u4'], 0: ['u6', 'u7', 'u8']}
pos = {
    "u1": [-0.5, -2],
    "u5": [0.5, -2],
    "u2": [-1.0, -4],
    "u3": [0.0, -4],
    "u4": [1.0, -4],
    "u6": [-1.0, 0],
    "u7": [0.0, 0],
    "u8": [1.0, 0]
}

target = "u7"
a = u_prime_processor(target, pos, layered_pos)
print(a)