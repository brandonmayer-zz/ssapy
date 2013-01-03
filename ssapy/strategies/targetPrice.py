"""
this is ssapy.strategies.targetPrice

Author: Brandon Mayer
Date: 11/21/2011

Stragegy:
1) Determine optimal bundle via acq(...)
2) Bid price prediction for each good in optimal bundle

Modifications:
Adapted from ssapy.agents.targetPrice 1/1/2013
"""
import numpy
from ssapy.util import acq

def targetPrice(bundles, revenue, pricePrediction, verbose = False):
    bundleView  = numpy.atleast_2d(bundles)
    revenueView = numpy.atleast_1d(revenue)
    ppView      = numpy.atleast_1d(pricePrediction)
    
    if verbose:
        print "Computing bid via targetPrice strategy."

        
    optBundle = acq(bundleView, revenueView, ppView, verbose)[0]

    bid = ppView.copy()
    bid[~optBundle] = 0.0
    
    if verbose:
        print "Optimal Bundle   = {0}".format(optBundle)
        print "Price Prediction = {0}".format(ppView)
        print "bid              = {0}".format(bid)
        
    return bid

if __name__ == "__main__":
    from ssapy.util import listBundles
    from ssapy.agents.marketSchedule import listRevenue
    
    pp = [5,5]
    l = 1
    v = [20,10]
    bundles = listBundles(2)
    rev = listRevenue(bundles, v, l)
    
    print bundles
    print rev
    
    bid = targetPrice(bundles,rev,pp,True)
        
    
    