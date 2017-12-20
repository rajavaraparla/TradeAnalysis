"""
    This is the basic class OLH Class.
    All the further classes will be inherited from this.

"""


class OLHBasicClass:

    def __init__(self,script, trade_time, p_open, high, low, ltp, volume, pclose=None):
        self.script = script
        self.trade_time = trade_time
        self.p_open = p_open # Current Candle Open.
        self.high = high
        self.low = low
        self.ltp = ltp
        self.volume = volume
        self.pclose = pclose

    def __repr__(self):
        ''' Representation of OLHBasicClass '''
        olh_str = 'OLHBasicClass({},{},{},{},{},{},{})'.format(
            self.script, self.trade_time, self.p_open, self.high, self.low, self.ltp, self.volume, self.pclose
        )
        return olh_str

    def __str__(self):
        ''' String representation of OLHBasicClass '''
        olh_str = 'SCRIPT:{};TradeTime={};OPEN={};HIGH={};LOW={};LTP={};VOLUME={};PCLOSE={}'.format(
            self.script, self.trade_time, self.p_open, self.high, self.low, self.ltp, self.volume, self.pclose
        )
        return olh_str


