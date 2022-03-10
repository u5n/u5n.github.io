""" Exponential distribution
"""
import numpy as np
import time
from math import *

"""
example1
    simulate bus arrive
"""

def simulate(total_timespan, n_passenger, expection_time):
    """
    args
        expection_time: example, avg 10 time unit per bus, then expection_time = 10
    """
    lam = 1/expection_time 
    n_bus = total_timespan // expection_time
    rng = np.random.RandomState(int(time.time()))
    passenger_arrive = total_timespan*rng.rand(n_passenger)
    bus_arrive = total_timespan*np.sort(rng.rand(n_bus))
    # add the last bus
    bus_arrive = np.append(bus_arrive, total_timespan)

    # time to meet first bus
    wait_time = bus_arrive[np.searchsorted(bus_arrive, passenger_arrive, 'left')] - passenger_arrive
    prob_can_get = lambda x: (wait_time<=x).sum()/n_passenger
    return prob_can_get


total_timespan = 8*60*10000
expection_time = 150
n_passenger = 1000000
prob_can_get = simulate(total_timespan, n_passenger, expection_time)
CDF = lambda x: 1-np.exp(-x/expection_time)
print(CDF(1), prob_can_get(1))
# print(CDF(30), prob_can_get(30))