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
    
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--agentType',     action='store', dest='agentType',              default='baselineBider')
    
    parser.add_argument('--nproc',         action='store', dest='NUM_PROC', type = int,   default = multiprocessing.cpu_count() )
    parser.add_argument('--m',             action='store', dest='m',        type = int,   default = 5)
    parser.add_argument('--L',             action='store', dest='L',        type = int,   default = 100)
    parser.add_argument('--d',             action='store', dest='d',        type = float, default = 0.05)
    parser.add_argument('--g',             action='store', dest='g',        type = int,   default = 1000000)
    parser.add_argument('--pInitFile',     action='store', dest='pInitFile',type = int)
    parser.add_argument('--minPrice',      action='store', dest='minPrice', type = int,   default = 0)
    parser.add_argument('--maxPrice',      action='store', dest='maxPrice', type = int,   default = 50)
    
    parser.add_argument('--noDampen',      action='store_true')
    parser.add_argument('--supressOutput', action='store_true')
    parser.add_argument('--writeTxt',      action='store_true')
    parser.add_argument('--plot',          action='store_true')
    
    
    args = parser.parse_args().__dict__
    
    verbose = not args['supressOutput']
    
    # Store local variables that will be needed in loops
    # so we don't have to look up in args dictionary
    # every iteration (swap memory for cpu cycles)
    L = args['L']
    dampen = not args['noDampen']
    g = args['g']    
    delta = args['d']
    
    initDist = margDistSCPP()
    if args['pInitFile'] == None:
        tempDist = []
        for i in xrange(args['m']):
            a = [1]*int(args['maxPrice']-(args['maxPrice']))
            binEdges = [bin for bin in xrange( int(args['maxPrice']-args['minPrice'])+1 ) ]
            tempDist.append(numpy.histogram(a,binEdges,density=True))
        
        initDist.setPricePrediction(tempDist)
        
    else:
        initDist.loadPickle(args['pInitFile'])
        
        
    if verbose:
        print'Computing Symmetric Self Confirming Point Price Prediction.'
        
        print'Agent Type(s)               = {0}'.format(agentTypeList)
        
        print 'Termination Threshold (d)  = {0}'.format(args['d'])
        
        print 'pInit                       = {0}'.format(pInit)
        
        print'Number of Iterations        = {0}'.format(args['L'])
        
        print'Number of Games             = {0}'.format(args['g'])
        
        print'Number of Items per Auction = {0}'.format(args['m'])
        
        print 'Using Dampining             = {0}'.format(args['noDampen'])
        
        print'Number of Parallel Cores    = {0}'.format(args['NUM_PROC'])
        
        print'Output Directory             = {0}'.format(args['outDir'])
    
    
    
if __name__ == "__main__":
    main()
        
        

