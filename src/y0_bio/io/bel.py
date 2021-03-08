# -*- coding: utf-8 -*-

"""Convert BEL to y0 mixed graphs."""

from typing import Optional

import pybel
import pybel.constants as pc
from ananke.graphs import ADMG
from pybel import BELGraph

from y0.graph import NxMixedGraph

__all__ = [
    'bel_to_nxmg',
    'bel_to_admg',
    'bel_to_causaleffect',
    'emmaa_to_nxmg',
]

CORRELATIVE_RELATIONS = pc.CORRELATIVE_RELATIONS | {pc.CORRELATION}
VALID = {'di', 'bi', 'skip'}


def bel_to_nxmg(
    bel_graph: BELGraph,
    *,
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
    - Only include protein-protein relationships identified by HGNC

    :param bel_graph: A BEL graph
    :param include_associations: Should :data:`pybel.constants.ASSOCIATION` relationships be included as bidirected
        edges in the graph? Defaults to false.
    :param indirect_handler: How should indirected edges be handled? If 'bi', adds as bidirected edges. Elif 'di',
        adds as bidirected edges. If 'skip', do not include. If None, defaults to 'bi'.
    :return: A y0 networkx mixed graph

    :raises ValueError: for invalid input on "indirect_handler"
    """
    rv = NxMixedGraph()
    if indirect_handler is None:
        indirect_handler = 'bi'
    if indirect_handler not in VALID:
        raise ValueError(f'invalid indirect edge handler: {indirect_handler}. Should be in {VALID}')
    for u, v, d in bel_graph.edges(data=True):
        try:
            u_name = u.name
        except AttributeError:
            u_name = str(u)
        try:
            v_name = v.name
        except AttributeError:
            v_name = str(v)
        if u_name == v_name:
            continue
        if d[pc.RELATION] in CORRELATIVE_RELATIONS:
            rv.add_undirected_edge(u_name, v_name)
        elif include_associations and d[pc.RELATION] == pc.ASSOCIATION:
            rv.add_undirected_edge(u_name, v_name)
        elif d[pc.RELATION] in pc.DIRECT_CAUSAL_RELATIONS:
            rv.add_directed_edge(u_name, v_name)
        elif d[pc.RELATION] in pc.INDIRECT_CAUSAL_RELATIONS:
            if indirect_handler == 'bi':
                rv.add_undirected_edge(u_name, v_name)
            elif indirect_handler == 'di':
                rv.add_directed_edge(u_name, v_name)
    return rv


def bel_to_admg(
    graph: BELGraph,
    *,
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

    >>> import pybel
    >>> from y0.dsl import P, Variable
    >>> from y0.identify import is_identifiable
    >>> from y0_bio.resources import BEL_EXAMPLE
    >>> from y0_bio.io.bel import bel_to_nxmg
    >>> bel_graph = pybel.load(BEL_EXAMPLE)
    >>> nxmg = bel_to_nxmg(bel_graph)
    >>> is_identifiable(nxmg, P(Variable('Severe Acute Respiratory Syndrome') @ Variable('angiotensin II')))
    """
    nxmg = bel_to_nxmg(
        graph,
        include_associations=include_associations,
        indirect_handler=indirect_handler,
    )
    return nxmg.to_admg()


def bel_to_causaleffect(
    graph: BELGraph,
    *,
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


def emmaa_to_nxmg(model: str, date: Optional[str] = None, **kwargs) -> NxMixedGraph:
    """Get content from EMMAA and convert to a NXMG.

    :param model: The name of the EMMAA model
    :param date: The optional date of the EMMAA model. See :func:`pybel.from_emmaa`.
    :param kwargs: Keyword arguments to pass to :func:`bel_to_nxmg`
    :return: A y0 networkx mixed graph

    The following example uses the `RAS model <https://www.ndexbio.org/#/network/cc9f904f-4ffd-11e9-9f06-0ac135e8bacf>`_
    on EMMAA.

    >>> from y0.dsl import P, Variable
    >>> from y0.identify import is_identifiable
    >>> from y0_bio.io.bel import emmaa_to_nxmg
    >>> KRAS = Variable('KRAS')
    >>> MAPK1 = Variable('MAPK1')
    >>> ras = emmaa_to_nxmg('rasmodel')
    >>> is_identifiable(ras, P(MAPK1 @ KRAS))
    True
    """
    bel_graph = pybel.from_emmaa(model, date=date)
    return bel_to_nxmg(bel_graph, **kwargs)
