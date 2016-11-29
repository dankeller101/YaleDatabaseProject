

import requests
import datetime
from .models import Stock, Stock_Day


class stockDayDatabaseInterface():
    def getAllDaysOrdered(self, stock):
        days = Stock_Day.objects.order_by('day').get(stock=stock)
        return days

    def getSpecificDay(self, stock, dayRequested):
        day = Stock_Day.get(stock=stock, day=dayRequested)
        return day

    def getRangeDaysOrdered(self, stock, earliestDate, LatestDate):
        days = Stock_Day.objects.order_by('day').filter(day__lte=LatestDate).filter(day__gte=earliestDate).get(stock=stock)
        return days

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
        stock.current_high = mostRecentDay['high']
        stock.current_low = mostRecentDay['low']
        stock.end_date = self.parseDate(mostRecentDay['date'])
        stock.save()
        return stock

    def updateStockWithDays(self, stock):
        lastDate = stock.end_date
        mostRecentDay = self.addNewDays(stock, lastDate)
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
