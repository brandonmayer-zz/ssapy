"""
this is /ssapy/strategies/targetMU.py

Author: Brandon Mayer
Date:   11/21/2011

Specialized agent class to replicate targetMU from Yoon and Wellman 2011.
This is just a wrapper around targetMV and accepts a price prediction distribution
and calculates the mean(s) for price prediction

Modified:
    Brandon A. Mayer - 1/31/2013 Adopted strategy interface 
    (moved from depreciated ssapy.agents).
"""
import numpy

from ssapy.strategies.targetMV import targetMV

def targetMU(bundles, revenue, pricePrediction, nSamples, verbose = False):
    """
    Computes bids as the marginal utility for each good contained in the optimal
    bundle according to acq (Boyan & Greenwald '01).
    
    Expected price vectors are computed from a distribution via inverse transform 
    sampling with the number of samples as a parameter of the algorithm.
    
    1) Sample pricePrediction using nSamples to compute expectedPrices
    2) Compute optimal bundle (wrt surplus) with expectedPrices
    3) for each good in optimal bundle, bid the marginal utility of the good else
       bid zero.
       
    Inputs
    ------
        bundles         :=    (2d array-like)
                              rows indicate individual bundles,
                              columns are individual goods.
                                 
        revenue         :=    (1d array-like)
                              an numpy array of revenue values, one for each bundle.
                              
        pricePrediction :=    (dok_hist, jointGMM, margDist)
                              a distribution with function sample(...) implemented.
                              
                              
        nSamples        :=    (int) number of samples used to compute expected
                              price vector.
                              
        verbose         :=    (bool) Flag to output debug info to stdout.
        
        
    Returns
    -------
        bids            :=    (1d array-like) vector of bids, one for each good.
                              bids.shape[0] = bundles.shape[1]
    """
    if verbose:
        print "targetMU"
        print "\tDrawing {0} price samples.".format(pricePrediction)
    
    samples = pricePrediction.sample(nSamples = nSamples)
    
    if verbose:
        print "\tSapmles:"
        print "{0}".format(samples)
        
    expectedPrices = numpy.mean(samples,0)
    if verbose:
        print "\tExpected Price Vector = {0}".format(expectedPrices)
        
    return targetMV( bundles, revenue, expectedPrices, verbose )
    
    
def targetMU8(bundles, revenue, pricePrediction, verbose):
    return targetMU(bundles, revenue, pricePrediction, 8, verbose)

def targetMU64(bundles, revenue, pricePrediction, verbose):
    return targetMU(bundles, revenue, pricePrediction, 64, verbose)

def targetMU256(bundles, revenue, pricePrediction, verbose):
    return targetMU(bundles, revenue, pricePrediction, 256, verbose)