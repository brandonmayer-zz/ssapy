"""
This is a script to get a quick look at the space of the
expected risk aware utility function given two bidders
"""

import numpy
from auctionSimulator.hw4.pricePrediction.margDistSCPP import * 

def valuation(m = 2, vmin = 1, vmax = 50):
    """
    return valuation vector and lambda
    """
    l = numpy.random.random_integers(1,m)
    
    v = numpy.random.random_integers(low = vmin, high = vmax, size = m)
    
    v.sort()
    
    v = v[::-1]
    
    return v,l

def allBundles(nGoods = 5):
        """
        Return a numpy 2d array of all possible bundles that the agent can
        bid on given the number of auctions.
        
        The Rows represent the bundle index.
        
        The Columns Represent the good index.        
        
        Return bundles as booleans for storage and computational efficiency
        """
        assert isinstance(nGoods,int) and nGoods >=0,\
            "nGoods = {0} is not a positive integer".format(nGoods)
        return numpy.atleast_2d([bin for bin in itertools.product([False,True],repeat=nGoods)]).astype(bool)
    
def expectedUtility(bids = None, margDist=None,v = None, l = None):
    """
    Given a matrix of bids (each row is a bid, over goods represented by columns)
    compute the corresponding expected risk aware utility
    given a valuation over each bundle
    """
    expectedPrices = margDist.expectedPrices({'method':'iTsample','nSample':8})
    
    margUpv = margdist.margUpv()
    
    
def main():
    
    #load a distribution
    straightMUpkl = "C:\\bmProjects\\courses\\fall2011\\csci2951\\" +\
                    "auctionSimulator\\hw4\\pricePrediction\\margDistPredictions\\" +\
                    "distPricePrediction_straightMU_10000_2011_12_4_1323040769.pkl"
           
    margDist5 = margDistSCPP()
    margDist5.loadPickle(straightMUpkl)        
#    margDist5.graphPdf()

    margDist2 = margDistSCPP(margDistData=margDist5.data[0:2])
    margDist2.graphPdf() 
    
    expectedPrices = margDist2.expectedPrices({'method':'iTsample','nSamples':8})
    
    upv = margDist2.margUpv(expectedPrices = expectedPrices)
    
    
if __name__ == "__main__":
    main()