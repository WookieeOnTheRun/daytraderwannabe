# module containing functions for calculation and determination

import yfinance as yf
import datetime as dt
import statistics as stats

def GetSevenDayLowClose( ticker ) :
    
    # reference : https://www.youtube.com/watch?v=_9Bmxylp63Y
    # get lowest closing price of a stock within a 7 day period

    endDate = dt.date.today()
    startDate = endDate + dt.timedelta( days = -7 )

    tckr = yf.Ticker( ticker )

    tckrInfo = tckr.info

    # .history() returns a dataframe
    historyView = tckr.history( start = startDate, end = endDate )

    lowestClose = historyView[ "Close" ].min()
    # lowestClose = "${:,.2f}".format( lowestClose )

    lowestCloseDate = historyView[ "Close" ].idxmin()

    # print( "Lowest 7 Day Close was", lowestClose, "on", lowestCloseDate )

    listReturn = []
    listReturn.append( lowestCloseDate )
    listReturn.append( lowestClose )

    return( listReturn )

def GetRollingSevenDayLowClose( ticker ) :

    tckr = yf.Ticker( ticker )

    masterEndDate = dt.date.today()
    masterStartDate = masterEndDate + dt.timedelta( days = -30 )

    # print( "Master Start :", masterStartDate )
    # print( "Master End :", masterEndDate )

    listResults = []

    rollingEndDate = masterEndDate
    rollingStartDate = rollingEndDate + dt.timedelta( days = -7 )

    # print( "Start :", rollingStartDate )
    # print( "End :", rollingEndDate )

    # begin loop
    while ( rollingStartDate >= masterStartDate ) :

        rollingHistoryView = tckr.history( start = rollingStartDate, end = rollingEndDate )

        lowestClose = rollingHistoryView[ "Close" ].min()
        # lowestClose = "${:,.2f}".format( lowestClose )

        # print( "Function Lowest Close: ", lowestClose )

        listResults.append( lowestClose )

        rollingEndDate = rollingStartDate
        rollingStartDate = rollingStartDate + dt.timedelta( days = -7 )

    # print( "Rolling Results from Function:", listResults )

    return( listResults )

def GetRecommendation( ticker ) :

    # get current info at time of execution
    tckr = yf.Ticker( ticker )
    tckrInfo = tckr.info
    
    # get lowest close price over last 7 days
    listResults = GetSevenDayLowClose( ticker )
    lowestClosePrice = listResults[ 1 ]

    # get rolling 7 day close over 30 days
    listRollingResults = GetRollingSevenDayLowClose( ticker )

    # print( "Rolling Results:", listRollingResults )

    # get mean, max std dev of rolling list
    rollingMean = stats.mean( listRollingResults )
    rollingMax = max( listRollingResults )
    rollingMin = min( listRollingResults )
    rollingStdDev = stats.pstdev( listRollingResults )

    # How does lowest closing price(s) compare to fiftyDayAverage? twoHundredDayAverage?

    print( "Data for :", ticker )
    print( "7-Day Low Close:", "${:,.2f}".format( lowestClosePrice ) )
    print( "Rolling 7-Day Low Close over a Period of 30 Days:", listRollingResults )
    print( "Min Value from Rolling 7-Day Results:", "${:,.2f}".format( rollingMin ) )
    print( "Max Value from Rolling 7-Day Results:", "${:,.2f}".format( rollingMax ) )
    print( "Mean Value from Rolling 7-Day Results:", "${:,.2f}".format( rollingMean ) )
    print( "Standard Deviation Value from Rolling 7-Day Results:", "${:,.2f}".format( rollingStdDev ) )

    if "fiftyDayAverage" in tckrInfo.keys() and tckrInfo[ "fiftyDayAverage" ] is not None :
        curr50Day = tckrInfo[ "fiftyDayAverage" ]
        print( "Fifty Day Average :", "${:,.2f}".format( curr50Day ) )

    if "twoHundredDayAverage" in tckrInfo.keys() and tckrInfo[ "twoHundredDayAverage" ] is not None :
        curr200Day = tckrInfo[ "twoHundredDayAverage" ]
        print( "Two Hundred Day Average :", "${:,.2f}".format( curr200Day ) )

    # Quick check for 'Golden Cross' or 'Death Cross' or approaching - Delta of 15%
    # if Golden Cross - sell?
    # if Death Cross - watch or buy?

    if ( ( curr50Day >= curr200Day ) or ( ( curr50Day < curr200Day) and ( ( curr50Day / curr200Day ) <= .15 ) ) ) :

        print( "Golden Cross either identified or impending - watch for possible sale opportunity" )

    elif ( ( curr50Day < curr200Day ) or ( ( curr50Day < curr200Day) and ( ( curr50Day / curr200Day ) > .15 ) ) ) :

        print( "Death Cross either identified or impending - continue to monitor or consider purchase" )