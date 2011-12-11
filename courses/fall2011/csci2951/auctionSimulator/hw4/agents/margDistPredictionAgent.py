"""
This is /auctionSimulator/hw4/agents/pointPredictionAgent.py

Author:        Brandon A. Mayer
Date:          11/27/2011

A base class for agents who utilize a distribution price prediction.
"""
from pricePredictionAgent import *
from auctionSimulator.hw4.pricePrediction.margDistSCPP import *
from auctionSimulator.hw4.padnums import pprint_table as ppt

import sys

class margDistPredictionAgent(pricePredictionAgent):
    def __init__(self,**kwargs):
        if 'margDistPricePrediction' in  kwargs:
            kwargs['pricePrediction'] = kwargs['margDistPricePrediction']
            
        super(margDistPredictionAgent,self).__init__(**kwargs)
            
    @staticmethod
    def predictionType():
        return "margDistSCPP"
    
    @staticmethod
    def type():
        return "margDistPredictionAgent"
    
    @staticmethod
    def SS(**kwargs):
      """
      Standard SS checks for the margDistPrediciton agent.
      """  
      assert 'margDistPrediction' in kwargs,\
            "Must specify margDistPrediction in kwargs parameter."
            
      assert isinstance(kwargs['margDistPrediction'],margDistSCPP) or\
                isinstance(kwargs['margDistPrediction'],tuple),\
            "kwargs['margDistPrediction'] must be an instance of type margDistSCPP or a python tuple."
            
      pricePrediction = None
      if isinstance(kwargs['margDistPrediction'], margDistSCPP):
                        
          pricePrediction = kwargs['margDistPrediction']
            
      elif isinstance(kwargs['margDistPrediction'], tuple):
            
          pricePrediction = margDistSCPP(kwargs['margDistPrediction'])
            
      else:
          # this should never happen
          raise AssertionError
      
      return pricePrediction
      
    def bid(self, **kwargs):
        """
        Interface to bid.
        Accepts an argument of margDistPrediction which
        will take precidence over any stored prediction
        """
        bundles = self.allBundles(self.m)
        if 'margDistPrediction' in kwargs:
                            
                return self.SS(margDistPrediction = kwargs['margDistPrediction'],
                               bundles            = bundles,
                               l                  = self.l,
                               valuation          = simYW.valuation(bundles, self.v, self.l))
                
                           
        else:
            assert isinstance(self.pricePrediction, margDistSCPP),\
                "Must specify a price prediction to bid."
                
            return self.SS(margDistPrediction = self.pricePrediction,
                           bundles            = bundles,
                           l                  = self.l,
                           valuation          = simYW.valuation(bundles,self.v,self.l))
    
    def printSummary(self,**kwargs):
        """
        Print a summary of the agent's state to standard output.
        
        Can provide an expected price vector else one will be generated.
        The method of computing the expected prices is controled by the
        method parameter
        
        method   := 'average' uses arithmetic average (default)
        
        method   := 'iTsample' uses inverse transform sampling
        
        nSamples := if 'iTsample' is specified this parameter controls the number
                    of samples used, the default is 8
        """
        super(margDistPredictionAgent,self).printSummary()
        
        assert 'margDistPrediction' in kwargs or self.pricePrediction != None,\
            "Must specify a price prediction"
            
        pricePrediction = None
        
        if 'margDistPrediction' in kwargs:
            
            assert isinstance(kwargs['margDistPrediction'],margDistSCPP) or\
                isinstance(kwargs['margDistPrediction'], tuple),\
                    "kwargs['margDistPrediction'] must be a margDistSCPP or numpy.ndarray"
                    
            if isinstance(kwargs['margDistPrediction'], margDistSCPP):
                
                pricePrediction = kwargs['margDistPrediction']
                
            elif isinstance(kwargs['margDistPrediction'], tuple):
                
                pricePrediction = margDistSCPP(kwargs['margDistPrediction'])
                
            else:
                raise AssertionError('Should never get here')
                
        else:
            pricePrediction = self.pricePrediction
            
        bundles = self.allBundles(self.m)
        
        valuation = self.valuation(bundles = bundles,
                                   v       = self.v,
                                   l       = self.l )
        
        expectedPriceVector = None
        
        if 'expectedPriceVector' in kwargs:
            expectedPriceVector = kwargs['expectedPriceVector']
        else:
            method = 'average'
            if 'method' in kwargs:
                method = kwargs['method']
    
            if method == 'average':
                expectedPriceVector = pricePrediction.expectedPrices()
                
            elif method == 'iTsample':
                
                nSamples = 8
                
                if 'nSamples' in kwargs:
                    nSamples = kwargs['nSamples']
                    
                expectedPriceVector = pricePrediction.expectedPrices( method   = 'iTsample',
                                                                      nSamples = nSamples)
            else:
                print '----ERROR----'
                print 'Unknown method to compute expected price vector'
                raise AssertionError
            
                
        
        print 'Expected Price Vector = {0}'.format(expectedPriceVector)
        
        expectedSurplus = self.surplus(bundles     = bundles,
                                       valuation   = valuation,
                                       priceVector = expectedPriceVector)
        
        expectedCost = self.cost(bundles = bundles, 
                                 price   = expectedPriceVector)
        
        print 'Bundle | Valuation | Expected Cost | Expected Surplus'
        
        table = [['Bundle', 'Valuation', 'Expected Cost', 'Expected Surplus']]
        
        for i in xrange(bundles.shape[0]):
            table.append([str(bundles[i].astype(numpy.int)), valuation[i], expectedCost[i], expectedSurplus[i]])
            
        ppt(sys.stdout, table)
                
        [expectedOptBundle, expectedOptSurplus] = self.acq(priceVector=expectedPriceVector)
        
        print "Expected Optimal Bundle acq(expectedPriceVector):     {0}".format(expectedOptBundle.astype(numpy.int))
        print "Expected Surplus of Expected Optimal Bundle:          {0}".format(expectedOptSurplus)
        print "Bid:    {0}".format(self.bid(margDistPrediction = pricePrediction))
        print ''