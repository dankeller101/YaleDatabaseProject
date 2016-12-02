

import requests
import datetime
import numpy as np
import predict_my_money.computations.basic_computations
from .models import Stock, Stock_Day, Portfolio, Portfolio_Day, Stock_Owned


class stockDayDatabaseInterface():
    def getAllDaysOrdered(self, stock):
        days = Stock_Day.objects.order_by('day').filter(stock=stock)
        return days

    def getSpecificDay(self, stock, dayRequested):
        try:
            day = Stock_Day.objects.get(stock=stock, day=dayRequested)
        except Stock_Day.DoesNotExist:
            return None
        else:
            return day

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
            if portfolio.end_date < current_date:
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
        stockInterface = stockDayDatabaseInterface()
        stocks = Stock_Owned.objects.get(portfolio=portfolio)
        num_observed_days = today.date - earliest_day.date
        num_observed_days = num_observed_days.days

        #build 2d numpy array where each row = a stock, each column = a day
        stock_prices = np.empty((len(stocks), num_observed_days))
        stock_amounts = np.empty(len(stocks))
        lookup_date = earliest_day - datetime.timedelta(days=60)
        for i, stock in enumerate(stocks):
            days = stockInterface.getRangeDaysOrdered(stock.stock, lookup_date, today)
            stock_prices[i, :] = np.array([day.adjustedClose if day else np.nan for day in days])
            stock_amounts[i] = stock.amount_owned


        portfolioValues = np.sum(stock_prices, axis=0)
        mostRecentDay = None
        #create Portfolio_Day objects
        for index in range(num_observed_days):
            newPortDay = Portfolio_Day()
            newPortDay.portfolio = portfolio
            newPortDay.day = earliest_day + datetime.timedelta(days=index)
            newPortDay.value = portfolioValues[index + 60]
            newPortDay.diversity = predict_my_money.compute_diversity(stock_prices[:, index:index+60], stock_amounts)
            newPortDay.save()
            mostRecentDay = newPortDay

        return mostRecentDay


class stockAPI():
#returns a new stock with dates from oldest point to current day
    def getNewStockDays(self, ticker):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token 2348473cfae1ffc4a9a473c3b575f750e32328ba'
        }
        endDate = datetime.date.today().__str__()
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
        lastDate = lastDate.__str__()
        endDate = datetime.date.today().__str__()
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
            # see if stock exists in database
            stock = Stock.objects.get(stock_name=ticker)
        except Stock.DoesNotExist:
            # if stock does not exist
            stock = self.createNewStock(ticker)
        else:
            current_date = datetime.date.today()
            if stock.end_date < current_date:
                stock = self.updateStockWithDays(stock)
        return stock
