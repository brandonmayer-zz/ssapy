import numpy

from ssapy import acq, marginalUtility

def targetMV(**kwargs):
    pricePrediction = kwargs.get('pricePrediction')
    
    if pricePrediction == None:
        raise KeyError("Must specify pricePrediction.")
    
    
    bundles = kwargs.get('bundles')
    if bundles == None:
        raise KeyError("Must specify bundles.")
    
    valuation = kwargs.get('valuation')
    if valuation == None:
        raise KeyError("Must specify valuation.")
    
    
    verbose = kwargs.get('verbose', False)
    
    [optBundle, optSurplus] = acq(bundles     = bundles,
                                  valuation   = valuation,
                                  priceVector = pricePrediction)
    
    if verbose:
        print "optBundle  = {0}".format(optBundle)
        print "optSurplus = {0}".format(optSurplus)
        
    n_goods = bundles.shape[1]
    bid = numpy.zeros(n_goods, dtype = numpy.float)
    
    for goodIdx, good in enumerate(optBundle):
        if good:
            bid[goodIdx] = marginalUtility(bundles, pricePrediction, valuation, goodIdx)
            
    if verbose:
        print "bid = {0}".format(bid)
        
    return bid

if __name__ == "__main__":
    import ssapy
    from ssapy.marketSchedule import listRevenue
    
    pp = [5,5]
    
    bundles = ssapy.allBundles(2)
    
    l = 1
    v = [20, 10]
    
    valuation = listRevenue(bundles, v, l)
    
    print bundles
    print valuation
    
    bid = targetMV(bundles = bundles, valuation = valuation, pricePrediction = pp, verbose = True)
    
    