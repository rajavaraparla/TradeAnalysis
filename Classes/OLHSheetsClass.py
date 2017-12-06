"""
    This will hold the information from Google Sheets Intra data

"""
class OLHSheetsClass: # pylint: disable=too-few-public-methods , too-many-arguments
    """
        OLHSheetsClass

    """
    def __init__(self, script, p_open, high, low, ltp, prev_close, cond):
        self.script = script
        self.p_open = p_open
        self.high = high
        self.low = low
        self.ltp = ltp
        self.pclose = prev_close
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



