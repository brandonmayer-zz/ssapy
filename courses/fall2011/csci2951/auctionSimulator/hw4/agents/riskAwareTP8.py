"""
this is /auctionSimulator/hw4/agents/riskAware.py

Author:    Brandon A. Mayer
Date:      12/6/2011
"""

from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.agents.targetPrice import *
    
class riskAwareTP8(riskAware):
    
    @staticmethod        
    def type():
        return "riskAwareTP8"
        
    @staticmethod
    def SS(args={}):
        expectedPrices = args['margDistPrediction'].expectedPrices({'method':'iTsample','nSamples':8})
        
        #optimalBundle
        optBundle, optExpectedSurplus = riskAware.acqMUPV( {'bundles'        : args['bundles'],
                                                            'valuation'      : args['valuation'],
                                                            'l'              : args['l'],
                                                            'A'              : args['A'],
                                                            'riskFunc'       : 'linear',
                                                            'margDist'       : args['margDistPrediction'],
                                                            'expectedPrices' : expectedPrices} )
        
        return targetPrice.bundleBid({'pointPricePrediction' : expectedPrices,
                                      'bundle'               : optBundle})
        
        
    def printSummary(self,args={}):
        """
        Print a summary of agent state to standard out.
        """
        print "Agent Name              = {0}".format(self.name)
        print "Agent ID                = {0}".format(self.id)
        print "Agent Type              = {0}".format(self.type())
        print "Agent lambda            = {0}".format(self.l)
        print "Agent Valuation Vector  = {0}".format(self.v)
        print "Agent Risk Aversion (A) = {0}".format(self.A)
        
        assert 'margDistPricePrediction' in args or self.pricePrediction != None,\
            "Must specify a price prediction"
            
            
        if 'margDistPricePrediction' in args:
            
            assert isinstance(args['margDistPricePrediction'],margDistSCPP) or\
                isinstance(args['margDistPricePrediction'], tuple),\
                    "args['margDistPricePrediction'] must be a margDistSCPP or numpy.ndarray"
                    
            if isinstance(args['margDistPricePrediction'], margDistSCPP):
                
                pricePredicton = args['margDistPricePrediciton']
                
            elif isinstance(args['margDistPricePrediction'], tuple):
                
                pricePrediction = margDistSCPP(args['margDistPricePrediction'])
                
            else:
                raise AssertionError('Should never get here')
                
        else:
            pricePrediction = self.pricePrediction
            
            
        bundles = self.allBundles(self.m)
        
        valuation = self.valuation(bundles = bundles,
                                   v       = self.v,
                                   l       = self.l )
        
        expectedPriceVector = pricePrediction.expectedPrices({'method':'iTsample','nSamples':8})
        
        mupv = self.mUPV({'bundles'        : bundles,
                          'valuation'      : valuation,
                          'l'              : self.l,
                          'margDist'       : pricePrediction,
                          'expectedPrices' : expectedPriceVector,
                          'A'              : self.A})
        print 'Expected Price Vector = {0}'.format(expectedPriceVector)
        
        upv = self.upv({'margDist'       : pricePrediction,
                        'expectedPrices' : expectedPriceVector})
        
        print 'Marginal Upper Partial Variance = {0}'.format(upv)
        
        expectedSurplus = self.surplus(bundles     = bundles,
                                       valuation   = valuation,
                                       priceVector = expectedPriceVector)
        
        expectedCost = self.cost(bundles = bundles, 
                                 price   = expectedPriceVector)
        
        print 'Bundle | Valuation | Expected Cost | Expected Surplus | Upper Parial Variance | Mean Upper-Partial Variance Utility'
        
        for i in xrange(bundles.shape[0]):
                print "{0}  {1:^8} {2:^8.3} {3:^8.3} {4:^8.3} {5:^8.3}".format( bundles[i].astype(numpy.int),
                                                          valuation[i],
                                                          expectedCost[i],
                                                          expectedSurplus[i],
                                                          numpy.dot(upv,bundles[i]),
                                                          mupv[i])
         
        [optBundleAcq, optSurplusAcq]   = self.acq(priceVector = expectedPriceVector)
        
        [optBundleMupv, optSurplusMupv] = self.acqMUPV( {'bundles'        : bundles,
                                                         'valuation'      : valuation,
                                                         'l'              : self.l,
                                                         'A'              : self.A,
                                                         'margDist'       : pricePrediction,
                                                         'expectedPrices' : expectedPriceVector})
        
        
        print ''
        print ''
        
        
        posIdx = expectedSurplus > 0.0
        if posIdx.any():
            print 'Bundles With Positive Expected surplus'
            print 'Bundle      |    Surplus   |     UPV     |      A*exp(UPV)     |  M-UPV Utility'
            
            for i in xrange(numpy.nonzero(posIdx)[0].shape[0]):
                print'{0}   {1:^5}   {2:^5}   {3:^5}    {4:^5}'.format(bundles[posIdx][i].astype(int), 
                                                                       expectedSurplus[posIdx][i], 
                                                                       numpy.dot(upv,bundles[posIdx][i]),
                                                                       self.A*numpy.exp(numpy.dot(upv,bundles[posIdx][i])),
                                                                       mupv[posIdx][i])
                                                    
        else:
            print 'No bundles with positive expected surplus.'
                                                    
        print ''
        
        print 'Optimal Bundle ACQ:           {0}'.format(optBundleAcq.astype(numpy.int))
        print 'Optimal Expected Surplus ACQ: {0}'.format(optSurplusAcq)
        
        print 'Optimal Bundle MUPV:          {0}'.format(optBundleMupv.astype(numpy.int))
        print 'Optimal Surplus MUPV:         {0}'.format(optSurplusMupv)
        
        print 'Bidding Strategy:             {0}'.format(self.bidStrategy)
        print 'Bid = {0}'.format(targetPrice.bundleBid({'pointPricePrediction' : expectedPriceVector,
                                                        'bundle'               : optBundleMupv}))
        
        print ''
        
        
        
        
        
        
                                                            
                                                                    
        
    
    