"""
Conditional Local Bidder strategy

Author: Brandon A. Mayer
Date: 1/2/2013 (adapted from ssapy.agents.condLocalBid)
"""

import numpy

def condLocalLimitUpdate(bundles, revenue, bids, 
                         targetBid, samples, eps = 1e-5, 
                         verbose = False):
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
    
    normWon = numpy.float(numpy.count_nonzero(goodsWon[:,targetBid] == True))
    normLost = numpy.float(numpy.count_nonzero(goodsWon[:,targetBid] == False))
    
    posIdxList = numpy.flatnonzero(bundles[:,targetBid] == True)
    
    for posIdx in posIdxList:
        posBundle = bundles[posIdx,:]
        negBundle = posBundle.copy()
        negBundle[targetBid] = False
        negIdx = numpy.where((bundles == negBundle).all(axis=1))[0][0]
        
#        p1 = numpy.count_nonzero( numpy.all(goodsWon == posBundle, 1) ) + eps
#        p1 = numpy.float(p1) / (normWon + 2*eps)
        if normWon == 0:
            p1 = 0.5
        else:
            p1 = numpy.float(numpy.count_nonzero( numpy.all(goodsWon == posBundle, 1) ) )
            if verbose:
                print '\t#({0}) = {1}'.format(posBundle, p1)
                print '\t#({0} = True) = {1}'.format(targetBid, normWon)
                 
            p1 /= normWon
            
        if verbose:
            print 'p({0} | {1} = True ) = {2}'.format(posBundle,targetBid,p1)
             
#        p1 = numpy.count_nonzero( numpy.all(goodsWon == posBundle, 1) )
#        p1 = numpy.float(p1) / (normWon + 1)
        if p1 > 1.0:
            raise ValueError ("p1 = {0} > 1.0".format(p1))
        
        if p1 < 0.0:
            raise ValueError("p1 = {0} < 0.0".format(p1))
        
#        p0 = numpy.count_nonzero( numpy.all(goodsWon == negBundle, 1) ) + eps
#        p0 = numpy.float(p0) / ( normLost +  2*eps )

        if normLost == 0:
            p0 = 0.5
        else:
#            p0 = numpy.float(numpy.count_nonzero( numpy.all(goodsWon == negBundle, 1) )) / normLost
            p0 = numpy.float(numpy.count_nonzero( numpy.all(goodsWon == negBundle, 1) ))
            if verbose:
                print '\t#({0}) = {1}'.format(negBundle, p0)
                print '\t#({0} = True) = {1}'.format(targetBid, normLost)
            
            p0 /= normLost
        
        if verbose:
            print 'p({0} | {1} = False) = {2}'.format(posBundle,targetBid,p0)
        
        if p0 > 1.0:
            raise ValueError ("p0 = {0} > 1.0".format(p0))
        
        if p0 < 0.0:
            raise ValueError("p0 = {0} < 0.0".format(p0))
        
    
        newBid += ((revenue[posIdx]*p1) - (revenue[negIdx]*p0))
        
    if verbose:
        print newBid
        
    return newBid

