# recommender_algorithms.py
# November 2016
# CPSC 537
#
# This file contains the three recommender algorithms
# that are used for the "Portfolio Playground" app.
# They are as follows:
#   (i) Random -- recommend a random portfolio under a budget
#   (ii) High Return -- recommend a portfolio with high expected TSR
#   (iii) Diverse -- recommend a diverse portfolio
# Depending on the computational limits, we may run this only on
# popular stocks.

import numpy as np
import random
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.vector_ar import var_model

def recommend_random_portfolio(stock_ids, stock_prices, budget, max_investment=None, **kwargs):

    """
    Recommends a portfolio by randomly selecting stocks, and then number of shares.
    :param stock_ids:
        a list of stock names
    :param stock_prices:
        a 1D numpy array of adjusted stock prices to be considered
    :param budget:
        a float that is the maxmimum amount to be invested in the portfolio
    :param max_investment:
        a float that is the maximum amount to invest in any one stock. Default is no limit
    :return: portfolio
        a dictionary where keys are stock ids and values are the number of shares

    """

    # check for bad inputs
    if np.any(stock_prices < 0):
        raise ValueError('Stock prices must be nonnegative')
    if budget < 0:
        raise ValueError('Budget must be nonnegative')
    if max_investment and max_investment < 0:
        raise ValueError('Max investment must be nonnegative')

    # if max_investment is none, place it as infinity
    if not max_investment:
        max_investment = np.inf

    n = stock_prices.size

    # initialize portfolio and initial budget
    portfolio = {}
    potential_stocks = set(range(n))
    current_budget = budget

    # continually add random choices until we run out of budget or options
    while True:

        # randomly sample a stock, get price, maximum number of shares we can purchase
        i = random.choice(tuple(potential_stocks))
        price = stock_prices[i]
        max_shares = int(np.floor(min(current_budget, max_investment) / price))

        # break if we reach a stock that we cannot afford a single share
        if max_shares == 0:
            break
        else:

            # if this is the last stock, add all of it
            if len(potential_stocks) == 1:
                portfolio[stock_ids[i].stock_name] = (max_shares, price)
                break
            else:
                # select random number of shares, remove stock from potential stocks
                num_shares = np.random.randint(1, max_shares+1)
                portfolio[stock_ids[i].stock_name] = (num_shares, price)
                potential_stocks.remove(i)

    return portfolio

def preprocessing_steps(stock_prices, normalize=True, log=True):

    n, p = stock_prices.shape

    # take the log first
    if log:
        stock_prices += 1.0 # add 1 across the board for log
        stock_prices = np.log(stock_prices)

    # then normalize the data -- take care to not run into divide by zero issues
    if normalize:
        stock_prices_mean = np.mean(stock_prices, axis=1).reshape(n, 1)
        stock_prices_var = np.std(stock_prices, axis=1).reshape(n, 1)
        ind_zero_var = np.argwhere(stock_prices_var == 0)
        stock_prices_var[ind_zero_var] = 1.0

        # normalization step
        stock_prices = (stock_prices - stock_prices_mean) / stock_prices_var
    else:
        stock_prices_mean = None
        stock_prices_var = None

    return stock_prices, stock_prices_mean, stock_prices_var

def postprocessing_steps(stock_prices, normalize=True, log=True, mean=None, var=None):

    if normalize:
        if (mean is None) or (var is None):
            raise ValueError('If normalizing, mean and var must be given')
        stock_prices = (stock_prices * var) + mean

    if log:
        stock_prices = np.exp(stock_prices)
        stock_prices -= 1.0

    return stock_prices

def forecast_stock_price_arima(stock_prices, time_horizon):

    # I've transposed some stuff -- check it out
    n, p = stock_prices.shape

    # HARD CODED PARAMETERS - not the statistically best thing, but it's a good start
    order_p = 5  # hard coded to choose a working week for lag terms
    order_d = 2  # hard coded to choose the second derivative
    order_q = 1  # hard coded to choose one smoothing term

    # fit model
    stock_prices_t = np.transpose(stock_prices)
    arima_mod = ARIMA(stock_prices_t, order=(order_p, order_d, order_q))
    results = arima_mod.fit()

    # predict price from the last data point to the time horizon
    forecasted_price_t = results.predict(start=p, end=p + time_horizon, dynamic=True)
    forecasted_price = np.transpose(forecasted_price_t)

    return forecasted_price

