"""
this is /auctionSimulator/hw/pricePredicitons/symmetricDistributionPricePrediction.py

Author: Brandon A. Mayer
Date:   11/19/2011

Because the multiprocessing python module must be executed as a script
this is a command line interface script for generating Self Confirming 
Distribution Price Predicitons from Yoon & Wellman 2011 executing the each game
in parallel.

Very similar in form and function to symmetricPointPricePrediciton.py script in the same
directory
"""

from auctionSimulator.hw4.agents.straightMU import *

import argparse
import matplotlib.pyplot as plot
import multiprocessing
import numpy
import time
import os

class symmetricDPPworker(object):
    """
    Functor to facilitate concurrency in symmetric self confirming price prediction (Yoon & Wellman 2011)
    
    Due to the homogeneity of the "games" defined in the self confirming price prediction,
    We can specify an agent type and the number of goods that will participate in all acutions.
    
    Therefore create an instance of this class with the correct parameters then we can use
    multiprocessing.Pool.map to pass a single argument to the callable class.
    
    When this class is called, it instantiates a new agent (so that each concurrent process
    is run with a completely different agent) and returns a unique bid instance.
    """
    def __init__(self,agentType='straightMU', m = 5):
        # store values for specific initialization
        self.agentType = agentType
        self.m         = m

    def __call__(self, margDistPrediciton = None):
        """
        Make the class callable with a single argument for multiprocessing.Pool.map()
        """
        agent = None
        
        assert margDistPrediction != None,\
            "Must provide a marginal distribution price prediciton"
        
        if self.agentType == 'straightMU':
            agent = straightMU(m=self.m)
        else:
            print 'symmetricDPPworker.__call(self.margDistPrediction)'
            print 'Unknown Agent Type: {0}'.format(agentType)
            raise AssertionError
        
        return numpy.array(agent.bid({'margDistPrediction': margDistPrediciton})).astype('float')

def main():
    desc = 'Parallel Implementation of Self Confirming Distribution Price Prediction (Yoon & Wellman 2011)'
    
if __name__ == "__main__":
    main()
        
        

