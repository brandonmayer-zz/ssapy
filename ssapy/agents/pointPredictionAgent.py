"""
This is /auctionSimulator/hw4/agents/pointPredictionAgent.py

Author:        Brandon A. Mayer
Date:          11/27/2011

A base class for agents who utilize a point price prediction.
"""

from pricePredictionAgent import *
from aucSim.pricePrediction.pointSCPP import *
from aucSim.padnums import pprint_table as ppt

import sys

class pointPredictionAgent(pricePredictionAgent):   
    def __init__(self,**kwargs):
        
        if 'pointPricePrediction' in kwargs:
           kwargs['pricePrediction'] = kwargs['pointPricePrediction']
           
        super(pointPredictionAgent,self).__init__(**kwargs)
        
    @staticmethod
    def predictionType():
        return "pointSCPP"
    
    @staticmethod
    def type():
        return "pointPredictionAgent"
    
    def printSummary(self,**kwargs):
        """
        Print a summary of agent's state to standard output.
        """
        super(pointPredictionAgent,self).printSummary()
        
        #if self.pricePrediction != None:
        if 'pointPricePrediction' in kwargs or self.pricePrediction != None:
            
            if 'pointPricePrediction' in kwargs:
                if isinstance(kwargs['pointPricePrediction'],pointSCPP):
                    pricePrediction = kwargs['pointPricePrediction'].data
                elif isinstance(kwargs['pointPricePrediciton'],numpy.ndarray):
                    pricePrediction = kwargs['pointPricePrediction']
            else:
                pricePrediction = self.pricePrediction.data
            
            print 'Price Prediction = {0}'.format(pricePrediction)
            
#            print 'Bundle | Valuation | Cost | Surplus'
            
            
                     
            
            bundles = self.allBundles(self.m)
            
            valuation = self.valuation(bundles = bundles, 
                                             v = self.v, 
                                             l = self.l)
            
            cost = self.cost(bundles = bundles, 
                             price   = pricePrediction)
            
            surplus = self.surplus(bundles     = bundles, 
                                   valuation   = valuation, 
                                   priceVector = pricePrediction)
            
            table = [["Bundle", "Valuation", "Cost", "Surplus"]]
            
            
            for i in xrange(bundles.shape[0]):
                table.append([str(bundles[i].astype(numpy.int)), valuation[i], cost[i], surplus[i]])
#                print "{0}  {1:^5} {2:^5} {3:^5}".format( bundles[i].astype(numpy.int),
#                                                          valuation[i],
#                                                          cost[i],
#                                                          surplus[i])
            ppt(sys.stdout, table)
                        
            [optBundle, optSurplus] = self.acq(priceVector=pricePrediction)
            
            print "Optimal Bundle (acq):      {0}".format(optBundle.astype(numpy.int))
            print "Surplus of Optimal Bundle: {0}".format(optSurplus)
#            print "Bid:                       {0}".format(self.bid({'pointPricePrediction':pricePrediction}))
            print "Bid:                       {0}".format(self.bid(pointPricePrediction = pricePrediction))
            print ''
        else:
            print 'No point price prediction information provided...'
            
    def bid(self, **kwargs):
        """
        Interface to bid.
        Accepts an argument of pointPricePrediction which
        will take precidence over any stored prediction
        """
        bundles = self.allBundles(self.m)
        
        if 'pointPricePrediction' in kwargs:
            if isinstance(kwargs['pointPricePrediction'],pointSCPP):
                return self.SS(pointPricePrediction = kwargs['pointPricePrediction'].data,
                               bundles              = bundles,
                               l                    = self.l,
                               valuation            = simYW.valuation(bundles,self.v,self.l))
                
            elif isinstance(kwargs['pointPricePrediction'],numpy.ndarray):
                return self.SS(pointPricePrediction = kwargs['pointPricePrediction'],
                               bundles              = bundles,
                               l                    = self.l,
                               valuation            = simYW.valuation(bundles,self.v,self.l))
            else:
                print '----ERROR----'
                print 'pointPredictionAgent::bid'
                print 'unkown pointPricePrediction type'
                raise AssertionError
            
        else:
            assert isinstance(self.pricePrediction,pointSCPP),\
                "Must specify a price prediction to bid." 
            return self.SS( pointPricePrediction = self.pricePrediction.data,
                            bundles              = bundles,
                            l                    = self.l,
                            valuation            = simYW.valuation(bundles,self.v,self.l))
            