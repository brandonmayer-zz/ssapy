"""
this is /auctionSimulator/hw4/agents/targetMUS8.py

Author:    Brandon A. Mayer
Date:      12/5/2011

Specialized agent to bid by targetMUS strategy but sampling from
marginal distributions using the inverse transform method using 8 samples
per marginal distribution
"""
from auctionSimulator.hw4.agents.targetMUS import *

class targetMUS8(targetMUS):
    """
    A concrete class for targetMUS8
    """
    @staticmethod
    def type():
        return "targetMUS8"
    
    @staticmethod
    def SS(args={}):
        return targetMUS.SS({'margDistPrediction' : args['margDistPrediction'],
                              'method'            : 'iTsample',
                              'nSamples'          : 8,
                              'bundles'           : args['bundles'],
                              'valuation'         : args['valuation'],
                              'l'                 : args['l']})
        
    def printSummary(self):
        super(targetMUS8,self).printSummary({'method'   : 'iTsample',
                                             'nSamples' : 8})