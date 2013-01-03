"""
Conditional Local Bidder strategy

Author: Brandon A. Mayer
Date: 1/2/2013 (adapted from ssapy.agents.condLocalBid)
"""

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
    
    
    