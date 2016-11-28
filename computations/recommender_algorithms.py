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
import statsmodels as sm
import gurobipy as gurobi

def recommend_random_portfolio(budget, max_per_stock, stock_ids, stock_prices):

    """

    :param budget:
        a float that is the maxmimum amount to be invested in the portfolio
    :param max_per_stock:
        a float that is the maximum amount to invest in any one stock
    :param stock_ids:
        a list of stock names
    :param stock_prices:
        a 1D numpy array of stock prices to be considered
    :return:
    """

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
        max_shares = int(np.floor(min(current_budget, max_per_stock) / price))

        # break if we reach a stock that we cannot afford a single share
        if max_shares == 0:
            break
        else:

            # if this is the last stock, add all of it
            if len(potential_stocks) == 1:
                portfolio[stock_ids[i]] = max_shares
                break
            else:
                # select random number of shares
                num_shares = random.choice(1, range(max_shares) + 1)
                portfolio[stock_ids[i]] = num_shares

    return portfolio

def recommend_high_return_portfolio():

    return

def recommend_diverse_portfolio():

    return

