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

def straightMU(**kwargs):
    pricePrediction = kwargs.get('pricePrediction')
    if pricePrediction == None:
        raise KeyError("Must specify pricePrediction.")
    
    revDict = kwargs.get('revDict')
    if revDict == None:
        raise KeyError("Must specify  revDict.")
        
    n_samples = kwargs.get('n_samples')
    if n_samples == None:
        raise KeyError("Must specify number of samples")
    
    samples = pricePrediction.sample(n_samples = n_samples)
    
    expectedPrices = numpy.mean(samples, 0)
    
    return straightMV( pricePrediction = expectedPrices,
                       revDict         = revDict)
  
def straightMU8(**kwargs):
    """
    Calculate the expected using inverse sampling method and 8 samples
    Then bid via straightMV with the resulting expected prices
    """
    
    kwargs.update(n_samples = 8)
    
    return straightMU(**kwargs)
    
def straightMU64(**kwargs):
    
    kwargs.update(n_samples = 64)
    
    return straightMU(**kwargs)

def straightMU256(**kwargs):
    
    kwargs.update(n_samples = 256)
    
    return straightMU(**kwargs)
    
    