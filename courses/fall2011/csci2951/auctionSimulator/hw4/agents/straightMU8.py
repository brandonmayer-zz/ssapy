"""
this is /auctionSimulator/hw4/agents/straightMU8.py

Author:    Brandon A. Mayer
Date:      12/5/2011

Specialized agent to bid by straightMU strategy but sampling from
marginal distributions using the inverse transform method using 8 samples
per marginal distribution
"""

from auctionSimulator.hw4.agents.straightMU import *

class straightMU8(straightMU):
    """
    A concrete class for straightMU8
    """
    @staticmethod
    def type():
        return "straightMU8"
    
    @staticmethod
    def SS(args={}):
        
        return straightMU.SS( {'margDistPrediction' : args['margDistPrediction'],
                               'method'             : 'iTsample',
                               'nSamples'           : 8,
                               'bundles'            : args['bundles'],
                               'valuation'           : args['valuation'],
                               'l'                  : args['l']} )
        
    def printSummary(self):
        super(straightMU8,self).printSummary({'method'   : 'iTsample',
                                              'nSamples' : 8})