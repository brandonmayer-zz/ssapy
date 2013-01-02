from auctionSimulator.hw4.auctions.simultaneousAuction import *
from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.pricePrediction.margDistSCPP import *
from auctionSimulator.hw4.agents.simYW import *


import itertools
import numpy
import multiprocessing

import os
  
def main():
    filename = "F:\\courses\\fall2011\\csci2951\\hw4\\distributionPricePrediction\\distPricePrediction_straightMU8_10000_2011_12_8_1323383753.pkl"
    
    margDist = margDistSCPP()
    
    margDist.loadPickle(filename)
    
#    margDist.graphPdf()
    expectedPrices = margDist.expectedPrices()
    
    print'Arithmetic Expected Prices:'
    print expectedPrices
    
    upv = margDist.margUpv(expectedPrices)
    print 'upv of arithmetic expected prices'
    print upv
    
    expectedPrices8 = margDist.expectedPrices({'method':'iTsample','nSamples':8})
    print ''
    print'Sampled Expected Prices (8 samples):'
    print expectedPrices8
    
    upv8 = margDist.margUpv(expectedPrices8)
    print 'upv of sampled expected prices'
    print upv8
    
    #generate a random valuation
    l = 3
    v = simYW.randomValueVector()
    
    
    bundles = simYW.allBundles()
    
    valuation = simYW.valuation(bundles=bundles, 
                                v = v,
                                l=l)
    
    print'Bundles:'
    print bundles.astype('int')
    
    
    utility = riskAware.mUPV({'expectedPrices' : expectedPrices8,
                              'bundles'        : bundles,
                              'valuation'      : valuation,
                              'l'              : l,
                              'A'              : 3})
    print 'utility:'
    print utility
    
    
    
    
    
    
    
        
        
if __name__ == '__main__':
    main()
     
        
        
    