def forecast_stock_price_var(stock_prices, time_horizon, max_order=5):

    # transpose this sucker
    stock_prices_t = np.transpose(stock_prices)

    # select optimal order
    var_mod = var_model.VAR(stock_prices_t)
    order = var_mod.select_order(max_order)
    opt_order = order['aic']

    # fit data with optimal order
    results = var_mod.fit(maxlags=opt_order)

    # predict price to time horizon
    forecasted_price_t = results.forecast(stock_prices_t, time_horizon)
    forecasted_price = np.transpose(forecasted_price_t)

    return forecasted_price

def forecast_price(stock_prices, time_horizon, model='arima', max_order=20, preprocess=False):

    # pre-process the data
    if preprocess:
        processed_stock_prices, stock_mean, stock_var = preprocessing_steps(stock_prices, log=True, normalize=True)
    else:
        processed_stock_prices = stock_prices

    # build the model and forecast the prices
    if model is 'arima':
        forecasted_prices = forecast_stock_price_arima(processed_stock_prices, time_horizon)  # ARIMA
    elif model is 'var':
        forecasted_prices = forecast_stock_price_var(processed_stock_prices, time_horizon)  # VAR
    else:
        raise ValueError('Model %s is not supported' % model)

    # post-process the data
    if preprocess:
        forecasted_prices = postprocessing_steps(forecasted_prices, normalize=True, log=True, mean=stock_mean, var=stock_var)

    return forecasted_prices

def recommend_high_return_portfolio(stock_ids, stock_prices, budget, time_horizon=14, max_investment=None, model='var', preprocess=True):

    """
    Recommends a portfolio by fitting an autoregressive integrated moving average (ARIMA) model to stock prices,
    forecasting to a further time horizon, and then greedily choosing those stocks with highest forecasted total
    stock return.
    :param stock_ids:
        a list of stock names
    :param stock_prices:
        a 2D numpy array where rows are stocks and columns are adjusted stock prices
    :param budget:
        a float that is the maxmimum amount to be invested in the portfolio
    :param time_horizon:
        a int that is the number of days to predict out to. Default is 14 days.
    :param max_investment:
        a float that is the maximum amount to invest in any one stock. Default is no limit.
    :return: portfolio
        a dictionary where keys are stock ids and values are the tuple (number of shares, price)

    """

    # check for bad inputs
    if np.any(stock_prices < 0):
        raise ValueError('Stock prices must be nonnegative')
    if budget < 0:
        raise ValueError('Budget must be nonnegative')
    if time_horizon < 0:
        raise ValueError('Time Horizon must be nonnegative')
    if (max_investment is not None) and (max_investment < 0):
        raise ValueError('Max investment must be nonnegative')

    # set max_investment to budget if it is not given
    if max_investment is None:
        max_investment = budget

    # forecast the prices using model
    forecasted_prices = forecast_price(stock_prices, time_horizon=time_horizon, model=model, preprocess=preprocess)

    # compute the TSR
    first_price = stock_prices[:, 0]
    last_forecast_price = forecasted_prices[:, -1]
    single_share_tsr = (last_forecast_price - first_price) / first_price

    # initialize portfolio and initial budget
    portfolio = {}
    current_budget = budget
    scratch_tsr = single_share_tsr

    # continually add highest returns until we run out of budget or options
    while True:

        # select the highest predicted TSR, get price, maximum number of shares we can purchase
        i = np.argmax(scratch_tsr)
        price = stock_prices[i, -1] # most recent day
        max_shares = int(np.floor(min(current_budget, max_investment) / price))

        # break if we reach a stock that we cannot afford a single share
        if max_shares == 0:
            break
        else:

            # if this is the last stock, add all of it
            if np.sum(scratch_tsr != -np.inf) == 1:
                portfolio[stock_ids[i].stock_name] = (int(np.floor(current_budget / price)), price)
                break
            else:
                # select shares, remove from potential stocks, set tsr to negative
                portfolio[stock_ids[i].stock_name] = (max_shares, price)
                scratch_tsr[i] = -np.inf
                current_budget -= max_shares * price

    return portfolio

