# basic_computations.py
# November 2016
# CPSC 537
#
# This file handles the basic computations of
# TSR and diversity scores over a given time
# period.

import numpy as np

def compute_tsr(stock_prices, num_shares):

    """
    Computes the Total Stock Return (TSR) for a given portfolio
    :param stock_prices
        a 2D numpy array where rows are stocks and columns are adjusted prices -- cannot contain np.nan
    :param num_shares
        a 1D numpy array that is the number of shares in each stock
    :return: tsr
        a 1D numpy array that is the tsr at each time.
    """

    # check for errors
    if np.any(np.isnan(stock_prices)):
        raise ValueError('Stock prices cannot contain NaN')
    if np.any(np.isnan(num_shares)):
        raise ValueError('Number of shares cannot contain NaN')
    if np.any(num_shares < 0):
        raise ValueError('Number of shares must be positive')
    if np.any(stock_prices < 0):
        raise ValueError('Stock prices must be nonnegative')

    # get first day prices
    n, p = stock_prices.shape
    first_day_price = stock_prices[:, 0].reshape(n, 1)

    # compute individual stock TSR
    num_shares = num_shares.reshape(num_shares.size, 1)
    individual_tsr = num_shares * ((stock_prices - first_day_price) / first_day_price)

    # sum for portfolio TSR
    tsr = np.sum(individual_tsr, axis=0)

    return tsr

def compute_diversity(stock_prices, num_shares):

    """
    Computes the diversity for a given portfolio
    :param stock_prices
        a 2D numpy array where rows are stocks and columns are prices -- cannot contain np.nan
    :param num_shares
        a 1D numpy array that is the number of shares in each stock
    :return: diversity
        a float that is the weighted average of correlation coefficients
    """

    if np.any(np.isnan(stock_prices)):
        raise ValueError('Stock prices cannot contain NaN')
    if np.any(np.isnan(num_shares)):
        raise ValueError('Number of shares cannot contain NaN')
    if np.any(num_shares <= 0):
        raise ValueError('Number of shares must be positive')
    if np.any(stock_prices < 0):
        raise ValueError('Stock prices must be nonnegative')
    if stock_prices.shape[0] <= 1:
        return 0

    n, p = stock_prices.shape

    # try adding small ammounts of random noise to avoid zero correlation coefficient
    stock_prices = stock_prices + 0.01 * np.random.rand(stock_prices.shape[0], stock_prices.shape[1])

    # get the matrix of correlation coefficients
    cor_mat = np.abs(np.corrcoef(x=stock_prices))
    cor_vec = cor_mat[np.triu_indices(n, k=1)]

    if np.any(np.isnan(cor_vec)):
        print('Whoah we reached an issue where cor_mat is nan')
        pass

    # get weight matrix
    num_shares = num_shares[:].astype(float)
    weight_mat = np.outer(num_shares, num_shares)
    weight_vec = weight_mat[np.triu_indices(n, k=1)]
    norm_weight_vec = weight_vec / np.sum(weight_vec)

    # get diversity score as weighted sum
    diversity_score = 1. - np.inner(cor_vec, norm_weight_vec)

    if not np.isreal(diversity_score):
        print('We reached an issue here where diversity is not real')
        pass

    return diversity_score