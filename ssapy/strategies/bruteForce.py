from ssapy.pricePrediction.jointGMM import expectedSurplus_
import numpy
import itertools

def bruteForceS( bundleRevenueDict,  evalSamples = None, min=0.0, max=50.0, step=1.0, ret='bid'):
    m = evalSamples.shape[1]
    
    xx = numpy.arange(min,max+1.0,step)
    
    maxSurplus = -numpy.float('inf')
    bid = None
    for c in itertools.product(xx,repeat=m):
        es = expectedSurplus_(bundleRevenueDict, numpy.atleast_1d(c), evalSamples)
        if es > maxSurplus:
            bid = numpy.atleast_1d(c)
            maxSurplus = es
            print bid
            print maxSurplus
            
    if ret == 'bid':
        return bid
    elif ret == 'all':
        return bid, maxSurplus