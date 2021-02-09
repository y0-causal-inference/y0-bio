# -*- coding: utf-8 -*-

"""Import BEL to Ananke."""

from typing import Optional

import pybel.constants as pc
from ananke.graphs import ADMG
from pybel import BELGraph

from y0.graph import NxMixedGraph

__all__ = [
    'bel_to_nxmg',
    'bel_to_admg',
    'bel_to_causaleffect',
]

CORRELATIVE_RELATIONS = pc.CORRELATIVE_RELATIONS | {pc.CORRELATION}
VALID = {'di', 'bi', 'skip'}


def bel_to_nxmg(
    graph: BELGraph,
    include_associations: bool = False,
    indirect_handler: Optional[str] = None,
) -> NxMixedGraph:
    """Convert a BEL Graph to a y0 networkx mixed graph.

    Rules:

    - Directly increases, directly decreases, and directly regulates all become directed edges
    - Optional: increases, decreases, and regulates become bidirected edges because there might
      be some confounders in the middle
    - Positive correlation, negative correlation, and correlation become bidirected edges
    - Association edges are excluded by default, could be optionally included

    :param graph: A BEL graph
    :param include_associations: Should :data:`pybel.constants.ASSOCIATION` relationships be included as bidirected
        edges in the graph? Defaults to false.
    :param indirect_handler: How should indirected edges be handled? If 'bi', adds as bidirected edges. Elif 'di',
        adds as bidirected edges. If 'skip', do not include. If None, defaults to 'bi'.
    :return: A y0 networkx mixed graph
    """
    rv = NxMixedGraph()
    if indirect_handler is None:
        indirect_handler = 'bi'
    if indirect_handler not in VALID:
        raise ValueError(f'invalid indirect edge handler: {indirect_handler}. Should be in {VALID}')
    for u, v, d in graph.edges(data=True):
        if d[pc.RELATION] in CORRELATIVE_RELATIONS:
            rv.add_undirected_edge(u.name, v.name)
        elif include_associations and d[pc.RELATION] == pc.ASSOCIATION:
            rv.add_undirected_edge(u.name, v.name)
        elif d[pc.RELATION] in pc.DIRECT_CAUSAL_RELATIONS:
            rv.add_directed_edge(u.name, v.name)
        elif d[pc.RELATION] in pc.INDIRECT_CAUSAL_RELATIONS:
            if indirect_handler == 'bi':
                rv.add_undirected_edge(u.name, v.name)
            elif indirect_handler == 'di':
                rv.add_directed_edge(u.name, v.name)
    return rv


def bel_to_admg(
    graph: BELGraph,
    include_associations: bool = False,
    indirect_handler: Optional[str] = None,
) -> ADMG:
    """Convert a BEL Graph to an Ananke ADMG.

    :param graph: A BEL graph
    :param include_associations: Should :data:`pybel.constants.ASSOCIATION` relationships be included as bidirected
        edges in the graph? Defaults to false.
    :param indirect_handler: How should indirected edges be handled? If 'bi', adds as bidirected edges. Elif 'di',
        adds as bidirected edges. If 'skip', do not include. If None, defaults to 'bi'.
    :return: An Ananke ADMG
    """
    nxmg = bel_to_nxmg(
        graph,
        include_associations=include_associations,
        indirect_handler=indirect_handler,
    )
    return nxmg.to_admg()


def bel_to_causaleffect(
    graph: BELGraph,
    include_associations: bool = False,
    indirect_handler: Optional[str] = None,
) -> ADMG:
    """Convert a BEL Graph to a CausalEffect R graph object.

    :param graph: A BEL graph
    :param include_associations: Should :data:`pybel.constants.ASSOCIATION` relationships be included as bidirected
        edges in the graph? Defaults to false.
    :param indirect_handler: How should indirected edges be handled? If 'bi', adds as bidirected edges. Elif 'di',
        adds as bidirected edges. If 'skip', do not include. If None, defaults to 'bi'.
    :return: A CausalEffect R graph object
    """
    nxmg = bel_to_nxmg(
        graph,
        include_associations=include_associations,
        indirect_handler=indirect_handler,
    )
    return nxmg.to_causaleffect()
