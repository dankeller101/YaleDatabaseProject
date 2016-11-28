# basic_computations.py
# November 2016
# CPSC 537
#
# This file handles the basic computations of
# TSR and diversity scores over a given time
# period.

import numpy as np

def compute_tsr(stock_prices, dividends, num_shares):

    """
    Computes the Total Stock Return (TSR) for a given portfolio
    :param stock_prices
        a 2D numpy array where rows are stocks and columns are prices
    :param dividends
        a 2D numpy array where rows are stocks and columns are dividends paid since purchase (cummulative)
    :param num_shares
        a 1D numpy array that is the number of shares in each stock
    :return: tsr
        a 1D numpy array that is the tsr at each time.
    """

    # check for errors
    if np.any(num_shares < 0):
        raise ValueError('Number of shares must be nonnegative')
    if np.any(stock_prices < 0):
        raise ValueError('Stock prices must be nonnegative')
    if np.any(dividends < 0):
        raise ValueError('Dividends must be nonnegative')
    if np.any(np.diff(dividends) < 0):
        raise ValueError('Dividends must be monotonically increasing')

    # get first day prices
    n, p = stock_prices.shape
    first_day_price = stock_prices[:, 0].reshape(n, 1)

    # compute individual stock TSR
    num_shares = num_shares.reshape(num_shares.size, 1)
    individual_tsr = num_shares * ((stock_prices - first_day_price + dividends) / first_day_price)

    # sum for portfolio TSR
    tsr = np.sum(individual_tsr, axis=1)

    return tsr

def compute_diversity(stock_prices, num_shares):

    """
    Computes the diversity for a given portfolio
    :param stock_prices
        a 2D numpy array where rows are stocks and columns are prices
    :param num_shares
        a 1D numpy array that is the number of shares in each stock
    :return: diversity
        a float that is the weighted average of correlation coefficients
    """

    if np.any(num_shares < 0):
        raise ValueError('Number of shares must be nonnegative')
    if np.any(stock_prices < 0):
        raise ValueError('Stock prices must be nonnegative')

    n, p = stock_prices.shape

    # get the matrix of correlation coefficients
    cor_mat = np.abs(np.corrcoef(x=stock_prices))
    cor_vec = cor_mat[np.triu_indices(n, k=1)]

    # get weight matrix
    num_shares = num_shares[:].astype(float)
    weight_mat = np.outer(num_shares, num_shares)
    weight_vec = weight_mat[np.triu_indices(n, k=1)]
    norm_weight_vec = weight_vec / np.sum(weight_vec)

    # get diversity score as weighted sum
    diversity_score = 1. - np.inner(cor_vec, norm_weight_vec)

    return diversity_score