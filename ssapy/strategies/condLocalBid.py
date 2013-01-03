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
        newBid     := (float) the new bid for the target good
    """
    
    newBid = 0.0
        
    goodsWon = samples <= bids
    
    normWon = numpy.count_nonzero(goodsWon[:,targetBid] == True)
    normLost = numpy.count_nonzero(goodsWon[:,targetBid] == False)
    
    posIdxList = numpy.flatnonzero(bundles[:,targetBid] == True)
    
    for posIdx in posIdxList:
        posBundle = bundles[posIdx,:]
        negBundle = posBundle.copy()
        negBundle[targetBid] = False
        negIdx = numpy.where((bundles == negBundle).all(axis=1))[0][0]
        
        p1 = numpy.count_nonzero( numpy.all(goodsWon == posBundle, 1) ) + 1
        p1 = numpy.float(p1) / (normWon + 2)
        
        if p1 > 1.0:
            raise ValueError ("p1 = {0} > 1.0".format(p1))
        
        if p1 < 0.0:
            raise ValueError("p1 = {0} < 0.0".format(p1))
        
        p0 = numpy.count_nonzero( numpy.all(goodsWon == negBundle, 1) ) + 1 
        p0 = numpy.float(p0) / ( normLost +  2 )
        
        if p0 > 1.0:
            raise ValueError ("p0 = {0} > 1.0".format(p1))
        
        if p0 < 0.0:
            raise ValueError("p0 = {0} < 0.0".format(p1))
        
    
        newBid += (revenue[posIdx]*p1) - (revenue[negIdx]*p0)
        
    return newBid

def condLocal(bundles, revenue, initialBids, samples, maxItr = 100, tol = 1e-5, verbose = False):
    """
    Starting form an initial bid, run the condLocal algorithm and return 
    an updated bid vector.
    
    Use the following convention:
        Iteration - consists of m updates where m is the number of goods
        Update - an update for a single bid.
    
    INPUTS
    ------
    bundles     := (2d array-like) List of bundles
        
    revenue     := (1d array-like) List of revenue (1:1 correspondence with bundles)
    
    initialBids := (1d array-like) List of initial bids, 1 per good at auction.
                    bundles.shape[1] = initialBids.shape[0]
                    
    samples     := (2d array-like; shape = (nSamples x nGoods)) A list of samples from a 
                    price distribution.
                    
    maxItr      := (int) Stop updating after maxItr iterations. If maxItr is reached,
                    the algorithm is said to have diverged.
    
    tol         := (float) If the Euclidean distance between iterations 
                    (an update has been performed to each of the m bids)
                    is less than tol, the algorithm is said to have converged 
                    and returns the updated bid vector.
    
    OUTPUTS
    -------
    obids        := (1d array-like) A list of bids - one for each good.
    
    converged    := (boolean) A flag indicating convergence.
    
    itr          := The number of Iterations (impying n*iterations updates were performed)
                    performed. If converged = False -> itr = maxItr.
                    
    l            := Euclidean distance between the last update step 
                    and the previous state of the bid vector.
    """
    m = bundles.shape[1]
    obids = numpy.atleast_1d(initialBids).copy()
    converged = False
    
    for itr in xrange(maxItr):
        oldBid = obids.copy()
        
        for gIdx in xrange(m):
            obids[gIdx] = condLocalUpdate(bundles, revenue, obids, gIdx, samples, verbose)
        
        l = numpy.dot(oldBid - obids, oldBid - obids)
        
        if l <= tol:
            converged = True
            break
        
    return obids, converged, itr, l   

def plotCondLocal(bundles, revenue, initialBids, samples, maxItr, tol, filename = None, verbose = True):
    import matplotlib.pyplot as plt
    
    GREY = numpy.atleast_1d([169.,169.,169.])/255
    RED  = numpy.atleast_1d([255,0,0])/255
    
    m = bundles.shape[1]
    
    if (m != 2):
        raise KeyError("Can only visualize updates for auctions with 2 goods")
    
    obids = numpy.atleast_1d(initialBids).copy()
    converged = False
    
    plt.scatter(samples[:,0],samples[:,1], alpha=0.75)
    
    for itr in xrange(maxItr):
        oldBid = obids.copy()
        
        plt.plot(oldBid[0],oldBid[1],color=GREY)
        
        for gIdx in xrange(m):
            obids[gIdx] = condLocalUpdate(bundles, revenue, obids, gIdx, samples, verbose)
            
        plt.plot(obids[0],obids[1],color=RED)
            
        l = numpy.dot(oldBid - obids, oldBid - obids)
        
        if l <= tol:
            converged = True
            break
    
    plt.show()
        
    return obids, converged, itr, l  
    