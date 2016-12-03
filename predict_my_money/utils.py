

import requests
import datetime
import numpy as np
import predict_my_money.computations.basic_computations
from .models import Stock, Stock_Day, Portfolio, Portfolio_Day, Stock_Owned




def get_stock_price_array(stock_list, first_date, last_date):

    # initialize interface object
    interfaceObject = stockDayDatabaseInterface()

    # get all historical stock data into a 2D numpy array -- start with dict, put into numpy array later
    num_stocks = len(stock_list)
    stock_price_dict = {}

    for i, stock in enumerate(stock_list):

        # get all days in the range that we have in the database
        days = interfaceObject.getRangeDaysOrdered(stock, first_date, last_date)

        # add days to stock price
        for day in days:
            # only do anything if that day is not None
            if day:
                # if this day already exists, update the numpy array
                if day.day in stock_price_dict.keys():
                    stock_price_dict[day.day][i] = day.adjustedClose
                # else if this day does not exist, then create a numpy array initialized to all entries nan
                else:
                    stock_price_dict[day.day] = np.empty(num_stocks) * np.nan
                    stock_price_dict[day.day][i] = day.adjustedClose

    # turn the dictionary into a 2D numpy array using column stack
    date_list = sorted(stock_price_dict.keys())
    stock_prices = np.column_stack(tuple([stock_price_dict[k] for k in date_list]))

    # Clean the data
    # 1. Remove any stock that is missing more than 75% of the data
    percent_missing_threshold = 0.75
    n, p = stock_prices.shape
    keep_rows = np.sum(np.isnan(stock_prices), axis=1) < p * percent_missing_threshold
    stock_prices = stock_prices[keep_rows, :]
    stock_list = [stock for i, stock in enumerate(stock_list) if keep_rows[i]]

    # 2. For each day we have,
    #       If there is less than 75% of the data, remove it
    #       Otherwise, interpolate data from 5 days before or 5 days after
    #           if 10 consecutive days are missing, remove the stock

    # remove days with few data points
    keep_columns = np.sum(np.isnan(stock_prices), axis=0) < p * percent_missing_threshold
    stock_prices = stock_prices[:, keep_columns]
    date_list = [date for i, date in enumerate(date_list) if keep_columns[i]]

    # interpolate those where they are missing
    rows_to_remove = []
    for ind in np.argwhere(np.isnan(stock_prices)):

        # try going backward 5 days
        interpolated = False
        for i in np.arange(1, 6):
            try:
                interp = stock_prices[ind[0], ind[1] - i]
                if np.isreal(interp):
                    stock_prices[ind[0], ind[1]] = interp
                    interpolated = True
                    break
            except IndexError:
                break

        # try going forward 5 days
        if not interpolated:
            for i in np.arange(1, 6):
                try:
                    interp = stock_prices[ind[0], ind[1] + i]
                    if np.isreal(interp):
                        stock_prices[ind[0], ind[1]] = interp
                        interpolated = True
                        break
                except IndexError:
                    break

        # if not interpolated, remove that stock
        if not interpolated:
            rows_to_remove.append(ind[0])

    # remove the finals rows that had 10 consecutive days missing
    stock_prices = np.delete(stock_prices, rows_to_remove, axis=0)
    stock_list = [stock for i, stock in enumerate(stock_list) if not keep_rows[i]]

    # raise an error if we have too few days to run our model on
    lower_threshold_on_days = stock_prices.shape[0]  # howl if we have more stocks than days
    lower_threshold_on_stocks = num_stocks * 0.75
    if stock_prices.shape[1] <= lower_threshold_on_days or stock_prices.shape[0] <= lower_threshold_on_stocks:
        raise RuntimeError('There is not enough clean data for the days and stocks requested')

    return stock_prices, stock_list, date_list




