# -*- coding: utf-8 -*-

"""Import BEL to Ananke."""

from ananke.graphs import ADMG
from pybel import BELGraph


def bel_to_ananke(graph: BELGraph) -> ADMG:
    """Convert a BEL Graph to an Ananke ADMG.

    Rules:

    - Directly increases, directly decreases, and directly regulates all become directed edges
    - Optional: increases, decreases, and regulate can either become directed or not
    - Positive correlation, negative correlation, and correlation become bidirected edges
    - Optional: association becomes bidirected edges

    :param graph: A BEL graph
    :return: An Ananke ADMG
    """
    raise NotImplementedError
