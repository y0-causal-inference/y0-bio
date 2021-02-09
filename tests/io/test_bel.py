# -*- coding: utf-8 -*-

"""Tests for BEL importer."""

import unittest

from ananke.graphs import ADMG
from pybel import BELGraph
from pybel.dsl import Protein

from y0_bio.io.bel import bel_to_ananke

A = Protein(namespace='hgnc', name='A')
B = Protein(namespace='hgnc', name='B')


class TestBELImport(unittest.TestCase):
    """Test importing BEL."""

    def admg_equal(self, expected, actual, msg=None):
        """Check that two ADMGs are equivalent."""
        self.assertIsInstance(expected, ADMG)
        self.assertIsInstance(actual, ADMG)
        self.assertEqual(expected, actual, msg=msg)

    def test_import_causal(self):
        """Check a directly increases."""
        bel_graph = BELGraph()
        bel_graph.add_directly_increases(A, B, citation='', evidence='')
        actual = bel_to_ananke(bel_graph)
        expected = ADMG(
            vertices=['A', 'B'],
            di_edges=[
                ('A', 'B'),
            ],
        )
        self.admg_equal(expected, actual)
