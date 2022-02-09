# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2021-07-06
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio
from contextlib import suppress

from clu.actor import AMQPActor

from cluplus import __version__
from cluplus.configloader import Loader

from .commands import command_parser as scraper_command_parser

from lvmscraper.datastore import DataStore
from lvmscraper.scraper import AMQPClientScraper
from lvmscraper.webserver import WebServer

import threading
import cherrypy

# hard exit
#import signal
#signal.signal(signal.SIGINT, signal.SIG_DFL)


__all__ = ["ScraperActor"]


class ScraperActor(AMQPActor):
    """PWI actor.
    """

    parser = scraper_command_parser
    
    def __init__(
            self,
            *args,
            **kwargs
    ):
        super().__init__(*args, version=__version__, **kwargs)
        
        self.schema = {
                        "type": "object",
                        "properties": {},
                        "additionalProperties": True
                     }

        self.load_schema(self.schema, is_file=False)

        self.datastore = DataStore()


    async def start(self):
        await super().start()

      
        try:
            self.log.debug(f"Start scraper ...")

            ### fixme
            scraper = await AMQPClientScraper(self.datastore, 'lvm.scrap', host='localhost').start()

            webserver = threading.Thread(target=cherrypy.quickstart, args=[WebServer(self.datastore)])
            webserver.start()


        except Exception as ex:
            self.log.error(f"Unexpected exception {type(ex)}: {ex}")

        self.log.debug("Start done")

    async def stop(self):
        return await super().stop()

    @classmethod
    def from_config(cls, config, *args, **kwargs):
        """Creates an actor from hierachical configuration file(s)."""

        instance = super(ScraperActor, cls).from_config(config, loader=Loader, *args, **kwargs)

        if kwargs["verbose"]:
            instance.log.fh.setLevel(0)
            instance.log.sh.setLevel(0)

        instance.log.debug("Hello world")

        assert isinstance(instance, ScraperActor)
        assert isinstance(instance.config, dict)

        instance.parser_args = [ instance.datastore ]

        return instance