class stockDayDatabaseInterface():
    def getAllDaysOrdered(self, stock):
        days = Stock_Day.objects.order_by('day').filter(stock=stock)
        return days

    def getSpecificDay(self, stock, dayRequested):
        try:
            day = Stock_Day.objects.filter(stock=stock, day=dayRequested)
        except Stock_Day.DoesNotExist:
            return None
        else:
            if len(day) > 1:
                toBeDestroyed = None
                for time in day:
                    if toBeDestroyed:
                        toBeDestroyed.delete()
                    toBeDestroyed = time
                return toBeDestroyed
            elif len(day) == 1:
                return day[0]
            else:
                return None

    def getRangeDaysOrdered(self, stock, earliestDate, LatestDate):
        days = Stock_Day.objects.order_by('day').filter(day__lte=LatestDate).filter(day__gte=earliestDate).filter(stock=stock)
        return days

class portfolioAPI():
#controls portfolio maintenance

    def getPortfolio(self, portfolio_id):

        try:
            # see if stock exists in database
            portfolio = Portfolio.objects.get(pk=portfolio_id)
        except Portfolio.DoesNotExist:
            # if stock does not exist
            return None
        else:
            current_date = datetime.date.today()
            if portfolio.end_date.date < current_date - datetime.timedelta(days=1):
                recentDay = self.fixPortfolioDays(portfolio_id, portfolio.end_date)
                portfolio.end_date = recentDay.day
                portfolio.current_diversity = recentDay.diversity
                portfolio.current_value = recentDay.value
                portfolio.save()
        return portfolio

    def fixPortfolioDays(self, portfolio_id, earliest_day=None):
        if not earliest_day:
            earliest_day = datetime.datetime.strptime('01-01-2012', '%m-%d-%Y') + datetime.timedelta(days=60)

        today = datetime.date.today()
        portfolio = Portfolio.objects.get(pk=portfolio_id)

        #instantiate interfaces
        stockInterface = stockDayDatabaseInterface()
        stockapi = stockAPI()

        #all stock_owned objects connected to this portfolio
        stocks = Stock_Owned.objects.get(portfolio=portfolio)

        #fill stocksObjects array with stock objects
        stocksObjects = []
        for stock in stocks:
            #get stock objects
            stock = Stock.objects.get(pk=stock.stock)
            #update stock with newest days
            stock = stockapi.getStock(stock.stock_name)
            stocksObjects.append(stock)

        creationDateWithBuffer = portfolio.end_date - datetime.timedelta(days=70)

        cleanedArray, stocks_in, days_in = get_stock_price_array(stocksObjects, creationDateWithBuffer, today)

        #clean stock_owned objects array
        stocks = [stock for i, stock in enumerate(stocks) if stocks[i].stock in stocks_in]

        #build 1d numpy array for amounts
        stock_amounts = np.array([stock.amount_owned for stock in stocks])

        #find first index
        endFrame = portfolio.end_date + datetime.timedelta(days=1)
        startFrame = endFrame + datetime.timedelta(days=60)
        startIndex = 0
        endIndex = 0

        for index, day in enumerate(days_in):
            if day < startFrame:
                startIndex = index
            else:
                startIndex = index
                break
        for index, day in enumerate(days_in):
            if day < endFrame:
                endIndex = index
            else:
                endIndex = index
                break

        tsr_array = predict_my_money.computations.basic_computations.compute_tsr(cleanedArray, stock_amounts)

        mostRecentDay = None
        #create Portfolio_Day objects
        while endFrame < today - datetime.timedelta(days=1):
            newPortDay = Portfolio_Day()
            newPortDay.portfolio = portfolio
            newPortDay.day = endFrame
            newPortDay.value = tsr_array[endIndex]
            newPortDay.diversity = predict_my_money.computations.basic_computations.compute_diversity(cleanedArray[:, startIndex:endIndex + 1], stock_amounts)
            newPortDay.save()
            mostRecentDay = newPortDay
            endFrame = endFrame + datetime.timedelta(days=1)
            startFrame = startFrame + datetime.timedelta(days=1)
            if days_in[startIndex + 1] >= startFrame:
                startIndex += 1
            if days_in[endIndex + 1] <= endFrame:
                endIndex += 1

        return mostRecentDay




