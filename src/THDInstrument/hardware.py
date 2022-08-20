# coding=utf-8


from .instrument_base import InstrumentBase as _InstrumentBase
from .instrument_base import findResource

__all__ = ['THD_Arduino']


class THD_Arduino(_InstrumentBase):
    def __init__(self,
                 ResourceName=None, logFile=None):
        if ResourceName is None:
            ResourceName = findResource('FC-UNI, Thermal Diffusivity Instrument',
                                        filter_string='ASRL',
                                        timeout=2000,
                                        read_termination='\n',
                                        write_termination='\n')
        super().__init__(ResourceName, logFile)
        self._IDN = 'Thermal Diffusivity Instrument'
        self.VI.write_termination = self.VI.LF
        self.VI.read_termination = self.VI.LF

    @property
    def ID(self):
        '''ID'''
        return self.query('*IDN?')

    @property
    def Temperature1(self):
        return self.query_float('MEAS:TEMP1?')

    @property
    def Temperature2(self):
        return self.query_float('MEAS:TEMP1?')
        
    def set_voltage(self, vOut):
        return self.write('VOLT %0.4f' % vOut)
