import numpy

from ssapy.util import acq, marginalUtility, listBundles

def targetMV(bundles, revenue, pricePrediction, verbose = False):
    """
    Returns bid according to targetMV strategy.
    1) solve for optimal bundle
    2) for all goods in optimal bundle, bid marginal utility for that good.
    """
    
    b = numpy.atleast_2d(bundles)
    
    rev = numpy.atleast_1d(revenue)
    
    pp = numpy.atleast_1d(pricePrediction)
    
    
    [optBundle, optSurplus] = acq(b, rev, pp)
                                  
    
    if verbose:
        print "optBundle  = {0}".format(optBundle)
        print "optSurplus = {0}".format(optSurplus)
        
    n_goods = bundles.shape[1]
    bid = numpy.zeros(n_goods, dtype = numpy.float)
    
    for goodIdx, good in enumerate(optBundle):
        if good:
            bid[goodIdx] = marginalUtility(bundles, valuation, 
                                           pricePrediction, goodIdx)
            
    if verbose:
        print "bid = {0}".format(bid)
        
    return bid

if __name__ == "__main__":
    from ssapy.agents.marketSchedule import listRevenue
    
    pp = [5,5]
    
    bundles = listBundles(2)
    
    l = 1
    v = [20, 10]
    
    valuation = listRevenue(bundles, v, l)
    
    print bundles
    print valuation
    
    bid = targetMV(bundles, valuation, pp, True)
    
    