"""
this is /auctionSimulator/hw4/agents/riskAware.py

Author:    Brandon A. Mayer
Date:      12/6/2011
"""

from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.agents.targetMVS import *

class riskAwareTMVS8(riskAware):
    @staticmethod
    def type():
        return "riskAwareMUS8"
    
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
        
        return targetMVS.bundleBid({'bundle'                : optBundle,
                                    'valuation'             : args['valuation'],
                                    'pointPricePrediction'  : expectedPrices,
                                    'l'                     : args['l']})
        