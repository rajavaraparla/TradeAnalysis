"""
    This will hold the information from Google Sheets Intra data

"""
from Classes.OLHBasicClass import OLHBasicClass


class OLHEodClass(OLHBasicClass): # pylint: disable=too-few-public-methods , too-many-arguments
    """
        OLHEodClass

    """
    def __init__(self, script, trade_time, p_open, high, low, ltp,volume, pclose, vwap):
        OLHBasicClass.__init__(self, script, trade_time, p_open,high ,low, ltp, volume, pclose)
        self.vwap = vwap


    def __str__(self):
        ''' String representation of OLHSheetsClass '''
        olh_str = 'SCRIPT:{},OPEN={};HIGH={};LOW={};LTP={};PCLOSE={};VWAP-{};'.format(
            self.script, self.p_open, self.high, self.low, self.ltp, self.pclose, self.vwap
        )
        return olh_str

    def __repr__(self):
        ''' Representation of OLHSheetsClass '''
        olh_str = 'OLHSheetsClass({},{},{},{},{},{},{}'.format(
            self.script, self.p_open, self.high, self.low, self.ltp, self.pclose, self.vwap
        )
        return olh_str



