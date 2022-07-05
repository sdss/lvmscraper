# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2022-02-09
# @Filename: scraper.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import asyncio
import aio_pika as apika

from clu.client import AMQPClient, AMQPReply

from .datastore import DataStore


from collections.abc import MutableMapping

def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str = '.'):
    def _flatten_dict_gen(d, parent_key, sep):
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                yield from flatten_dict(v, new_key, sep=sep).items()
            else:
                yield new_key, v

    return dict(_flatten_dict_gen(d, parent_key, sep))


class AMQPClientScraper(AMQPClient):
    def __init__(self, datastore, name:str="", **kwargs):

        self.store = datastore.store
        self.ignore = ["text", "help", "schema", "error", "error.exception_message", "error.exception_module", "error.exception_type", "cards", "scraper"]
        
        self.actor_name = name
        self.scraper_name = f"{self.actor_name}.listener"
        
        super().__init__(self.scraper_name, **{key: val for (key,val) in kwargs.items() if key != 'name'})


    async def handle_reply(self, message: apika.IncomingMessage) -> AMQPReply:
        """Handles a reply received from the exchange.
        """
        reply = AMQPReply(message, log=self.log)

        # self.log.warning(f"{self.name} {reply.headers} {reply.sender} {reply.command_id}")
        
        if reply.sender == self.actor_name:
            return
        
        body = { key: value for (key,value) in flatten_dict(reply.body).items() if key not in self.ignore}
        if not len(body): 
            return
        
        self.store[reply.sender] = {**old, **body} if (old:=self.store.get(reply.sender)) else body
        
#        print(f"{reply.sender}: {body}")
#        print(self.store)
