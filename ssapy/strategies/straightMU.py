"""
this is /ssapy/strategies/straightMU

Author: Brandon Mayer
Date:   11/21/2011

Modified:
    Brandon Mayer - 10/30/2012 - Moved to ssapy.strategies

Specialized agent class to replicate straightMU from Yoon and Wellman 2011.
This is just a wrapper around targetMV and accepts a price prediction distribution
and calculates the mean(s) for price prediction
"""

from ssapy.strategies.straightMV import straightMV

import numpy

def straightMU(bundles, revenue, pricePrediction, n_samples, verbose = False):
    
    if verbose:
        print "straightMU - Drawing {0} samples.".format(n_samples)
        
    samples = pricePrediction.sample(n_samples = n_samples)
    
    if verbose:
        print "Samples:"
        print "{0}".format(samples)
    
    expectedPrices = numpy.mean(samples, 0)
    
    if verbose:
        print "Expected Price Vector: {0}".format(expectedPrices)
    
    return straightMV( bundles, revenue, expectedPrices, verbose)

def straightMUa(bundles, revenue, pricePrediction, verbose = False):
    if verbose:
        print "straightMUa"
        
    expectedPrices = pricePrediction.expectedValue()
    
    return straightMV(bundles, revenue, expectedPrices, verbose)

def straightMU8(bundles, revenue, pricePrediction, verbose = False):
    """
    Compute straight marginal value bid by sampling from a distribution
    (8 samples) to compute an expected price vector.
    """
    return straightMU(bundles, revenue, pricePrediction, 8, verbose)
    
def straightMU64(bundles, revenue, pricePrediction, verbose = False):
    """
    Compute straight marginal value bid by sampling from a distribution
    (64 samples) to compute an expected price vector.
    """   
    return straightMU(bundles, revenue, pricePrediction, 64, verbose)

def straightMU256(bundles, revenue, pricePrediction, verbose = False):
    """
    Compute straight marginal value bid by sampling from a distribution
    (256 samples) to compute an expected price vector.
    """   
    
    return straightMU(bundles, revenue, pricePrediction, 256, verbose)
    
    