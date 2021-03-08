# -*- coding: utf-8 -*-

"""Example data and resources."""

import os

__all__ = [
    'BEL_EXAMPLE',
]

HERE = os.path.abspath(os.path.dirname(__file__))
BEL_EXAMPLE = os.path.join(HERE, 'covid_example.bel.nodelink.json')
