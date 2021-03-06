# recommender_interface.py
# November 2016
# CPSC 537
#
# This file interfaces the front end user input to the backend, including
# database queries and recommendation algorithms algorithm calls.
#

#computation imports
import time
import numpy as np
from predict_my_money.computations.recommender_algorithms import recommend_random_portfolio, recommend_high_return_portfolio, recommend_diverse_portfolio

#backend imports
import datetime
import json
from predict_my_money.utils import stockDayDatabaseInterface, stockAPI, get_stock_price_array
from django.http import HttpResponse

class SandP():
    def __init__(self):
        self.stocks = [
            "MMM", "ABT", "ABBV", "ACN", "ATVI", "AYI", "ADBE", "AAP", "AES", "AET", "AMG", "AFL", "A", "APD", "AKAM",
            "ALK", "ALB", "AA", "ALXN", "ALLE", "AGN", "ADS", "LNT", "ALL", "GOOGL", "GOOG", "MO", "AMZN", "AEE", "AAL"
            "AEP", "AXP", "AIG", "AMT", "AWK", "AMP", "ABC", "AME", "AMGN", "APH", "APC", "ADI", "ANTM", "AON", "APA",
            "AIV", "AAPL", "AMAT", "ADM", "AJG", "AIZ", "T", "ADSK", "ADP", "AN", "AZO", "AVGO", "AVB", "AVY", "BHI"]
            # "BLL", "BAC", "BCR", "BAX", "BBT", "BDX", "BBBY", "BRK-B", "BBY", "BIIB", "BLK", "HRB", "BA", "BWA", "BXP",
            # "BSX", "BMY", "BF-B", "CHRW", "CA", "COG", "CPB", "COF", "CAH", "KMX", "CCL", "CAT", "CBG", "CBS", "CELG",
            # "CNC", "CNP", "CTL", "CERN", "CF", "SCHW", "CHK", "CVX", "CMG", "CB", "CHD", "CI", "XEC", "CINF", "CTAS",
            # "CSCO", "C", "CFG", "CTXS", "CME", "CMS", "COH", "CTSH", "CL", "CMCSA", "CMA", "CAG", "CXO", "COP", "ED",
            # "STZ", "GLW", "COST", "CCI", "CSRA", "CSX", "CMI", "CVS", "DHI", "DHR", "DRI", "DVA", "DE", "DLPH", "DAL",
            # "XRAY", "DVN", "DO", "DLR", "DFS", "DISCA", "DISCK", "DG", "DLTR", "D", "DOV", "DOW", "DPS", "DTE", "DD",
            # "DUK", "DNB", "ETFC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "EMC", "EMR", "ENDP", "ETR", "EOG",
        #     "EQT", "EFX", "EQIX", "EQR", "ESS", "EL", "ES", "EXC", "EXPE", "EXPD", "ESRX", "EXR", "XOM", "FFIV", "FB",
        #     "FAST", "FRT", "FDX", "FIS", "FITB", "FSLR", "FE", "FISV", "FLIR", "FLS", "FLR", "FMC", "FTI", "FL", "F",
        #     "FTV", "FBHS", "BEN", "FCX", "FTR", "GPS", "GRMN", "GD", "GE", "GGP", "GIS", "GM", "GPC", "GILD", "GPN",
        #     "GS", "GT", "GWW", "HAL", "HBI", "HOG", "HAR", "HRS", "HIG", "HAS", "HCA", "HCP", "HP", "HSIC", "HES",
        #     "HPE", "HOLX", "HD", "HON", "HRL", "HST", "HPQ", "HUM", "HBAN", "ITW", "ILMN", "IR", "INTC", "ICE", "IBM",
        #     "IP", "IPG", "IFF", "INTU", "ISRG", "IVZ", "IRM", "JBHT", "JEC", "JNJ", "JCI", "JPM", "JNPR", "KSU", "K",
        #     "KEY", "KMB", "KIM", "KMI", "KLAC", "KSS", "KHC", "KR", "LB", "LLL", "LH", "LRCX", "LM", "LEG", "LEN",
        #     "LUK", "LVLT", "LLY", "LNC", "LLTC", "LKQ", "LMT", "L", "LOW", "LYB", "MTB", "MAC", "M", "MNK", "MRO",
        #     "MPC", "MAR", "MMC", "MLM", "MAS", "MA", "MAT", "MKC", "MCD", "MCK", "MJN", "MDT", "MRK", "MET", "KORS",
        #     "MCHP", "MU", "MSFT", "MHK", "TAP", "MDLZ", "MON", "MNST", "MCO", "MS", "MSI", "MUR", "MYL", "NDAQ", "NOV",
        #     "NAVI", "NTAP", "NFLX", "NWL", "NFX", "NEM", "NWSA", "NWS", "NEE", "NLSN", "NKE", "NI", "NBL", "JWN", "NSC",
        #     "NTRS", "NOC", "NRG", "NUE", "NVDA", "ORLY", "OXY", "OMC", "OKE", "ORCL", "OI", "PCAR", "PH", "PDCO",
        #     "PAYX", "PYPL", "PNR", "PBCT", "PEP", "PKI", "PRGO", "PFE", "PCG", "PM", "PSX", "PNW", "PXD", "PBI", "PNC",
        #     "RL", "PPG", "PPL", "PX", "PCLN", "PFG", "PG", "PGR", "PLD", "PRU", "PEG", "PSA", "PHM", "PVH", "QRVO",
        #     "QCOM", "PWR", "DGX", "RRC", "RTN", "O", "RHT", "REGN", "RF", "RSG", "RAI", "RHI", "ROK", "COL", "ROP",
        #     "ROST", "RCL", "R", "SPGI", "CRM", "SCG", "SLB", "SNI", "STX", "SEE", "SRE", "SHW", "SIG", "SPG", "SWKS",
        #     "SLG", "SJM", "SNA", "SO", "LUV", "SWN", "SE", "STJ", "SWK", "SPLS", "SBUX", "HOT", "STT", "SRCL", "SYK",
        #     "STI", "SYMC", "SYF", "SYY", "TROW", "TGT", "TEL", "TGNA", "TDC", "TSO", "TXN", "TXT", "BK", "CLX", "KO",
        #     "HSY", "MOS", "TRV", "DIS", "TMO", "TIF", "TWX", "TJX", "TMK", "TSS", "TSCO", "TDG", "RIG", "TRIP", "FOXA",
        #     "FOX", "TYC", "TSN", "USB", "UDR", "ULTA", "UA", "UNP", "UAL", "UNH", "UPS", "URI", "UTX", "UHS", "UNM",
        #     "URBN", "VFC", "VLO", "VAR", "VTR", "VRSN", "VRSK", "VZ", "VRTX", "VIAB", "V", "VNO", "VMC", "WMT", "WBA",
        #     "WM", "WAT", "WFC", "HCN", "WDC", "WU", "WRK", "WY", "WHR", "WFM", "WMB", "WLTW", "WEC", "WYN", "WYNN",
        #     "XEL", "XRX", "XLNX", "XL", "XYL", "YHOO", "YUM", "ZBH", "ZION", "ZTS"
        # ]



