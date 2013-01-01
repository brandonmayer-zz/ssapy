"""
this is ssapy.strategies.targetMVS

Author: Brandon Mayer
Date: 11/18/2011

Specialized agent class to replicate targetMV* (hence MVS stands for MV Star) from
Yoon and Wellman (2011)

Modifications:
    Brandon A. Mayer - adapted strategy interface 1/1/2013
"""
import numpy
from ssapy.util import acq, marginalUtility
def targetMVS(bundles, revenue, pricePrediction, verbose = False):

    ppView      = numpy.atleast_1d(pricePrediction).astype('float')
    
    optBundle = acq(bundles, revenue, pricePrediction, verbose)[0]
    
    ppCopy = ppView.copy()
    ppCopy[~optBundle] = numpy.float('inf')
    
    if verbose:
        print "Computing bid via targetMVS"
        print "Optimal Bundle = {0}".format(optBundle.astype('int'))
        print "Price Prediction Copy = {0}".format(ppCopy)
    
    bids = numpy.zeros(ppView.shape[0])
    
    for goodIdx in numpy.flatnonzero(optBundle == True):
        bids[goodIdx] = marginalUtility(bundles, revenue, ppCopy, goodIdx)
    
    if verbose:
        print "bids = {0}".format(bids)    
        
    return bids

if __name__ == "__main__":
    from ssapy.util import listBundles
    from ssapy.marketSchedule import listRevenue
    
    pp = [5,5]
    l = 1
    v = [20,10]
    bundles = listBundles(2)
    rev = listRevenue(bundles, v, l)
    
    print bundles
    print rev
    
    targetMVS(bundles,rev,pp,True)
            
    
    