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
    
def ksStatistic(margDist1 = None, margDist2 = None):
    """
    A helper function for computing the maximum Kolmogorov-Smirnov (KS)
    statistic over marginal price distributions
    
    KS(F,F') = max_x |F(x) - F'(x)|
    
    Yoon & Wellman 2011 take the maximum over each of the KS 
    statistics seperately for each good:
    KS_marg = max_j KS(F_j,F'_j)
    """
    
    assert isinstance(margDist1, margDistSCPP) and\
            isinstance(margDist2, margDistSCPP),\
        "margDist1 and margDist2 must be instances of margDistSCPP"
        
    #use numpy assertions b/c they can't be turned off at 
    #compile time
    numpy.testing.assert_equal(margDist1.m, 
                               margDist2.m)
    margKs = []
    for idx in xrange(margDist1.m):
        numpy.testing.assert_equal(margDist1.data.shape,
                                   margDist1.data.shape)
        cs1 = numpy.cumsum(margDist1.data[idx][0])
        cs2 = numpy.cumsum(margDist2.data[idx][0])
        margKs.append(numpy.max(numpy.abs(cs1-cs2)))
        
    return numpy.max(numpy.atleast_1d(margKs)) 

def updateDist(currDist = None, newDist = None, kappa = None, verbose = True):
    
    assert isinstance(currDist, margDistSCPP),\
        "margDist1 must be an instance of margDistSCPP"
        
    assert isinstance(newDist, margDistSCPP),\
        "margDist2 must be an instance of margDistSCPP"
        
    assert isinstance(kappa,float) or isinstance(kappa,int),\
        "kappa must be a floating point number or integer"        
    
    numpy.testing.assert_equal(currDist.m, newDist.m)
    
    
    
    updatedDistData = []
    for idx in xrange(margDist.m):
        # test that the distributions are over the same bin indices
        # if they are not this calculation is meaninless
        
        numpy.testing.assert_equal(currDist.data[idx][1],currDist.data[idx][1])
        updatedDistData = currDist.data[idx][0] + kappa*(currDist.data[idx][0] - newDist.data[idx][0])
        # re-normalize for safety
        updatedDistData.astype(numpy.float)/numpy.sum(updatedDistData)
        
    return margDistSCPP(updatedDistData)
    

def main():
    desc = 'Parallel Implementation of Self Confirming Distribution Price Prediction (Yoon & Wellman 2011)'
    
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--agentType',     action='store', dest='agentType',              default='baselineBider')
    
    parser.add_argument('--outDir',        action='store', dest='outDir',   required=True)
    
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
    
    #add more agents as they are implemented
    assert args['agentType'] == 'straightMU',\
        "Unknown Agent Type {0}".format(args['agentType'])

    verbose = not args['supressOutput']
    
    

    #initial uniform distribution
    tempDist = []
    p = float(1)/round(args['maxPrice']-args['minPrice'])
    a = [p]*(args['maxPrice']-args['minPrice'])
    binEdges = [bin for bin in xrange( int(args['maxPrice']-args['minPrice'])+1 ) ]
    for i in xrange(args['m']):
        tempDist.append((numpy.atleast_1d(a),numpy.atleast_1d(binEdges)))
        
    currentDist = margDistSCPP(tempDist)
    
    #clean up
    del p,a,binEdges,tempDist
        
      
    if verbose:
        print'Computing Symmetric Self Confirming Point Price Prediction.'
        
        print'Agent Type                   = {0}'.format(args['agentType'])
        
        print 'Termination Threshold (d)  = {0}'.format(args['d'])
        
        print'Number of Iterations        = {0}'.format(args['L'])
        
        print'Number of Games             = {0}'.format(args['g'])
        
        print'Number of Items per Auction = {0}'.format(args['m'])
        
        print 'Using Dampining             = {0}'.format(args['noDampen'])
        
        print'Number of Parallel Cores    = {0}'.format(args['NUM_PROC'])
        
        print'Output Directory             = {0}'.format(args['outDir'])
    
    
    # Store local variables that will be needed in loops
    # so we don't have to look up in args dictionary
    # every iteration (swap memory for cpu cycles)
    L = args['L']
    dampen = not args['noDampen']
    g = args['g']    
    delta = args['d']
    ksStat=numpy.zeros(L,dtype=numpy.float64)
    
    kappa = 1
    for t in xrange(0,L):
        print ""
        pool = multiprocessing.Pool(processes=args['NUM_PROC'])
        
        if verbose:
            print 'Iteration: {0}'.format(t)
            
        # set up the dampining constant if so specified
        if dampen:
            kappa = float(L-t)/L
            
        if verbose:
            parallelStart = time.clock()
                
            # Run all games in parallel
            # use iterator object to conserve memory, the arguments 
            # are only returned when needed instead of storeing the whole list
        result = numpy.atleast_2d(pool.map(symmetricDPPworker, itertools.repeat(currentDist,times = g))).astype('float64')
            
        pool.close()
            
        pool.join()
            
        if verbose:
            parallelFinish = time.clock()
            print 'Finished {0} games in {1} seconds.'.format(g, parallelFinish-parallelStart)
   
        if verbose:
            histStart=time.clock()  
                   
        histData = [] 
        for m in xrange(result.shape[1]):
            histData.append(numpy.histogram(result[:,m]))
            
        if verbose:
            histEnd = time.clock()
            print 'Histogramed {0} distributions of {1} games in {2} seconds'.\
                format(result.shape[1],g,histFinish-histStart)
                
        newDist = margDistSCPP(histData)
        

        
        ksStat[t] =  ksStatistic(margDist1 = currentDist, margDist2 = newDist)
        
        if verbose:
            print 'KS Statistic between Successive Iterations = {0}'.format(ksStat[t])
        
        if ksStat[t] <= delta:
            pricePredictionPklFilename = os.path.join(args['outDir'], 
                                                          'distPricePrediction_{0}_{1}_{2}_{3}_{4}_{5}.pkl'.format(agentType,
                                                                                                                    args['g'],
                                                                                                                    date.today().year,
                                                                                                                    date.today().month,
                                                                                                                    date.today().day,
                                                                                                                    int(time.time())))
            
            
            pass
            
        
        
   
        
        
            
            
                
            
    
if __name__ == "__main__":
    main()
        
        

