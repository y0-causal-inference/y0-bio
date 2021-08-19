# -*- coding: utf-8 -*-

"""Tools for acquiring and normalizing the content from INDRA."""

import json
import os

import click

import pybel
import pybel.grounding

HERE = os.path.abspath(os.path.dirname(__file__))
RAW_PATH = os.path.join(HERE, 'covid19-indra-raw.bel.nodelink.json')
GROUNDED_PATH = os.path.join(HERE, 'covid19-indra-grounded.bel.nodelink.json')


@click.command()
@click.option('--force', is_flag=True)
@click.option('--user', prompt=True)
@click.password_option()
def main(force: bool, user: str, password: str):
    """Download and dump the INDRA 'rona graph."""
    if not os.path.exists(GROUNDED_PATH) and not force:
        if not os.path.exists(RAW_PATH) and not force:
            click.echo('Getting EMMAA graph')
            graph = pybel.from_emmaa('covid19')
            pybel.dump(graph, RAW_PATH)
        else:
            click.echo('Loading EMMAA graph from path')
            graph = pybel.load(RAW_PATH)

        graph = pybel.grounding.ground(graph)
        graph.summarize()

        pybel.dump(graph, GROUNDED_PATH)
    else:
        graph = pybel.load(GROUNDED_PATH)

    res = pybel.to_bel_commons(
        graph=graph,
        host='https://bel.labs.coronawhy.org',
        user=user,
        password=password,
    )
    click.secho(json.dumps(res.json(), indent=2))


if __name__ == '__main__':
    main()
