import sys
from os import path

"""
Add directory 1 level up to system path.
"""

current = path.dirname(path.realpath(__file__))
parent = path.dirname(current)
sys.path.append(parent)
