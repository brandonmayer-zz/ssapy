"""
this is /ssapy/strategies/straightMV.py

Author: Brandon Mayer
Date: 11/17/2011

Modified:
    Brandon Mayer 10/30/12 moved to ssapy.strategies

Specialized agent class to replicate straightMV from
Yoon and Wellman (2011)
"""

import numpy
from ssapy.util import marginalUtility

def straightMV(bundles, revenue, pricePrediction, verbose = False):
    b = numpy.atleast_2d(bundles)
    rev = numpy.atleast_1d(revenue)
    pp = numpy.atleast_1d(pricePrediction)
    
    n_goods = bundles.shape[1]
    marginalValueBid = numpy.zeros(n_goods,dtype=numpy.float64)
    for goodIdx in xrange(n_goods):
        marginalValueBid[goodIdx] = \
                marginalUtility(b,rev,pp,goodIdx)
                                 
    if verbose:
        print marginalValueBid
                                         
    return marginalValueBid

if __name__ == "__main__":
    from ssapy.util import listBundles
    from ssapy.marketSchedule import listRevenue
    
    pp = [5,5]
    bundles = listBundles(2)
    l = 1
    v = [20,10]
    rev = listRevenue(bundles, v, l)
     
    print bundles
    print rev
    
    bid = straightMV(bundles, rev,pp,True)

