import numpy

def jointLocalUpdate( bundles, revenue, bids, targetBid, samples, verbose = False ):
    """
    Update a single bid index, targetBid, of bids given a set of samples 
    and revenue-bundle pair.
    
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
    
    posIdxList = numpy.flatnonzero(bundles[:,targetBid] == True)
    
    nSamples = samples.shape[0]
    
    for posIdx in posIdxList:
        posBundle = bundles[posIdx,:]
        negBundle = posBundle.copy()
        negBundle[targetBid] = False
        
        negIdx = numpy.where( (bundles == negBundle).all(axis=1))[0][0]
        
        posRev = revenue[posIdx]
        negRev = revenue[negIdx]
        
        p = numpy.float( numpy.count_nonzero( 
                numpy.all(numpy.delete(goodsWon,targetBid,1) 
                    == numpy.delete(posBundle,targetBid),1) ) )
        
        p/=nSamples
        
        if p > 1.0:
            raise ValueError("p > 1.0")
        elif p < 0.0:
            raise ValueError("p < 0.0")
        
        newBid += (posRev - negRev)*p

    return newBid

def jointLocal(bundles, revenue, initialBids, samples, maxItr, tol, filename = None, verbose = True):
    """
    Starting form an initial bid, run the jointLocal algorithm and return 
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
    
    m         = bundles.shape[1]
    obids     = numpy.atleast_1d(initialBids).copy()
    converged = False
    
    for itr in xrange(maxItr):
        oldBid = obids.copy()
        
        for gIdx in xrange(m):
            obids[gIdx] = jointLocalUpdate(bundles, revenue, obids, gIdx, samples, verbose)
            
        d = oldBid - obids
        l = numpy.dot(d,d)
        
        if l <= tol:
            converged = True
            break
        
    return obids, converged, itr, l