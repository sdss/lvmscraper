# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2022-02-09
# @Filename: datastore.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from datetime import datetime as dt

from types import SimpleNamespace

import fnmatch
import string

import hashlib, base64
import pandas as pd


class DataStore(object):
    def __init__(self):
        ### fix me
        self.sys_to_fits_keymap = {
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
        
        self.sys_param_to_fits_keymap = {
            'ra_j2000_hours':        ('RA',  "[HOURS] ra j2000 $NAME"),
            'dec_j2000_degs':         ('DEG', "[DEG] dec j2000 $NAME"),
            'DeviceEncoderPosition': ('POS', '[$Units] focus position $NAME'),
            'Units': (),
        }
        
        self.store = {}
        
    def createSysFitsKey(self, name: str):
        if (sk:=self.sys_to_fits_keymap.get(name)):
            return sk
        else:
            return "XXX"

    def createFits8key(self, sys: str, key: str):
        fitsSkey = self.createSysFitsKey(sys)
        if fitsSkey:
            return fitsSkey + base64.b64encode(hashlib.md5(f"{fitsSkey}.{key}".encode('utf8')).digest())[:5].decode()
        else:
            return base64.b64encode(hashlib.md5(f"{fitsSkey}.{key}".encode('utf8')).digest())[:8].decode()
        return sys_to_fits_keymap.get(name)


    def data(self, filter):
        return { key: self.store[key] for key in fnmatch.filter(self.store, filter)}

    def formatData(self, filter):
        return pd.DataFrame(data=self.data(filter)).fillna('').to_html()

    def asFits(self, filter):
        fkeys = []
        for sk in fnmatch.filter(self.store, filter):
            sv = self.store[sk]
            for (pk,pv) in sv.items():
                if (sp2f:=self.sys_param_to_fits_keymap.get(pk)) != None:
                    if len(sp2f):
                        comment = string.Template(sp2f[1]).substitute(sv, NAME=sk)
                        key = self.createSysFitsKey(sk) + sp2f[0]
                        fkeys.append([key, pv, comment])
                else:
                    comment = f"{sk[p+1 if (p:=sk.find('.')) else 0:]}.{pk}"
                    fkeys.append([self.createFits8key(sk, pk), pv, comment])
        return fkeys

    def formatFits(self, filter):
        return pd.DataFrame(data=self.asFits(filter), columns=['Key', 'Value', 'Description']).to_html(index=False)


