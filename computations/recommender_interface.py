# recommender_interface.py
# November 2016
# CPSC 537
#
# This file interfaces the front end user input to the backend, including
# database queries and recommendation algorithms algorithm calls.
#

import numpy as np
from recommender_algorithms import recommend_random_portfolio, recommend_high_return_portfolio, recommend_diverse_portfolio


def create_portfolio(user_id, portfolio_id, recommend_type='random', potential_stocks=None, num_observed_days=730, **kwargs):

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
    :return: updates the database to include the user's portfolio
    """

    # TODO: consider pulling data inside the recommender algorithm to avoid work for random recommender

    # raise error if recommend_type is not supported
    if recommend_type not in ['random', 'diverse', 'high_return']:
        raise ValueError('recommend_type not recognized')

    # TODO: if potential stocks are not given, choose top k=500 popular stocks
    if potential_stocks is None:
        # potential_stocks = [] # hard-coded list
        pass

    # TODO: query the database for the stock prices and dividends of potential stocks
    # from current time to number of observed days ago

    # TODO: clean the data -- remove NaN

    # TODO: put into format for recommender algorithms
    stock_ids = None # list of stock names
    stock_prices = None # 2D numpy array of stock prices


    # run desired recommender algorithm
    if recommend_type is 'random':

        current_stock_prices = stock_prices[:,0]
        portfolio = recommend_random_portfolio(stock_ids=stock_ids, stock_prices=current_stock_prices, **kwargs)

    elif recommend_type is 'high_return':

        portfolio = recommend_high_return_portfolio(stock_ids=stock_ids, stock_prices=stock_prices, **kwargs)

    elif recommend_type is 'diverse':

        portfolio = recommend_diverse_portfolio(stock_ids=stock_ids, stock_prices=stock_prices, **kwargs)

    # TODO: update the database with the portfolio for the user
    # this part uses the user_id and portfolio_id arguments

    return