def condLocalLimit(bundles, revenue, initialBids, 
                   samples, maxItr = 100, tol = 1e-5, 
                   verbose = False, ret = 'bids'):
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
                    
    ret         := (string) Else return tuple:
                            (bids, converged (boolean), nItr (int), dist (float)) 
    
    OUTPUTS
    -------
    obids        := (1d array-like) A list of bids - one for each good.
    
    ONLY RETURNED IF ret == 'all'
    converged    := (boolean) A flag indicating convergence.
    
    itr          := The number of Iterations (impying n*iterations updates were performed)
                    performed. If converged = False -> itr = maxItr.
                    
    l            := Euclidean distance between the last update step 
                    and the previous state of the bid vector.
    """
    m = bundles.shape[1]
    newBids = numpy.atleast_1d(initialBids).copy()
    converged = False
    
    for itr in xrange(maxItr):
        oldBid = newBids.copy()
        
        for gIdx in xrange(m):
            newBids[gIdx] = condLocalLimitUpdate(bundles, revenue, newBids, gIdx, samples, verbose)
            
        d = numpy.linalg.norm(oldBid-newBids)
        
        if d <= tol:
            converged = True
            break
        
    if ret == 'bids':
        return newBids
    elif ret == 'all':
        return newBids, converged, itr + 1, d
    else:
        raise ValueError("Unknown Return Type.")

def condLocalUpdate(bundles, revenue, bids, 
                    targetBid, samples, eps = 1.0, 
                    verbose = False): 
                    
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
    
    normWon = numpy.float(numpy.count_nonzero(goodsWon[:,targetBid] == True))
    normLost = numpy.float(numpy.count_nonzero(goodsWon[:,targetBid] == False))
    
    posIdxList = numpy.flatnonzero(bundles[:,targetBid] == True)
    
    for posIdx in posIdxList:
        posBundle = bundles[posIdx,:]
        negBundle = posBundle.copy()
        negBundle[targetBid] = False
        negIdx = numpy.where((bundles == negBundle).all(axis=1))[0][0]
        
        p1 = numpy.count_nonzero( numpy.all(goodsWon == posBundle, 1) ) + eps
        
        if verbose:
            print '\t#({0}) = {1}'.format(posBundle, p1)
            print '\t#({0} = True) = {1}'.format(targetBid, normWon)
            
        p1 = numpy.float(p1) / (normWon + 2*eps)
        
           
        if verbose:
            print 'p({0} | {1} = True ) = {2}'.format(posBundle,targetBid,p1)
             

        if p1 > 1.0:
            raise ValueError ("p1 = {0} > 1.0".format(p1))
        
        if p1 < 0.0:
            raise ValueError("p1 = {0} < 0.0".format(p1))
        
        p0 = numpy.float(numpy.count_nonzero( numpy.all(goodsWon == negBundle, 1) )) + eps
        
        if verbose:
            print '\t#({0}) = {1}'.format(negBundle, p0)
            print '\t#({0} = True) = {1}'.format(targetBid, normLost)
            
        p0 = numpy.float(p0) / ( normLost +  2*eps )

        p0 = numpy.float(numpy.count_nonzero( numpy.all(goodsWon == negBundle, 1) ))
        
                
        if verbose:
            print 'p({0} | {1} = False) = {2}'.format(posBundle,targetBid,p0)
        
        if p0 > 1.0:
            raise ValueError ("p0 = {0} > 1.0".format(p0))
        
        if p0 < 0.0:
            raise ValueError("p0 = {0} < 0.0".format(p0))
        
    
        newBid += ((revenue[posIdx]*p1) - (revenue[negIdx]*p0))
        
    if verbose:
        print newBid
        
    return newBid

def condLocal(bundles, revenue, initialBids, 
              samples, maxItr = 100, tol = 1e-5, 
              verbose = False, ret = 'bids', eps = 1.0):
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
                    
    ret         := (string) Else return tuple:
                            (bids, converged (boolean), nItr (int), dist (float)) 
    
    OUTPUTS
    -------
    obids        := (1d array-like) A list of bids - one for each good.
    
    ONLY RETURNED IF ret == 'all'
    converged    := (boolean) A flag indicating convergence.
    
    itr          := The number of Iterations (impying n*iterations updates were performed)
                    performed. If converged = False -> itr = maxItr.
                    
    l            := Euclidean distance between the last update step 
                    and the previous state of the bid vector.
    """
    m = bundles.shape[1]
    newBids = numpy.atleast_1d(initialBids).copy()
    converged = False
    
    for itr in xrange(maxItr):
        oldBid = newBids.copy()
        
        for gIdx in xrange(m):
            newBids[gIdx] = condLocalUpdate(bundles, revenue, 
                                            newBids, gIdx, samples, 
                                            eps=eps, verbose = verbose)
            
        d = numpy.linalg.norm(oldBid-newBids)
        
        if d <= tol:
            converged = True
            break
        
    if ret == 'bids':
        return newBids
    elif ret == 'all':
        return newBids, converged, itr + 1, d
    else:
        raise ValueError("Unknown Return Type.")
    