class stockAPI():
#returns a new stock with dates from oldest point to current day
    def getNewStockDays(self, ticker):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token 2348473cfae1ffc4a9a473c3b575f750e32328ba'
        }
        endDate = datetime.date.today() - datetime.timedelta(days=1)
        endDate = endDate.__str__()
        requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/" + ticker + "/prices?startDate=2012-1-1&endDate=" + endDate,
                                       headers=headers)
        return requestResponse.json()

    def getNewStockMeta(self, ticker):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token 2348473cfae1ffc4a9a473c3b575f750e32328ba'
        }
        requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/" + ticker,
                                       headers=headers)
        return requestResponse.json()

    def updateStock(self, ticker, lastDate):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token 2348473cfae1ffc4a9a473c3b575f750e32328ba'
        }
        lastDate = lastDate + datetime.timedelta(days=1)
        lastDate = lastDate.__str__()
        endDate = datetime.date.today() - datetime.timedelta(days=1)
        endDate = endDate.__str__()
        requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/" + ticker + "/prices?startDate=" + lastDate + "&endDate=" + endDate,
                                       headers=headers)
        return requestResponse.json()


    def createNewStock(self, ticker):
        meta = self.getNewStockMeta(ticker)
        if not meta:
            return None
        elif not 'startDate' in meta:
            return None
        stock = Stock()
        stock.stock_name = ticker
        stock.start_date = self.parseMetaDate(meta['startDate'])
        stock.end_date = self.parseMetaDate(meta['endDate'])
        stock.company_meta = meta['description']
        stock.company_name = meta['name']
        stock.save()
        mostRecentDay = self.addNewDays(stock, None)
        if not mostRecentDay:
            return stock
        stock.current_high = mostRecentDay['high']
        stock.current_low = mostRecentDay['low']
        stock.end_date = self.parseDate(mostRecentDay['date'])
        stock.save()
        return stock

    def updateStockWithDays(self, stock):
        lastDate = stock.end_date
        mostRecentDay = self.addNewDays(stock, lastDate)
        if not mostRecentDay:
            return stock
        stock.end_date = self.parseDate(mostRecentDay['date'])
        stock.current_low = mostRecentDay['low']
        stock.current_high = mostRecentDay['high']
        stock.current_adjusted_close = mostRecentDay['adjClose'] if mostRecentDay['adjClose'] else mostRecentDay['close']
        stock.save()
        return stock

    def addNewDays(self, stock, lastDate):
        if lastDate:
            days = self.updateStock(stock.stock_name, lastDate)
        else:
            days = self.getNewStockDays(stock.stock_name)
        mostRecentDay = None
        for day in days:
            newDay = Stock_Day()
            newDay.stock = stock
            newDay.high = day['high']
            newDay.low = day['low']
            newDay.day = self.parseDate(day['date'])
            newDay.open = day['open']
            newDay.close = day['close']
            newDay.volume = day['volume']
            newDay.adjustedClose = day['adjClose'] if day['adjClose'] else day['close']
            newDay.save()
            mostRecentDay = day
        return mostRecentDay

    def parseDate(self, date):
        date = date[0:10]
        return datetime.datetime.strptime(date, '%Y-%m-%d')

    def parseMetaDate(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d')

    def getStock(self, ticker):
        ticker = ticker.lower()
        try:
            ## see if stock exists in database
            # stock = Stock.objects.get(stock_name=ticker)

            # NEW CODE BY CHRIS
            stock = Stock.objects.filter(stock_name=ticker)
            if len(stock) > 1:
                keep = stock[-1]
                for s in stock[:-1]:
                    s.delete()
                stock = keep
            elif len(stock) == 1:
                stock = stock[0]
            else:
                stock = self.createNewStock(ticker)
            # END NEW CODE BY CHRIS

        except Stock.DoesNotExist:
            # if stock does not exist
            stock = self.createNewStock(ticker)
        else:
            current_date = datetime.date.today()
            if stock.end_date < current_date:
                stock = self.updateStockWithDays(stock)
        return stock
