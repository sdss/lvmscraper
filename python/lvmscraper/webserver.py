# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2022-02-09
# @Filename: webserver.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import time
import random
import string

import cherrypy


from datetime import datetime as dt


from .datastore import DataStore

class WebServer(object):
    def __init__(self, datastore:DataStore):
        self.datastore = datastore
        self.default = "*"
        self.refresh = 10
    
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
            {self.datastore.formatData(filter)}
            <h1> fits </h1>
            {self.datastore.formatFits(filter)}
          </body>
        </html>"""

