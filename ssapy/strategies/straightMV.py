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
import ssapy

def straightMV(**kwargs):
    pricePrediction = kwargs.get('pricePrediction')
    if pricePrediction == None:
        raise KeyError("Must specify pricePrediction")
    
    revDict = kwargs.get('revDict')
    if revDict == None:
        raise KeyError("Must specify revDict.")
    
    pricePrediction = numpy.atleast_1d(pricePrediction)
    
    bundles = numpy.atleast_2d(revDict.keys())
    
    valuation = numpy.atleast_1d(revDict.values())
        
    n_goods = bundles.shape[1]
    marginalValueBid = numpy.zeros(n_goods,dtype=numpy.float64)
    for goodIdx in xrange(n_goods):
        marginalValueBid[goodIdx] = \
                ssapy.marginalUtility(bundles, pricePrediction,
                                      valuation, goodIdx) 
    return marginalValueBid