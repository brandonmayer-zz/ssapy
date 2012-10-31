from ssapy.pricePrediction.margDistSCPP import margDistSCPP
from ssapy.pricePrediction.jointGMM import jointGMM

from scipy.stats import norm
from scipy.interpolate import interp1d

import numpy
import matplotlib.pyplot as plt

from straightMU import straightMU8, straightMU64, straightMU256

initStrategies = {'straightMU8': straightMU8,
                  'straightMU64': straightMU64,
                  'straightMU256':straightMU256}


def margLocalBid(**kwargs):
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
    
    initSS = kwargs.get('initStrategy','straightMU8')
    
    initialStrategy = initStrategies[initSS]
    
    bids = initialStrategy( pricePrediction = pricePrediction,
                            bundles         = bundles,
                            valuation       = valuation )
    
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
                                print 'p = {0}'.format(p)
                        else:
                            p *= (1- pricePrediction.margCdf(x = bids[og], margIdx = og))
                            if verbose:
                                print 'p = {0}'.format(p)
                            
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
        plt.plot(bidList[:-1],'bo-',markerfacecolor=None)
        plt.plot(bidList[-1],'ro')
        plt.show()
        
        
    if verboseOut:
        return bids, bidList, converged
    else:
        return bids
                            
                        
                
                
                
        
    
                       
    