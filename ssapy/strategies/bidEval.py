"""
This is /ssapy/strategies/evaluators.py

Author: Brandon A. Mayer
Date: 1/9/2013
"""
from ssapy.pricePrediction.jointGMM import expectedSurplus_
import numpy

def bidEvalS(bundleRevenueDict, candidateSamples, evalSamples, ret='bid'):
    
    maxSurplus = 0.0
    bid = numpy.zeros(candidateSamples.shape[1])
    
    for candidateSample in candidateSamples:
        es = expectedSurplus_(bundleRevenueDict, 
                              numpy.atleast_1d(candidateSample), 
                              evalSamples)
        
        if es > maxSurplus:
            bid = numpy.atleast_1d(candidateSample)
            maxSurplus = es
            
    if ret == 'bid':
        return bid
    
    elif ret == 'all':
        return bid, maxSurplus