def condLocalZeroUpdate(bundles, revenue, bids, 
                        targetBid, samples, 
                        verbose = False):
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
    
    normWon = numpy.float(numpy.count_nonzero(goodsWon[:,targetBid] == True))
    normLost = numpy.float(numpy.count_nonzero(goodsWon[:,targetBid] == False))
    
    posIdxList = numpy.flatnonzero(bundles[:,targetBid] == True)
    
    for posIdx in posIdxList:
        posBundle = bundles[posIdx,:]
        negBundle = posBundle.copy()
        negBundle[targetBid] = False
        negIdx = numpy.where((bundles == negBundle).all(axis=1))[0][0]
        
#        p1 = numpy.count_nonzero( numpy.all(goodsWon == posBundle, 1) ) + eps
#        p1 = numpy.float(p1) / (normWon + 2*eps)
        if normWon == 0:
            p1 = 0.
        else:
            p1 = numpy.float(numpy.count_nonzero( numpy.all(goodsWon == posBundle, 1) ) )
            if verbose:
                print '\t#({0}) = {1}'.format(posBundle, p1)
                print '\t#({0} = True) = {1}'.format(targetBid, normWon)
                 
            p1 /= normWon
            
        if verbose:
            print 'p({0} | {1} = True ) = {2}'.format(posBundle,targetBid,p1)
             
#        p1 = numpy.count_nonzero( numpy.all(goodsWon == posBundle, 1) )
#        p1 = numpy.float(p1) / (normWon + 1)
        if p1 > 1.0:
            raise ValueError ("p1 = {0} > 1.0".format(p1))
        
        if p1 < 0.0:
            raise ValueError("p1 = {0} < 0.0".format(p1))
        
#        p0 = numpy.count_nonzero( numpy.all(goodsWon == negBundle, 1) ) + eps
#        p0 = numpy.float(p0) / ( normLost +  2*eps )

        if normLost == 0:
            p0 = 0.
        else:
#            p0 = numpy.float(numpy.count_nonzero( numpy.all(goodsWon == negBundle, 1) )) / normLost
            p0 = numpy.float(numpy.count_nonzero( numpy.all(goodsWon == negBundle, 1) ))
            if verbose:
                print '\t#({0}) = {1}'.format(negBundle, p0)
                print '\t#({0} = True) = {1}'.format(targetBid, normLost)
            
            p0 /= normLost
        
        if verbose:
            print 'p({0} | {1} = False) = {2}'.format(posBundle,targetBid,p0)
        
        if p0 > 1.0:
            raise ValueError ("p0 = {0} > 1.0".format(p0))
        
        if p0 < 0.0:
            raise ValueError("p0 = {0} < 0.0".format(p0))
        
    
        newBid += ((revenue[posIdx]*p1) - (revenue[negIdx]*p0))
        
    if verbose:
        print newBid
        
    return newBid
    
