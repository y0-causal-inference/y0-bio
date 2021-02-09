# -*- coding: utf-8 -*-

"""Tests for BEL importer."""

import unittest

from pybel import BELGraph
from pybel.dsl import Protein

from y0.graph import NxMixedGraph
from y0_bio.io.bel import bel_to_nxmg

TEST_CITATION = '1234'
TEST_EVIDENCE = 'ev'
A = Protein(namespace='hgnc', name='A')
B = Protein(namespace='hgnc', name='B')
C = Protein(namespace='hgnc', name='C')
D = Protein(namespace='hgnc', name='D')


class TestBELImport(unittest.TestCase):
    """Test importing BEL."""

    def nxmg_equal(self, expected, actual, msg=None):
        """Check that two ADMGs are equivalent."""
        self.assertIsInstance(expected, NxMixedGraph)
        self.assertIsInstance(actual, NxMixedGraph)
        self.assertEqual(set(expected.directed.edges()), set(actual.directed.edges()), msg=msg)
        self.assertEqual(set(expected.undirected.edges()), set(actual.undirected.edges()), msg=msg)

    def test_import_causal(self):
        """Check a directly increases."""
        bel_graph = BELGraph()
        bel_graph.add_directly_increases(A, B, citation=TEST_CITATION, evidence=TEST_EVIDENCE)
        bel_graph.add_directly_decreases(B, C, citation=TEST_CITATION, evidence=TEST_EVIDENCE)
        bel_graph.add_negative_correlation(A, C, citation=TEST_CITATION, evidence=TEST_EVIDENCE)
        bel_graph.add_association(A, D, citation=TEST_CITATION, evidence=TEST_EVIDENCE)

        expected = NxMixedGraph.from_edges(
            directed=[
                ('A', 'B'),
                ('B', 'C'),
            ],
            undirected=[
                ('A', 'C'),
            ],
        )
        self.nxmg_equal(expected, bel_to_nxmg(bel_graph, include_associations=False))

        expected = NxMixedGraph.from_edges(
            directed=[
                ('A', 'B'),
                ('B', 'C'),
            ],
            undirected=[
                ('A', 'C'),
                ('A', 'D'),
            ],
        )
        self.nxmg_equal(expected, bel_to_nxmg(bel_graph, include_associations=True))
