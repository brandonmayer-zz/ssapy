import numpy

def marginalUtility_(bundleRevenueDict, bids, targetBid, sample):
    bundleWon = sample <= bids
    
    posBundle = bundleWon.copy()
    negBundle = bundleWon.copy()
    posBundle[targetBid] = True
    negBundle[targetBid] = False
    
    return bundleRevenueDict[tuple(posBundle)] - bundleRevenueDict[tuple(negBundle)]
    
def jointLocalUpdateMc(bundles, revenue, bids, targetBid, samples, verbose = False):
    """
    Compute jointLocalUpdate via monte carlo estimate of marginal revenue for good {j}
    """
    bundleRevenueDict = {}
    for bundle, r in zip(bundles,revenue):
        bundleRevenueDict[tuple(bundle)] = r
    muj = numpy.float64(0.0)
    for sample in samples:
        muj += marginalUtility_(bundles, revenue, bids, targetBid, sample)
    
    return muj/samples.shape[0]

def jointLocalMc(bundles, revenue, initialBids, samples, maxItr = 100, tol = 1e-5, verbose = True, ret = 'bids'):
    m         = bundles.shape[1]
    newBids   = numpy.atleast_1d(initialBids)
    converged = False
    for itr in xrange(maxItr):
        oldBids = newBids.copy()
        
        for gIdx in xrange(m):
            newBids[gIdx] = jointLocalUpdateMc(bundles, revenue, newBids, gIdx, samples)
            
        d = numpy.linalg.norm(oldBids - newBids)
        if d <= tol:
            converged = True
            break
        
        if ret == 'bids':
            return newBids
        elif ret == 'all':
            return newBids, converged, itr + 1, d
        else:
            raise ValueError("Unknown Return String {0}".format(ret))
        
    
    
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
        
    if verbose:
        print newBid

    return newBid

def jointLocal(bundles, revenue, initialBids, samples, maxItr = 100, tol = 1e-5, verbose = True, ret = 'bids'):
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
                    
    ret         := (string) Else return tuple:
                        (bids, converged (boolean), nItr (int), dist (float)) 
    
    OUTPUTS
    -------
    obids        := (1d array-like) A list of bids - one for each good.
    
    converged    := (boolean) A flag indicating convergence.
    
    itr          := The number of Iterations (impying n*iterations updates were performed)
                    performed. If converged = False -> itr = maxItr.
                    
    l            := Euclidean distance between the last update step 
                    and the previous state of the bid vector.
                    
    ONLY RETURNED IF ret == 'all'
    converged    := (boolean) A flag indicating convergence.
    
    itr          := The number of Iterations (impying n*iterations updates were performed)
                    performed. If converged = False -> itr = maxItr.
                    
    l            := Euclidean distance between the last update step 
                    and the previous state of the bid vector.
    """
    
    m         = bundles.shape[1]
    newBids   = numpy.atleast_1d(initialBids).copy()
    converged = False
    
    for itr in xrange(maxItr):
        oldBids = newBids.copy()
        
        for gIdx in xrange(m):
            newBids[gIdx] = jointLocalUpdate(bundles, revenue, newBids, gIdx, samples, verbose)
                
        d = numpy.linalg.norm(oldBids - newBids)
        if d <= tol:
            converged = True
            break
        
    if ret == 'bids':
        return newBids
    elif ret == 'all':
        return newBids, converged, itr + 1, d
    else:
        raise ValueError("Unknown Return String {0}".format(ret))