"""
This is /auctionSimulator/pricePrediction/marginalDistributionFunctions.py

Author:    Brandon A. Myaer
Date:      11/26/2011

A file containing functions to process marginal distributions represented as
histograms over a set of goods
"""

import numpy
import matplotlib.pyplot as plt

           

def sampleItransform(priceDistribution = None, nSamples = None):
    samples = []
    nGoods = []
    
    if isinstance(priceDistribution,list):
        nGoods = len(priceDistributions)
    elif isinstance(priceDistribution,tuple):
        nGoods = 1
    else:
        print "----ERROR----"
        print "marginalPriceDistributionFunctions::"+\
            "sampleItransform(priceDistribution = {0} ,nSamples = {1})".format(priceDistribution,nSamples)
        print "Unknown distribution format"
        raise AssertionError
    
    samples = numpy.zeros( (nSamples,nGoods) ) 
    
    for col in xrange(nGoods):
        hist,binEdges = priceDistributions[col]
        
        #numpy.testing.assert_almost_equal(numpy.sum(  ), 1.0)