def recommend_diverse_portfolio(stock_ids, stock_prices, budget, time_horizon=14, max_investment=None, diverse_thresh=0.2, model='var', preprocess=True):
    """
        Recommends a portfolio by fitting an autoregressive integrated moving average (ARIMA) model to stock prices,
        forecasting to a further time horizon. Next, the correlation matrix is chosen. Stocks are greedily chosen such
        that they are (i) diverse with stocks already in the portfolio (ii) have high forecasted TSR.
        :param stock_ids:
            a list of stock names
        :param stock_prices:
            a 2D numpy array where rows are stocks and columns are adjusted stock prices
        :param budget:
            a float that is the maxmimum amount to be invested in the portfolio
        :param time_horizon:
            a int that is the number of days to predict out to. Default is 14 days.
        :param max_investment:
            a float that is the maximum amount to invest in any one stock. Default is no limit.
        :param diverse_thresh:
            a float that is the maximum amount of correlation allowed between pairs in the portfolio. Default is 0.2
        :return: portfolio
            a dictionary where keys are stock ids and values are the number of shares

        """

    # check for bad inputs
    if np.any(stock_prices < 0):
        raise ValueError('Stock prices must be nonnegative')
    if budget < 0:
        raise ValueError('Budget must be nonnegative')
    if time_horizon < 0:
        raise ValueError('Time Horizon must be nonnegative')
    if (max_investment is not None) and (max_investment < 0):
        raise ValueError('Max investment must be nonnegative')

    # set max_investment to budget if it is not given
    if max_investment is None:
        max_investment = budget

    n, p = stock_prices.shape

    # forecast the prices using model
    forecasted_prices = forecast_price(stock_prices, time_horizon=time_horizon, model=model, preprocess=preprocess)

    # compute the TSR
    first_price = stock_prices[:, 0]
    last_forecast_price = forecasted_prices[:, -1]
    single_share_tsr = (last_forecast_price - first_price) / first_price

    # get the matrix of correlation coefficients
    cor_mat = np.abs(np.corrcoef(x=stock_prices))

    # initialize portfolio and initial budget
    portfolio = {}
    port_ind = []
    current_budget = budget
    scratch_tsr = single_share_tsr

    # continually add diverse but high returns until we run out of budget or options
    while True:

        # get the diverse options with respect to the current portfolio
        if not portfolio:
            diverse_options = [i for i in range(n)]
        else:
            diverse_options = [i for i in diverse_options if np.min(cor_mat[i, port_ind]) < diverse_thresh]

        # break if there are no more diverse options
        if not diverse_options:
            print('Warning: Only %d diverse options were found with a threshold of %.3f' % (len(portfolio), diverse_thresh))
            break

        # else, choose the diverse option with the highest forecasted TSR
        i = diverse_options[np.argmax(scratch_tsr[diverse_options])]
        price = stock_prices[i, -1]  # most recent day
        max_shares = int(np.floor(min(current_budget, max_investment) / price))

        # break if we reach a stock that we cannot afford a single share
        if max_shares == 0:
            break
        else:

            # if this is the last stock, add all of it
            if len(diverse_options) == 1:
                portfolio[stock_ids[i].stock_name] = (int(np.floor(current_budget / price)), price)
                break
            else:
                # select shares, remove from diverse options, add to portfolio indices, put tsr as lowest
                portfolio[stock_ids[i].stock_name] = (max_shares, price)
                diverse_options.remove(i)
                port_ind.append(i)
                scratch_tsr[i] = -np.inf
                current_budget -= max_shares * price

    return portfolio

