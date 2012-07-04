from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.padnums import pprint_table as ppt
import sys

def main():
    
    def drange(start,stop,step):
        r = start
        while r < stop:
            yield r
            r += step
    
    
    
    margPkl = "C:\\bmProjects\\courses\\fall2011\\csci2951\\auctionSimulator\\" +\
    "hw4\\pricePrediction\\margDistPredictions\\distPricePrediction_straightMU8_10000_2011_12_8_1323383753.pkl"
    margDist = margDistSCPP()
    margDist.loadPickle(margPkl)
    
    for i in xrange(10):
        print ''
        print ''
        m = 5
        l = numpy.random.random_integers(1,5)
        v = simYW.randomValueVector(0, 50, m = m)
        bundles = riskAware.allBundles(m)
        
        
        
        expectedPrices = margDist.expectedPrices(method   = 'iTsample',
                                                 nSamples = 8)
        
        valuation = simYW.valuation(bundles = bundles,v = v,l = l)
        
        
        
        
        acqBundle, acqSurplus = simYW.acqYW(bundles     = bundles,
                                            valuation   = simYW.valuation(bundles = bundles,v = v,l = l),
                                            priceVector = expectedPrices,
                                            l           = l)
        
        expectedSurplus = riskAware.surplus(bundles     = bundles, 
                                            valuation   = valuation, 
                                            priceVector = expectedPrices)
        
        upperPartialStd = margDist.margUps(expectedPrices = expectedPrices)
        
        table1 = [
                 ["m = ", m],
                 ["l = ", l],
                 ["v = ", str(v)],
                 ["Expected Prices = ", str(expectedPrices)],
                 ["acq Bundle = ",  str(acqBundle.astype(numpy.int))],
                 ["Marginal Upper Partial Std = ", str(upperPartialStd)]
                  ]
        
        ppt(sys.stdout,table1)
        
        table2 = []
        for A in drange(0,10,.2):
            optBundle, optMups = riskAware.acqMups( A               = A,
                                                    bundles         = bundles,
                                                    l               = l,
                                                    expectedSurplus = expectedSurplus,
                                                    upperPartialStd = upperPartialStd)
            
            table2.append(["A = {0}".format(A), "optBundle = {0}".format(optBundle.astype(int))])
            
        print''
        ppt(sys.stdout,table2)
        
                                                       
                                                      
                          
                          
    
    

if __name__ == "__main__":
    main()