def recommend_interfacer(recommend_type='random', potential_stocks=None, num_observed_days=730, **kwargs):

    """
    This function takes the user's information and recommender parameters as input,
    pulls the required data from the database, cleans the data as necessary, runs
    the recommender algorithms, and updates the database with the portfolio.

    :param user_id:
        this is a database decision to keep track of which user is getting portfolio
    :param portfolio_id:
        this is a database decision to show what the portfolio will be called -- MIGHT
        HAVE TO ADD MORE STUFF HERE DEPENDING ON DATABASE DESIGN
    :param recommend_type:
        string, that determines which recommender algorithm will be used. The following
        are supported:
            'random', 'high_return', 'diverse'
    :param potential_stocks:
        list, potential stocks to use in the recommender algorithms. Algorithms with higher
        computational cost should use less stocks.
    :param num_observed_days:
        int, the number of days for which the model will be trained on. Default is 2 years.
    :param kwargs:
        dictionary, arguments for recommender algorithms. Keys can include
        budget, max_investment, time_horizon, diversity_threshold
    :return: a JSON Response of a dictionary with stockname -> amount to buy
    """

    # set this to FALSE if not debugging
    verbose = True

    # raise error if recommend_type is not supported
    if recommend_type not in ['random', 'diverse', 'high_return']:
        raise ValueError('recommend_type not recognized')

    # if potential stocks does not have anything, then choose from the S&P500
    if potential_stocks is None:
        SandPObject = SandP()
        potential_stocks = SandPObject.stocks

    if verbose:
        print('You called recommender on the following %d stocks' % len(potential_stocks) + ', '.join(potential_stocks))
    start_time = time.time()

    # put stock objects
    stock_objects = []
    stockGetter = stockAPI()
    for i, stock in enumerate(potential_stocks):
        s = stockGetter.getStock(stock)
        if s:
            stock_objects.append(s)

        if verbose:
            print('\tGot %d of %d, %s' %(i+1, len(potential_stocks),stock))
            if not s:
                print('\t\t%s was NoneType!' % stock)

    if verbose:
        print('Got them all -- took %.3f seconds' %(time.time() - start_time) )

    potential_stocks = stock_objects

    # number of potential stocks
    num_stocks = len(potential_stocks)

    # get stock price data
    interfaceObject = stockDayDatabaseInterface()
    today = datetime.date.today()
    first_date = today - datetime.timedelta(days=num_observed_days)
    stock_prices, stock_list, date_list = get_stock_price_array(stock_list=potential_stocks,
                                                                first_date=first_date, last_date=today)

    #
    #
    # if recommend_type == 'random':
    #
    #     # initialize stock prices
    #     stock_prices = np.empty(num_stocks)
    #     try_date = today
    #     clean_data = False
    #
    #     # add data until it is clean - should only take a couple tries
    #     days_back_to_try = 100
    #     for i in range(days_back_to_try):
    #
    #         clean_data = True
    #         for j, stock in enumerate(potential_stocks):
    #             day = interfaceObject.getSpecificDay(stock, try_date)
    #             if (day is not None):
    #                 price = day.adjustedClose
    #                 if np.isreal(price):
    #                     stock_prices[j] = price
    #                 else:
    #                     clean_data = False
    #                     break
    #             else:
    #                 clean_data = False
    #                 break
    #
    #         # if we got clean data, break
    #         if clean_data:
    #             break
    #         else:
    #             try_date -= datetime.timedelta(days=1)
    #
    #     if not clean_data:
    #         raise RuntimeError('There is not enough clean data for the days and stocks requested')
    #
    # else:
    #
    #     # get an entire 2D array of stock prices
    #
    #     first_date = today - datetime.timedelta(days=num_observed_days)
    #     stock_prices, stock_list, date_list = get_stock_price_array(stock_list=potential_stocks,
    #                                                                 first_date=first_date, last_date=today)

    # run desired recommender algorithm
    if recommend_type == 'random':
        stock_prices = stock_prices[:, -1] # just look at one day for random
        portfolio = recommend_random_portfolio(stock_ids=potential_stocks, stock_prices=stock_prices, **kwargs)

    elif recommend_type == 'high_return':
        portfolio = recommend_high_return_portfolio(stock_ids=potential_stocks, stock_prices=stock_prices, **kwargs)

    elif recommend_type == 'diverse':
        portfolio = recommend_diverse_portfolio(stock_ids=potential_stocks, stock_prices=stock_prices, **kwargs)

    #return a JSON compile of the recommended portfolio that front end code will deal with
    return portfolio
    # return HttpResponse(json.dumps(portfolio), content_type="application/json")
