# import necessary libraries/packages
from distutils.log import error
import pandas as pd
import yfinance as yf

import os
import sys

# define variables
# tckrList = input( "Enter the ticker(s) value you'd like to research seperated by commas: " )
# tckrList = [ "MSFT" ]
tckrList = [ "MSFT", "VYM", "VGLT", "FRESX", "GLD", "FSPHX", "VEA", "VNQ", "VWO", "VB", "VOO", "VBIPX" ]

# small routine to load any packages in 'modules' folder
currDir = os.getcwd()
addDir = currDir + "\modules"

sys.path.insert( 0, addDir )

from modules import calculations as calc

# Ticker Info keys
""" ['exchange', 'shortName', 'longName', 'exchangeTimezoneName', 
'exchangeTimezoneShortName', 'isEsgPopulated', 'gmtOffSetMilliseconds', 
'quoteType', 'symbol', 'messageBoardId', 'market', 'annualHoldingsTurnover', 
'enterpriseToRevenue', 'beta3Year', 'profitMargins', 'enterpriseToEbitda', 
'52WeekChange', 'morningStarRiskRating', 'forwardEps', 'revenueQuarterlyGrowth', 
'fundInceptionDate', 'annualReportExpenseRatio', 'totalAssets', 'bookValue', 
'fundFamily', 'lastFiscalYearEnd', 'netIncomeToCommon', 'trailingEps', 'lastDividendValue', 
'SandP52WeekChange', 'priceToBook', 'nextFiscalYearEnd', 'yield', 'mostRecentQuarter', 
'enterpriseValue', 'priceHint', 'threeYearAverageReturn', 'lastSplitDate', 'lastSplitFactor', 
'legalType', 'lastDividendDate', 'morningStarOverallRating', 'earningsQuarterlyGrowth', 
'priceToSalesTrailing12Months', 'pegRatio', 'ytdReturn', 'forwardPE', 'maxAge', 'lastCapGain', 
'category', 'fiveYearAverageReturn', 'phone', 'longBusinessSummary', 'companyOfficers', 
'previousClose', 'regularMarketOpen', 'twoHundredDayAverage', 'trailingAnnualDividendYield', 
'payoutRatio', 'volume24Hr', 'regularMarketDayHigh', 'navPrice', 'averageDailyVolume10Day', 
'regularMarketPreviousClose', 'fiftyDayAverage', 'trailingAnnualDividendRate', 'open', 'toCurrency', 
'averageVolume10days', 'expireDate', 'algorithm', 'dividendRate', 'exDividendDate', 'beta', 'circulatingSupply', 
'startDate', 'regularMarketDayLow', 'currency', 'regularMarketVolume', 'lastMarket', 'maxSupply', 
'openInterest', 'marketCap', 'volumeAllCurrencies', 'strikePrice', 'averageVolume', 'dayLow', 'ask', 'askSize', 
'volume', 'fiftyTwoWeekHigh', 'fromCurrency', 'fiveYearAvgDividendYield', 'fiftyTwoWeekLow', 'bid', 'tradeable', 
'dividendYield', 'bidSize', 'dayHigh', 'preferredPosition', 'bondPosition', 'convertiblePosition', 'sectorWeightings', 
'holdings', 'bondHoldings', 'bondRatings', 'equityHoldings', 'otherPosition', 'cashPosition', 'stockPosition', 
'regularMarketPrice', 'preMarketPrice', 'logo_url'] """

########################
# real fun begins here #
########################
for tckrCode in tckrList :

    try :
        
        # primary code
        tckr = yf.Ticker( tckrCode )

    except :

        print( "Error : Failure during attempt to pull data for", tckrCode, ":" )
        print( error )

    else :

        # sample methods
        infoView = tckr.info # returns dictionary
        # print( infoView.keys() ) # pulls 'column names' from dictionary

        if "symbol" in infoView.keys() :

            print( "Pulling information for", infoView[ "symbol" ], ":", infoView[ "shortName" ] )

            listGetSevenDayClose = []
            listGetSevenDayClose = calc.GetSevenDayLowClose( tckrCode )

            # print( tckrCode, "Closed at a 7 day of low of :", listGetSevenDayClose[ 1 ], "on", listGetSevenDayClose[ 0 ] )

            # Ultimately - should I buy?
            calc.GetRecommendation( tckrCode )

        else :

            print( "Error : Ticker for", tckrCode, "could not be found." )

            break