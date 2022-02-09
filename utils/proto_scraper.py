import time
import random
import string

import threading
import cherrypy
import pandas as pd

import asyncio
from datetime import datetime as dt
import aio_pika as apika

from clu.client import AMQPClient, AMQPReply

from types import SimpleNamespace

import fnmatch

# hard exit
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

received = {}
fitscard = []
from collections.abc import MutableMapping

import hashlib, base64


def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str = '.'):
    def _flatten_dict_gen(d, parent_key, sep):
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                yield from flatten_dict(v, new_key, sep=sep).items()
            else:
                yield new_key, v

    return dict(_flatten_dict_gen(d, parent_key, sep))


def createSysFitsKey(name: str):
    sys_to_fits_keymap = {
        'lvm.sci.pwi': 'TIS', 
        'lvm.skye.pwi': 'TES', 
        'lvm.skyw.pwi': 'TWS', 
        'lvm.spec.pwi': 'TSS',
        'lvm.sci.foc': 'TIF', 
        'lvm.skye.foc': 'TEF', 
        'lvm.skyw.foc': 'TWF', 
        'lvm.spec.foc': 'TSF',
        'lvm.sci.km': 'TIK',
        'lvm.skye.km': 'TEK', 
        'lvm.skyw.km': 'TWK', 
        'lvm.spec.fibsel': 'TSF',
    }
    
    return sys_to_fits_keymap.get(name)

sys_param_to_fits_keymap = {
    'ra_j2000_hours':        ('RA',  "[HOURS] ra j2000 $NAME"),
    'dec_j2000_degs':         ('DEG', "[DEG] dec j2000 $NAME"),
    'DeviceEncoderPosition': ('POS', '[$Units] focus position $NAME'),
    'Units': (),
}

#Template('[$Units] %Y%d%m').substitute(r)


class StringGenerator(object):
    def __init__(self):
        self.default="*"
        self.refresh = 10
    
    def formatData(self, filter):
        sys = { key: received[key] for key in fnmatch.filter(received, filter)}
        return pd.DataFrame(data=sys).fillna('').to_html()


    def formatFits(self, filter):
        fkeys = []
        for sk in fnmatch.filter(received, filter):
            sv = received[sk]
            for (pk,pv) in sv.items():
                if (sp2f:=sys_param_to_fits_keymap.get(pk)) != None:
                    if len(sp2f):
                        comment = string.Template(sp2f[1]).substitute(sv, NAME=sk)
                        key=createSysFitsKey(sk) + sp2f[0]
                        fkeys.append([key, pv, comment])
                else:
                    
                    comment = f"{sk[p+1 if (p:=sk.find('.')) else 0:]}.{pk}"
                    fkeys.append([createFits8key(sk, pk), pv, comment])
                
        return pd.DataFrame(data=fkeys, columns=['Key', 'Value', 'Description']).to_html(index=False)


    @cherrypy.expose
    def index(self, filter="*", refresh=10):
        self.default = filter
        self.refresh = refresh
        
        return f"""<html>
          <head></head>
          <!meta http-equiv="refresh" content="{refresh}" >
          <body>
            <form method="get" action="">
              <input type="text" value={self.default} name="filter" />
              <button type="submit">filter</button>
            </form>
            <h1> data </h1>
            {self.formatData(filter)}
            <h1> fits </h1>
            {self.formatFits(filter)}
          </body>
        </html>"""


def createFits8key(sys: str, key: str):
    fitsSkey = createSysFitsKey(sys)
    if fitsSkey:
        return fitsSkey + base64.b64encode(hashlib.md5(f"{fitsSkey}.{key}".encode('utf8')).digest())[:5].decode()
    else:
        base64.b64encode(hashlib.md5(f"{fitsSkey}.{key}".encode('utf8')).digest())[:8].decode()


class AMQPClientScrap(AMQPClient):
    async def handle_reply(self, message: apika.IncomingMessage) -> AMQPReply:
        """Handles a reply received from the exchange.
        """
        global received
        global fitscard
        reply = AMQPReply(message, log=self.log)
#        print(f"{dt.now()} {reply.sender} {reply.body}")
        body = { key: value for (key,value) in flatten_dict(reply.body).items() if key not in ["text", "help", "error", "error.exception_message", "error.exception_module", "error.exception_type"]}
        if not len(body): return
        received[reply.sender] = {**old, **body} if (old:=received.get(reply.sender)) else body
        
        print(received)


async def main(loop):
   client = await AMQPClientScrap('lvm.scrap', host='localhost').start()
   

if __name__ == '__main__':
    # Start the server
    server = threading.Thread(target=cherrypy.quickstart, args=[StringGenerator()])
    server.start()
    
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    print("waiting ...")
    loop.run_forever()
    print("exit ...")


