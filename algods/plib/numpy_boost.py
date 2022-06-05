from math import inf
import numpy as np
def groupby(A):
    """ group A by its value use its difference """
    # min index of each groups; index[-1] == len(A)
    lends = np.diff(A, prepend=inf, append=inf).nonzero()[0]
    # number of groups
    len(lends) - 1 
    # size of groups 
    np.diff(lends)
    # array of groups           
    np.split(A, np.diff(A).nonzero()[0] + 1)