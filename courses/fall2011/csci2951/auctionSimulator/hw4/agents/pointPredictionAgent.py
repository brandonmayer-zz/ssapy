"""
This is /auctionSimulator/hw4/agents/pointPredictionAgent.py

Author:        Brandon A. Mayer
Date:          11/27/2011

A base class for agents who utilize a point price prediction.
"""

from pricePredictionAgent import *
from auctionSimulator.hw4.pricePrediction.pointSCPP import *

class pointPredictionAgent(pricePredictionAgent):
    def __init__(self,
                 m = 5,
                 v = None,
                 l = None,
                 vmin = 0,
                 vmax = 50,
                 pointPricePrediction = None,
                 name = "Anonymous"):
        
        super(pointPredictionAgent,self).__init__(m=m,
                                                  v=v,
                                                  l=l,
                                                  vmin=vmin,
                                                  vmax=vmax,
                                                  name=name,
                                                  pricePrediction=pointPricePrediction)
        
    @staticmethod
    def predictionType():
        return "pointSCPP"
    
    @staticmethod
    def type():
        return "pointPredictionAgent"
    
    def printSummary(self,args={}):
        """
        Print a summary of agent state to standard out.
        """
        super(pricePredictionAgent,self).printSummary()
        
        #if self.pricePrediction != None:
        if 'pointPricePrediction' in args or self.pricePrediction != None:
            
            if 'pointPricePrediction' in args:
                if isinstance(args['pointPricePreciction'],pointSCPP):
                    pricePrediction = args['pointPricePrediction'].data
                elif isinstance(args['pointPricePrediciton'],numpy.ndarray):
                    pricePrediction = args['pointPricePrediction']
            else:
                pricePrediction = self.pricePrediction.data
            
            print 'Price Prediction = {0}'.format(pricePrediction)
            
            print 'Bundle | Valuation | Cost | Surplus'
            
            bundles = self.allBundles(self.m)
            
            valuation = self.valuation(bundles = bundles, 
                                             v = self.v, 
                                             l = self.l)
            
            cost = self.cost(bundles = bundles, 
                             price   = pricePrediction)
            
            surplus = self.surplus(bundles     = bundles, 
                                   valuation   = valuation, 
                                   priceVector = pricePrediction)
            
            for i in xrange(bundles.shape[0]):
                print "{0}  {1:^5} {2:^5} {3:^5}".format( bundles[i].astype(numpy.int),
                                                          valuation[i],
                                                          cost[i],
                                                          surplus[i])
            
            optBundle = []
            optSurplus = []
                        
            [optBundle, optSurplus] = self.acq(priceVector=pricePrediction)
            
            print "Optimal Bundle (acq):      {0}".format(optBundle.astype(numpy.int))
            print "Surplus of Optimal Bundle: {0}".format(optSurplus)
            print "Bid:                       {0}".format(self.bid())
        else:
            print 'No point price prediction information provided...'
            
    def bid(self, args={}):
        """
        Interface to bid.
        Will accept an argument of pointPricePrediction which
        will take precidence over any stored prediction
        """
        bundles = self.allBundles(self.m)
        
        if 'pointPricePrediction' in args:
            if isinstance(args['pointPricePrediction'],pointSCPP):
                return self.SS({'pointPricePrediction':args['pointPricePrediction'].data,
                                'bundles':bundles,
                                'l':self.l,
                                'valuation': simYW.valuation(bundles,self.v,self.l)})
                
            elif isinstance(args['pointPricePrediction'],numpy.ndarray):
                return self.SS({'pointPricePrediction':args['pointPricePrediction'],
                                 'bundles':bundles,
                                 'l':self.l,
                                 'valuation': simYW.valuation(bundles,self.v,self.l)})
            else:
                print '----ERROR----'
                print 'pointPredictionAgent::bid'
                print 'unkown pointPricePrediction type'
                raise AssertionError
            
        else:
            assert isinstance(self.pricePrediction,pointSCPP),\
                "Must specify a price prediction to bid." 
            return self.SS({'pointPricePrediction':self.pricePrediction.data,
                            'bundles':bundles,
                            'l':self.l,
                            'valuation': simYW.valuation(bundles,self.v,self.l)})
            