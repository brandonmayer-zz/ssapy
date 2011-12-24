"""
This is /auctionSimulator/hw4/agents/pointPredictionAgent.py

Author:        Brandon A. Mayer
Date:          11/27/2011

A base class for agents who utilize a distribution price prediction.
"""
from pricePredictionAgent import pricePredictionAgent
from aucSim.pricePrediction.margDistSCPP import margDistSCPP
from aucSim.padnums import pprint_table as ppt

import sys

class margDistPredictionAgent(pricePredictionAgent):
    def __init__(self,**kwargs):
        if 'margDistPricePrediction' in  kwargs:
            kwargs['pricePrediction'] = kwargs['margDistPricePrediction']
        elif 'margDistPrediction' in kwargs:
            kwargs['pricePrediction'] = kwargs['margDistPrediction']
        elif 'margDist' in kwargs:
            kwargs['pricePrediction'] = kwargs['margDist']
            
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
      try:
          pricePrediction = kwargs['margDistPrediction']
      except KeyError:
          raise KeyError('Must specify margDistPrediction')
      
    
      numpy.testing.assert_(isinstance(kwargs['margDistPrediction'],margDistSCPP) or\
                                isinstance(kwargs['margDistPrediction'],tuple), 
                msg="kwargs['margDistPrediction'] must be an instance of type margDistSCPP or a python tuple.")
            
      
      if isinstance(pricePrediction, margDistSCPP):
          
          return pricePrediction
                          
      elif isinstance(kwargs['margDistPrediction'], tuple):
            
          return margDistSCPP(pricePrediction)
            
      else:
          raise AssertionError('This should never happen...')
            
    def bid(self, **kwargs):
        """
        Interface to bid.
        Accepts an argument of margDistPrediction which
        will take precidence over any stored prediction
        """
        m                  = kwargs.get('m', self.m)
        v                  = kwargs.get('v', self.v)
        l                  = kwargs.get('l', self.l)
        margDistPrediction = kwargs.get('margDistPrediciton', self.pricePrediction)
        bundles            = kwargs.get('bundles', self.allBundles(m))
        
        numpy.testing.assert_(isinstance(margDistPrediction,margDistSCPP),
            msg="margDistPrediction must be a valid instance of margDistSCPP.")
        
        return self.SS( margDistPrediction = margDistPrediction,
                        bundles            = bundles,
                        l                  = l,
                        valuation          = simYW.valuation(bundles,self.v,self.l) )
    
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