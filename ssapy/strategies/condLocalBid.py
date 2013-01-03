"""
Conditional Local Bidder strategy

Author: Brandon A. Mayer
Date: 1/2/2013 (adapted from ssapy.agents.condLocalBid)
"""

import numpy

def condLocalUpdate(bundles, revenue, bids, targetBid, samples, verbose = False):
    """
    Update a single bid index, targetBid, of bids given a set of samples and a 
    revenue function described by bundle - revenue pairs.
    
    INPUTS
    ------
        bundles    := (2d array-like) List of bundles
        
        revenue    := (1d array-like) List of revenue (1:1 correspondence with bundles)
        
        bids       := (1d array-like) List of bids. 
        
                        bids.shape[0] = bundles.shape[1]
        targetBid  := (int) the (zero-indexed) bid to be updated.
        
        samples    := (2d array-like) List of samples
                        samples.shape[0] = nSamples, samples.shape[1] = m (number of goods)
        
        verbose    := (boolean) output debugging info to stdout.
        
    OUTPUTS
    -------
        ubids       := (1d array like) updated bid vector
    """
    
    newBid = 0.0
        
    goodsWon = samples <= bids
    
    normWon = numpy.count_nonzero(goodsWon[:,targetBid] == True)
    normLost = numpy.count_nonzero(goodsWon[:,targetBid] == False)
    
    posIdxList = bundles[:,targetBid] == True
    
    for posIdx in posIdxList:
        posBundle = bundles[posIdx,:]
        negBundle = posBundle.copy()
        negBundle[targetBid] = False
        negIdx = numpy.where((bundles == negBundle).all(axis=1))[0]
        
        p1 = numpy.count_nonzero( numpy.all(goodsWon == posBundle, 1) ) + 1
        p1 = numpy.float(p1) / (normWon + 2)
        
        if p1 > 1.0:
            raise ValueError ("p1 = {0} > 1.0".format(p1))
        
        if p1 < 0.0:
            raise ValueError("p1 = {0} < 0.0".format(p1))
        
        p0 = numpy.count_nonzero( numpy.all(goodsWon == negBundle, 1) ) + 1 
        p0 = numpy.float(p0) / ( normLost +  1 )
        
        if p0 > 1.0:
            raise ValueError ("p0 = {0} > 1.0".format(p1))
        
        if p0 < 0.0:
            raise ValueError("p0 = {0} < 0.0".format(p1))
        
    
        newBid += (revenue[posIdx]*p1) - (revenue[negIdx]*p0)
        
    obid = bids.copy()
    
    obid[targetBid] = newBid
    
    return obid
    