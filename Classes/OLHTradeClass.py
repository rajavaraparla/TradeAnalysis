'''
    This is the template for the Intra Class

'''
from Classes.OLHBasicClass import OLHBasicClass


class OLHTradeClass(OLHBasicClass): # pylint: disable=too-few-public-methods , too-many-arguments
    '''
        OLHTradeClass

    '''

    def __init__(self,script, trade_time, p_open, high,low,ltp, pclose, ipivot, atp, trade_str
                 , sl, entry1, entry2, entry3, target1, target2
                 , target3, target4, target5):
        '''
        constructor for Trade class
        :param script:
        :param trade_time:
        :param p_open:
        :param high:
        :param low:
        :param ltp:
        :param pclose:
        :param ipivot:
        :param atp:
        :param trade_str:
        :param sl:
        :param entry1:
        :param entry2:
        :param entry3:
        :param target1:
        :param target2:
        :param target3:
        :param target4:
        :param target5:
        '''
        OLHBasicClass.__init__(self, script, trade_time, p_open, high, low, ltp, None, pclose)
        self.ipivot = ipivot
        self.atp = atp
        self.trade_str = trade_str
        self.sl = sl
        self.entry1 = entry1
        self.entry2 = entry2
        self.entry3 = entry3
        self.target1 = target1
        self.target2 = target2
        self.target3 = target3
        self.target4 = target4
        self.target5 = target5

    def __str__(self):
        ''' String representation of OLHTradeClass'''
        trade_class = "{}--->{}={},{},{} SL={} , TARGETS = {},{},{},{},{}".format(self.script, self.trade_str
                                                                                  , self.entry1, self.entry2
                                                                                  , self.entry3, self.sl
                                                                                  , self.target1, self.target2
                                                                                  , self.target3, self.target4
                                                                                  , self.target5)
        return trade_class
