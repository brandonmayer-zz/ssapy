#from ssapy.pricePrediction.margDistSCPP import margDistSCPP
from ssapy.pricePrediction.jointGMM import jointGMM

from scipy.stats import norm
from scipy.interpolate import interp1d

import numpy
import matplotlib.pyplot as plt

from straightMU import straightMU8, straightMU64, straightMU256

initStrategies = {'straightMU8': straightMU8,
                  'straightMU64': straightMU64,
                  'straightMU256':straightMU256}

def margLocalMcUpdate(bundleRevenueDict, bids, j, 
                      samples, verbose = False):
    newBid = 0.0
    
    for sample in samples:
        bundleWon = sample < bids
        bundleWon[j] = True
        
        bundleLost = bundleWon.copy()
        bundleLost[j] = False
        
        newBid += bundleRevenueDict[tuple(bundleWon)] - bundleRevenueDict[tuple(bundleLost)] 
        
    newBid /= samples.shape[0]
    
    if verbose:
        print '\tNew bid = {0}'.format(newBid)
        
    return newBid

def margLocalMc(bundleRevenueDict, initialBids, samples, maxItr = 100, 
                tol= 1e-5, verbose = False, ret = 'bids'):
    
    m         = samples.shape[1]
    newBids   = numpy.atleast_1d(initialBids).copy()
    converged = False
        
    for itr in xrange(maxItr):
        oldBids = newBids.copy()
        
        for gIdx in xrange(m):
            newBids[gIdx] = margLocalMcUpdate(bundleRevenueDict, 
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

def margLocalUpdate(bundles, revenue, bids, targetBidIdx, samples, verbose = False):
    """
    Update a single bid index, targetBidIdx, of bids given a set of samples and a 
    revenue function described by bundle - revenue pairs using the marginal local algorithm.
    
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
    
    pwin = numpy.sum(samples <= bids, 0, dtype = float)/samples.shape[0]
    
    posIdxList = numpy.flatnonzero(bundles[:,targetBidIdx == True])
    
    for posIdx in posIdxList:
        posBundle = bundles[posIdx,:]
        negBundle = posBundle.copy()
        negBundle[targetBidIdx] = False
        
        negIdx = numpy.where( (bundles == negBundle).all(axis=1) )[0][0]
        
        posRev = revenue[posIdx]
        negRev = revenue[negIdx]
        
        p = 1.0
        for goodIdx, good in enumerate(posBundle):
            if goodIdx == targetBidIdx:
                pass
            else:
                if good:
                    p*=pwin[goodIdx]
                else:
                    p*=(1-pwin[goodIdx])
                    
        if p > 1.0:
            raise ValueError("p > 1.0")
        elif p < 0.0:
            raise ValueError(" p < 0.0")
        
        newBid += (posRev - negRev)*p
        
    return newBid
        
def margLocal(bundles, revenue, initialBids, samples, maxItr = 100, tol= 1e-5, verbose = True, ret = 'bids'):
    """
    Starting form an initial bid, run the margLocal algorithm and return 
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
    
    ret         := (string) If ret == 'bids' just return the new bid vector
                            Else if ret == 'all' return tuple:
                            (bids, converged (boolean), nItr (int), dist (float)) 
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
    newBids = numpy.atleast_1d(initialBids).copy()
    converged = False
    
    for itr in xrange(maxItr):
        oldBid = newBids.copy()
        for gIdx in xrange(m):
            newBids[gIdx] = margLocalUpdate(bundles,revenue, newBids, gIdx, samples, verbose)
            
        d = numpy.linalg.norm(oldBid-newBids)
        
        if d <= tol:
            converged = True
            break
        
    if ret == 'bids':
        return newBids
    else:
        return newBids, converged, itr + 1, d
    
    
def margLocalA(**kwargs):
    """
    Marg Local Analytic - computes probabilities analytically.
    """
    pricePrediction = kwargs.get('pricePrediction')
    if pricePrediction == None:
        raise KeyError("Must specify pricePrediction")
    
    bundles = kwargs.get('bundles')
    if bundles == None:
        raise KeyError("Must specify bundles")
            
    valuation = kwargs.get('valuation')
    if valuation == None:
        raise KeyError("Must specify valuation")
    
    
    verboseOut = kwargs.get('verboseOut', False)
    
    verbose  = kwargs.get('verbose', True)
    
    vis = kwargs.get('vis', False)
    
    n_itr = kwargs.get('n_itr',100)
    
    tol = kwargs.get('tol',1e-3)
    
    initialBid = kwargs.get('initialBid')
    if initialBid == None:
        initSS = kwargs.get('initStrategy','straightMU8')
        initialStrategy = initStrategies[initSS]
#        bids = initialStrategy( pricePrediction = pricePrediction,
#                                bundles         = bundles,
#                                valuation       = valuation )
        bids = initialStrategy( bundles, valuation, pricePrediction, verbose)
    else:
        bids = initialBid
    
    if verbose:
        print 'initial bid = {0}'.format(bids)
    
    if isinstance(pricePrediction,margDistSCPP):
        cdf = []
        for hist,binEdges in pricePrediction.data:
            p = hist / numpy.float(numpy.dot(hist, numpy.diff(binEdges)))
            c = numpy.hstack((0,numpy.cumsum(p*numpy.diff(binEdges),dtype=numpy.float)))
            f = interp1d(binEdges,c,'linear')
            cdf.append(f)
            
    if vis or verboseOut:
        bidList = [bids]
    
    converged = False
    for itr in xrange(n_itr):
        if verbose:
            print 'itr = {0}, bid = {0}'.format(itr, bids)
            
        prevBid = bids.copy()
        
        for bidIdx in xrange(bids.shape[0]):
            if verbose:
                print '\tbidIdx = {0}'.format(bidIdx)
            newBid = 0.0
            
            otherGoods = numpy.delete(numpy.arange(bids.shape[0]),bidIdx)
            
            for bundleIdx, bundle in enumerate(bundles):
                val = valuation[bundleIdx]
                
                if verbose:
                    print '\t\tbundle = {0}'.format(bundle)
                    print '\t\tval = {0}'.format(val)
                
                
                p = 1.0
                
                if isinstance(pricePrediction, jointGMM):
                    for og in otherGoods:
                        if bundle[og] == True:
                            
                            p *= pricePrediction.margCdf(x = bids[og], margIdx = og)
                            if verbose:
                                print '\t\t\t p*=cdf({0})'.format(bids[og])
                                print '\t\t\tp = {0}'.format(p)
                        else:
                            p *= (1- pricePrediction.margCdf(x = bids[og], margIdx = og))
                            if verbose:
                                print '\t\t\tp*=(1-cdf({0}))'.format(bids[og])
                                print '\t\t\tp = {0}'.format(p)
                            
                elif isinstance(pricePrediction, margDistSCPP):
                    for og in otherGoods:
                        if verbose:
                            print '\t\t\tother good = {0}'.format(og)
                            
                        if bids[og] > pricePrediction.data[og][1][-1]:
                            if verbose:
                                print '\t\t\tbids[og] > pricePredicton.data[og][1][-1]'
                            pass
                            
                        elif bids[og] < pricePrediction.data[og][1][0]:
                            if verbose:
                                print '\t\t\tbids[og] < pricePrediction.data[og][1][0]'
                            p *= 1e-8
                        elif bundle[og] == True:
                            if verbose:
                                print '\t\t\tbundle[og] == {0}'.format(bundle[og])
                                print '\t\t\tcdf = {0}'.format(cdf[og](bids[og]))
                            p*=cdf[og](bids[og])
                        else:    
                            if verbose:
                                print '\t\t\tbundle[og] == {0}'.format(bundle[og])
                                print '\t\t\t(1-cdf) = {0}'.format((1-cdf[og](bids[og])))
                            p*=(1-cdf[og](bids[og]))
                            
                        if verbose:
                            print '\t\t\tp = {0}'.format(p)
                            
                if bundle[bidIdx] == True:
                    newBid += (val*p)
                else:
                    newBid -= (val*p)
                    
                if verbose:
                    print '\t\tnewBid = {0}'.format(newBid)
                    
            bids[bidIdx] = newBid
            
            if verboseOut or vis:
                bidList.append(bids)
            
        sse = numpy.dot(prevBid - bids, prevBid - bids)
        
        if verbose:
            print ''
            print 'Iteration = {0}'.format(itr)
            print 'prevBid   = {0}'.format(prevBid)
            print 'newBid    = {0}'.format(bids)
            print 'sse       = {0}'.format(sse)
            
        if sse <= tol:
            converged = True
            if verbose:
                print 'sse = {0} < tol = {1}'.format(sse,tol)
                print 'converged = True'
                
            break
                
            
    if vis:
        bidList = numpy.atleast_2d(bidList)
        plt.plot(bidList[:-1,0],bidList[:-1,1],'bo-',markerfacecolor=None)
        plt.plot(bidList[-1,0], bidList[-1,1],'ro')
        plt.show()
        
        
    if verboseOut:
        return bids, bidList, converged
    else:
        return bids
                            
                        
                
                
                
        
    
                       
    