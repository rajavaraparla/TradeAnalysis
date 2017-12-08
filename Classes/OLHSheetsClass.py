"""
    This will hold the information from Google Sheets Intra data

"""
from Classes.OLHBasicClass import OLHBasicClass


class OLHSheetsClass(OLHBasicClass): # pylint: disable=too-few-public-methods , too-many-arguments
    """
        OLHSheetsClass

    """
    def __init__(self, script, trade_time, p_open, high, low, ltp,volume, prev_close, cond):
        OLHBasicClass.__init__(self, script, trade_time, p_open,high ,low, ltp, volume, prev_close)
        self.cond = cond


    def __str__(self):
        ''' String representation of OLHSheetsClass '''
        olh_str = 'SCRIPT:{},OPEN={};HIGH={};LOW={};LTP={};PCLOSE={};Cond-{};'.format(
            self.script, self.p_open, self.high, self.low, self.ltp, self.pclose, self.cond
        )
        return olh_str

    def __repr__(self):
        ''' Representation of OLHSheetsClass '''
        olh_str = 'OLHSheetsClass({},{},{},{},{},{},{}'.format(
            self.script, self.p_open, self.high, self.low, self.ltp, self.pclose, self.cond
        )
        return olh_str



