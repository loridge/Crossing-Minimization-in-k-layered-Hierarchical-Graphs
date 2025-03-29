import sys, os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    
from sifting.crossing_function import (
    cross_count_optimized,
)