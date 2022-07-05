# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2021-07-06
# @Filename: data.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)



from __future__ import annotations

import click
from clu.command import Command

from clu.parsers.click import command_parser

from lvmscraper.datastore import DataStore

@command_parser.command()
@click.option("--filter", type=str, default="*")
async def data(command: Command, ds: DataStore, filter: str):
    """return raw data filtered"""

    #command.command_id="scraper"

    return command.finish( **ds.data(filter) )


@command_parser.command()
@click.option("--filter", type=str, default="*")
async def fits(command: Command, ds: DataStore, filter:str):
    """return fits data filtered"""

    #command.command_id="scraper"

    return command.finish( cards=ds.asFits(filter) )

