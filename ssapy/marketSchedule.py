#Functions to replicate market-based scheduling game described in
# "Exploring bidding strategies for market-based scheduling." Reeves et al.
# "Self-confirming price-prediction strategies for simultaneous one-shot auctions" Yoon et al.

import numpy
from ssapy import allBundles

def randomValueVector(vmin = 1, vmax = 50, m = 5, l = None):
    if l is None:
        l = numpy.random.random_integers(low = 1, high = m)
        
    v = numpy.zeros(m)
    
    sortedRandInts = numpy.random.random_integers(low = vmin, high=vmax, size = (m-l+1))
    sortedRandInts.sort()
    sortedRandInts = sortedRandInts[::-1]
    
    v[(l-1):] = sortedRandInts

    return v, l 

def revenueDict(v, l):
    
    m = numpy.asarray(v).shape[0]
    
    rev = {}
    
    for bundle in allBundles(m):
        cs = numpy.cumsum(bundle)
        if cs[-1] < l:
            rev[tuple(bundle)] = 0
        else:
            t = numpy.nonzero(bundle >= l)[0][0]
            rev[tuple(bundle)] = v[t]
            
    return rev
        
    
    
    
        

