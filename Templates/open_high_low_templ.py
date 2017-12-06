OH_STRING="""
    SCRIPT : #SCRIPT#
    LTP : #CMP#
    NSE : #NSE_SIGNAL#
    BSE : #BSE_SIGNAL#
    Trading Below ATP : #TRADE_ATP#
    Trading Below PIVOT : #TRADE_PIVOT#
    Trading Below PREV_CLOSE : #TRADE_PCLOSE#
    SL : #SL#
    Bonus Short : #ENTRY3#
    SHORT (If Red)@ : #ENTRY2#
    Hold (If Red)@ : #ENTRY1#
               T1@ : #TARGET1#
               T2@ : #TARGET2#
               T3@ : #TARGET3#
               T4@ : #TARGET4#
               T5@ : #TARGET5#
    Low Made : #LOW_MADE#
    """

OL_STRING="""
    SCRIPT : #SCRIPT#
    LTP : #CMP#
    NSE : #NSE_SIGNAL#
    BSE : #BSE_SIGNAL#
    Trading Above ATP : #TRADE_ATP#
    Trading Above PIVOT : #TRADE_PIVOT#
    Trading Above PREV_CLOSE : #TRADE_PCLOSE#
    SL : #SL#
    Bonus Buy : #ENTRY3#
    Buy (If Green)@ : #ENTRY2#
    Hold (If Green)@ : #ENTRY1#
               T1@ : #TARGET1#
               T2@ : #TARGET2#
               T3@ : #TARGET3#
               T4@ : #TARGET4#
               T5@ : #TARGET5#
    High Made : #HIGH_MADE#
"""