def condLocalZero(bundles, revenue, initialBids, 
                  samples, maxItr = 100, tol = 1e-5, 
                  verbose = False, ret = 'bids'):
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
                    
    ret         := (string) Else return tuple:
                            (bids, converged (boolean), nItr (int), dist (float)) 
    
    OUTPUTS
    -------
    obids        := (1d array-like) A list of bids - one for each good.
    
    ONLY RETURNED IF ret == 'all'
    converged    := (boolean) A flag indicating convergence.
    
    itr          := The number of Iterations (impying n*iterations updates were performed)
                    performed. If converged = False -> itr = maxItr.
                    
    l            := Euclidean distance between the last update step 
                    and the previous state of the bid vector.
    """
    m = bundles.shape[1]
    newBids = numpy.atleast_1d(initialBids).copy()
    converged = False
    
    for itr in xrange(maxItr):
        oldBid = newBids.copy()
        
        for gIdx in xrange(m):
            newBids[gIdx] = condLocalZeroUpdate(bundles, revenue, newBids, gIdx, samples, verbose)
            
        d = numpy.linalg.norm(oldBid-newBids)
        
        if d <= tol:
            converged = True
            break
        
    if ret == 'bids':
        return newBids
    elif ret == 'all':
        return newBids, converged, itr + 1, d
    else:
        raise ValueError("Unknown Return Type.")
          
def condLocalMcUpdate(bundleRevenueDict, bids, j, samples, pad = True, verbose = False):
        
    evg = 0.0
    evl = 0.0
    nwon = 0
    nlost = 0
    
    samplesCopy = list(samples.copy())
    
    if pad == True:
            
        bidplus = numpy.atleast_1d(bids).copy()
        bidplus[j] += 1
        
        bidminus = bids.copy()
        if bidminus[j] > 1.0:
            bidminus[j] -=1
        else:
            bidminus[j] = 0
        
        samplesCopy.append(bidplus)
        
        samplesCopy.append(bidminus)
            
    for sample in samplesCopy:
        if sample[j] <= bids[j]:
            evg += bundleRevenueDict[tuple(sample<=bids)]
            nwon += 1
        else:
            evg += bundleRevenueDict[tuple(sample<=bids)]
            nlost +=1
            
    if nwon > 0:
        evg /= nwon
        
    if nlost > 0:
        evl /= nlost
    
    newBid = evg - evl
        
    return newBid
        
def condLocalMc(bundles, revenue, initBids, samples, 
                maxItr = 100, tol = 1e-5, pad = True, 
                verbose = True, ret = 'bids' ):
    m = initBids.shape[0]
    newBids = numpy.atleast_1d(initBids).copy()
    converged = True
    
    brd = {}
    for b,r in zip(bundles,revenue):
        brd[tuple(b)] = r
    
    if m != samples.shape[1]:
        raise ValueError("m != samples.shape[1]")
    
    for itr in xrange(maxItr):
        oldBids = newBids.copy()
        
        for gIdx in xrange(m):
            newBids[gIdx] = condLocalMcUpdate(brd, newBids, gIdx, samples, pad, verbose)
        
        d = numpy.linalg.norm(oldBids-newBids)
        
        if d <= tol:
            converged = True
            break
        
    if ret == 'bids':
        return newBids
    elif ret == 'all':
        return newBids, converged, itr + 1, d
    else:
        raise ValueError('Unknown Return Type {0}'.format(ret))
            
    
def condMVLocalUpdate(bundleRevenueDict, bids, j, samples, verbose = False):
    
    newBid = 0.0
    
    samplesjwon = samples[samples[:,j] < bids[j]]
    
    if samplesjwon.shape[0] == 0:
        return 0.0
        
    for samplejwon in samplesjwon:
        bundleWon = samplejwon < bids
        bundleLost = bundleWon.copy()
        bundleLost[j] = False
#        jwonrev = revenue[numpy.where((bundles == bundleWon).all(axis=1))[0][0]]
#        jlostrev = revenue[numpy.where((bundles == bundleLost).all(axis=1))[0][0]]
        jwonrev  = bundleRevenueDict[tuple(bundleWon)]
        jlostrev = bundleRevenueDict[tuple(bundleLost)]
        newBid += jwonrev - jlostrev
        
    newBid /= samplesjwon.shape[0]
    
    if verbose:
        print '\tNew bid = {0}'.format(newBid)
        
    return newBid

def condMVLocal(bundles, revenue, initBids, samples, 
                     maxItr = 100, tol = 1e-5, verbose = False, 
                     ret = 'bids'):
    m         = bundles.shape[1]
    newBids   = numpy.atleast_1d(initBids).copy()
    converged = False
    
    brd = {}
    for b,r in zip(bundles,revenue):
        brd[tuple(b)] = r
    
    for itr in xrange(maxItr):
        oldBids = newBids.copy()
        
        for gIdx in xrange(m):
            newBids[gIdx] = condMVLocalUpdate(brd, 
                               oldBids, gIdx, samples, verbose)
            
        d = numpy.linalg.norm(oldBids - newBids)
        
        if d <= tol:
            converged = True
            break
            
    if ret == 'bids':
        return newBids
    elif ret == 'all':
        return newBids, converged, itr + 1, d
    else:
        raise ValueError('Unknown Return Type {0}.'.format(ret))
            