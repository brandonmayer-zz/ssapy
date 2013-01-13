"""
this is /ssapy/marketSchedule/__init__.py

Author: Brandon A. Mayer
Date: 1/1/2013

Module for Market Scheduling Game functions and agents as described in:

"Exploring bidding strategies for market-based scheduling", Reeves et. al. 2005 

and

"Self-Confirming Price-Prediction Strategies for Simultaneous One-Shot Auctions",
Yoon et. al. 2007
"""

import numpy
import itertools

from ssapy.agents import agentBase
from ssapy.util import listBundles, cost


def randomValueVector(vmin = 1, vmax = 50, m = 5, l = None):
    if l is None:
        l = numpy.random.random_integers(low = 1, high = m)
        
    v = numpy.zeros(m)
    
    sortedRandInts = numpy.random.random_integers(low = vmin, high=vmax, size = (m-l+1))
    sortedRandInts.sort()
    sortedRandInts = sortedRandInts[::-1]
    
    v[(l-1):] = sortedRandInts

    return v, l 

def listRevenue(bundles, v, l):
    """Compute the revenue (valuation) for a given 
    list of bundles (collection of goods)
    
    Parameters
    ----------
    bundles: array_like, shape (n_bundles, n_goods)
        List of collection of goods. Each row is collection, each column a good index.
        A 1 in the i^{th} row and j^{th} column implies the good j is contained in the 
        i^{th} listed bundle.
    
    v: array_like, shape (n_goods)
        The value vector described in the Market Scheduling game of YW.
        
    l: int,
        The minimal number of goods the agent needs to win to obtain value.
        Another parameter of the market schedule game.
        
    Returns
    -------
    valution: array_like, shape (n_bundles)
        valution[i] is the revenue the agent would receive had
        he/she been able to procure the collection of goods bundle[i]. 
    """
    if bundles == None:
        bundles = listBundles(numpy.atleast_1d(v).shape[0])
    else:
        bundles = numpy.atleast_2d(bundles)
    
    cs = [numpy.atleast_1d(i) for i in itertools.imap(numpy.cumsum,bundles)]
        
    valuation = []
    for bundle in cs:
        if bundle[-1] < l:
            valuation.append(0)
        else:
            t = numpy.nonzero(bundle >= l)[0][0]
            valuation.append(v[t])
            
    return numpy.atleast_1d(valuation)

def dictRevenue(v, l):
    
    m = numpy.asarray(v).shape[0]
    
    rev = {}
    
    for bundle in listBundles(m):
        cs = numpy.cumsum(bundle)
        if cs[-1] < l:
            rev[tuple(bundle)] = 0
        else:
            t = numpy.nonzero(bundle >= l)[0][0]
            rev[tuple(bundle)] = v[t]
            
    return rev
