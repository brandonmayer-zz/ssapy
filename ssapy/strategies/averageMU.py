"""
this is /ssapy/strategies/averageMU.py

Author Brandon A. Mayer
Date:  11/21/2011


Modified:
    Brandon A. Mayer - 1/1/2012 Adapted from agent
"""
import numpy
from ssapy.strategies.straightMV import straightMV

def averageMU(bundles, revenue, pricePrediction, nSamples, verbose = False):
    if verbose:
        print "averageMU - Drawing {0} samples.".format(nSamples)
        
    bundleView = numpy.atleast_2d(bundles)
    
    samples = pricePrediction.sample(n_samples = nSamples)
    accum = numpy.zeros(bundleView.shape[1], dtype = 'float')
    
    #accumulate sum
    for sample in samples:
        accum += straightMV(bundles, revenue, sample, verbose)
        
    #divide by number of samples for average
    accum /= nSamples
    
    if verbose:
        print "bid = {0}".format(accum)
        
    return accum
    
def averageMU8(bundles, revenue, pricePrediction, verbose = False):
    return averageMU(bundles, revenue, pricePrediction, 8, verbose)

def averageMU64(bundles, revenue, pricePrediction, verbose = False):
    return averageMU(bundles, revenue, pricePrediction, 64, False)

def averageMU256(bundles, revenue, pricePrediction, verbose = False):
    return averageMU(bundles, revenue, pricePrediction, 256, False)