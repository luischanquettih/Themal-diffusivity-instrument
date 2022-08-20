# coding=utf-8

# Author: Diego Gonzalez Chavez
# email : diegogch@cbpf.br / diego.gonzalez.chavez@gmail.com
# Adapted from https://github.com/Vrekrer/magdynlab

import pyvisa as visa
import datetime
import os
import time

__all__ = ['InstrumentBase']

Resources_in_use = []

def findResource(search_string,
                 filter_string='',
                 query_string='*IDN?',
                 open_delay=2,
                 **kwargs):
    if os.name == 'nt':
        rm = visa.ResourceManager()
    else:
        rm = visa.ResourceManager('@py')
    for resource in set(rm.list_resources()).difference(Resources_in_use):
        if filter_string in resource:
            VI = rm.open_resource(resource, **kwargs)
            time.sleep(open_delay)
            try:
                VI.clear()
                if search_string in VI.query(query_string):
                    VI.close()
                    return resource
            except:
                VI.close()
                pass
    return None

class InstrumentBase(object):
    '''
    Base class for the instrument
    '''

    def __init__(self, ResourceName, logFile=None, **kargs):
        if os.name == 'nt':
            rm = visa.ResourceManager()
        else:
            rm = visa.ResourceManager('@py')
        self.VI = rm.open_resource(ResourceName, **kargs)
        Resources_in_use.append(ResourceName)
        self._IDN = self.VI.resource_name
        if logFile is None:
            self._logFile = None
        else:
            if not os.path.isfile(logFile):
                with open(logFile, 'w') as log:
                    log.write('THD_Instrument LogFile\n')
            self._logFile = os.path.abspath(logFile)
        self._logWrite('OPEN_')

    def __del__(self):
        self._logWrite('CLOSE')
        self.VI.close()

    def __str__(self):
        return "%s : %s" % ('THD_Instrument', self._IDN)

    def _logWrite(self, action, value=''):
        if self._logFile is not None:
            with open(self._logFile, 'a') as log:
                timestamp = datetime.datetime.utcnow()
                log.write('%s %s %s : %s \n' %
                          (timestamp, self._IDN, action, repr(value)))
    _log = _logWrite

    def write(self, command):
        self._logWrite('write', command)
        self.VI.write(command)

    def read(self):
        self._logWrite('read ')
        returnR = self.VI.read()
        self._logWrite('resp ', returnR)
        return returnR

    def query(self, command):
        self._logWrite('query', command)
        returnQ = self.VI.query(command)
        returnQL = returnQ
        if len(returnQ) > 100:
            self._logWrite('resp ', returnQ[:100] + '...')
        else:
            self._logWrite('resp ', returnQ)
        return returnQ

    def query_type(self, command, type_caster):
        try:
            returnQ = self.query(command)
            return type_caster(returnQ)
        except Exception as E:
            self._logWrite('ERROR', E.__repr__())
            returnQ = self.query(command)
            return type_caster(returnQ)

    def query_int(self, command):
        return self.query_type(command, int)

    def query_float(self, command):
        return self.query_type(command, float)


