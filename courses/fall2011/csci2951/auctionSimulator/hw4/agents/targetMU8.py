"""
this is /auctionSimulator/hw4/agents/targetMU8.py

Author:    Brandon A. Mayer
Date:      12/5/2011

Specialized agent to bid by targetMU strategy but sampling from
marginal distributions using the inverse transform method using 8 samples
per marginal distribution
"""

from auctionSimulator.hw4.agents.targetMU import *

class targetMU8(targetMU):
    """
    A concrete class for targetMU8
    """
    
    @staticmethod
    def type():
        return "targetMU8"
    
    @staticmethod
    def SS(args={}):
        return targetMU.SS({'margDistPrediction' : args['margDistPrediction'],
                            'method'             : 'iTsample',
                            'nSamples'           : 8,
                            'bundles'            : args['bundles'],
                            'valuation'          : args['valuation'],
                            'l'                  : args['l']})
        
    def printSummary(self):
        super(targetMU8,self).printSummary({'method'   : 'iTsample',
                                              'nSamples' : 8})