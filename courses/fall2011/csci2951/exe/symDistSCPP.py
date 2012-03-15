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

from aucSim.agents.straightMU import *
from aucSim.agents.targetPriceDist import *
from aucSim.agents.riskAware import *

import argparse
from datetime import date
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
    def __init__(self, args={}):
        # store values for specific initialization
        
        numpy.testing.assert_('m' in args, 
                              msg="Must Specify m in args.")
        numpy.testing.assert_('agentType' in args, 
                              msg="Must specify the type of participating agents.")
        numpy.testing.assert_('nAgents' in args,
                              msg="Must specify the number of participating agents.")
        self.args = args
    def __call__(self, margDistPrediciton = None):
        """
        Make the class callable with a single argument for multiprocessing.Pool.map()
        """
        agent = None
        assert margDistPrediciton != None,\
            "Must provide a marginal distribution price prediciton"
        
        if self.args['agentType'] == 'straightMU':
            
            agentList = []
            for i in xrange(self.args['nAgents']):
                agentList.append(straightMU(m=self.args['m']))
            
            bids = numpy.atleast_2d([agent.bid(margDistPrediction = margDistPrediciton) for agent in agentList])
            
            #the winning bids at auction
            return numpy.max(bids,0)
        
        elif self.args['agentType'] == 'targetPriceDist':
            
            agentList = []
            for i in xrange(self.args['nAgents']):
                agentList.append(targetPriceDist(m=self.args['m']))
            
            
            bids = []
            if 'method' in self.args:
                if self.args['method'] == 'iTsample':
                    numpy.testing.assert_('nSamples' in self.args, msg = "Must provide nSamples parameter")
                    
                    bids = [agent.SS({'margDistPrediction': margDistPrediciton,
                                     'bundles'           : agent.allBundles(agent.m),
                                     'l'                 : agent.l,
                                     'valuation'         : agent.valuation(agent.allBundles(agent.m), agent.v, agent.l),
                                     'method'            : self.args['method'],
                                     'nSamples'          : self.args['nSamples']}) for agent in agentList]
                else:
                    bids =[numpy.array(agent.bid({'margDistPrediction': margDistPrediciton})).astype('float') for agent in agentList]
            
#            print [agent.l for agent in agentList]
            
#            [agent.printSummary({'margDistPrediction': margDistPrediciton}) for agent in agentList]
            
            return numpy.max(bids,0)
            
        elif self.args['agentType'] == 'riskAware':
            
#            agent = riskAware(m = self.args['m'])
            agentList = []
            for i in xrange(args['nAgents']):
                agentList.append(riskAware(m=self.args['m']))
            
            bids=[numpy.array(agent.bid({'margDistPrediction': margDistPrediciton})).astype('float') for agent in agentList]
            
            return numpy.max(bids,0)
            
        else:
            print 'symmetricDPPworker.__call(self.margDistPrediction)'
            print 'Unknown Agent Type: {0}'.format(agentType)
            raise AssertionError
        
        
    
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
        
        # test that the distributions are over the same bin indices
        # if they are not this calculation is meaninless
        numpy.testing.assert_equal(margDist1.data[idx][1],
                                   margDist2.data[idx][1])
        
        # cumulative sum of first distribution
        cs1 = numpy.cumsum(margDist1.data[idx][0])
        
        # cumulative sum of second distribution
        cs2 = numpy.cumsum(margDist2.data[idx][0])
        
        # record the maximum absoute difference between the 
        # cumulative sum over price probabilities
        margKs.append(numpy.max(numpy.abs(cs1-cs2)))
    
    # return the max over goods of the max absolute difference between
    # the cumulative sum over price probabilities
    return numpy.max(numpy.atleast_1d(margKs)) 

def updateDist(currDist = None, newDist = None, kappa = None, verbose = True, zeroEps = 0.00001):
    
    assert isinstance(currDist, margDistSCPP),\
        "margDist1 must be an instance of margDistSCPP"
        
    assert isinstance(newDist, margDistSCPP),\
        "margDist2 must be an instance of margDistSCPP"
        
    assert isinstance(kappa,float) or isinstance(kappa,int),\
        "kappa must be a floating point number or integer"        
    
    #test there exists a marginal distribution for each good
    numpy.testing.assert_equal(currDist.m, newDist.m)
    
    updatedDist = []
    for idx in xrange(currDist.m):
        
        # test that the distributions are over the same bin indices
        # if they are not this calculation is meaninless
        numpy.testing.assert_equal(currDist.data[idx][1],newDist.data[idx][1])
        
        #the update equation
        histTemp = currDist.data[idx][0] + kappa*(newDist.data[idx][0] - currDist.data[idx][0])
        
        #set all negative values to a value close to zero 
        #we don't want to set the price probability completely to zero
        #that way there is still some (small) chance of realizing that price
        histTemp[numpy.nonzero(histTemp < 0)] = zeroEps
        
        # re-normalize
        histTemp = histTemp.astype(numpy.float)/ \
                numpy.sum(histTemp*numpy.diff(currDist.data[idx][1]), dtype=numpy.float)
        
        # a bit pedantic but better safe than sorry...
        numpy.testing.assert_almost_equal(numpy.sum(histTemp*numpy.diff(currDist.data[idx][1]), dtype=numpy.float),
                                          numpy.float(1.0),
                                          err_msg = "Renomalization failed.")
        
        # make histogram, edge tuple
        updatedDist.append((histTemp, currDist.data[idx][1]))
    
    #insert into a marg dist wrapper and return
    return margDistSCPP(updatedDist)
    

def main():
    desc = 'Parallel Implementation of Self Confirming Distribution Price Prediction (Yoon & Wellman 2011)'
    
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--agentType',     action='store', dest='agentType',              default='straightMU')
    
    parser.add_argument('--outDir',        action='store', dest='outDir',   required=True)
    
    parser.add_argument('--nproc',         action='store', dest='NUM_PROC', type=int,    default=multiprocessing.cpu_count() )
    parser.add_argument('--m',             action='store', dest='m',        type=int,    default=5)
    parser.add_argument('--L',             action='store', dest='L',        type=int,    default=100)
    parser.add_argument('--d',             action='store', dest='d',        type=float,  default=0.05)
    parser.add_argument('--g',             action='store', dest='g',        type=int,    default=1000000)
    parser.add_argument('--pInitFile',     action='store', dest='pInitFile',type=int)
    parser.add_argument('--minPrice',      action='store', dest='minPrice', type=int,    default=0)
    parser.add_argument('--maxPrice',      action='store', dest='maxPrice', type=int,    default=50)
    parser.add_argument('--method',        action='store', dest='method',                default='average')
    parser.add_argument('--nSamples',      action='store', dest='nSamples', type=int,    default=8)
    parser.add_argument('--nAgents',       action='store', dest='nAgents',  type=int,    default=8)
    parser.add_argument('--serial',        action='store_true') #use serial implementation
    parser.add_argument('--noDampen',      action='store_true')
    parser.add_argument('--supressOutput', action='store_true')
    parser.add_argument('--writeTxt',      action='store_true')
    parser.add_argument('--plot',          action='store_true')
    
    
    
    args = parser.parse_args().__dict__
    
    if not os.path.isdir(args['outDir']):
        os.makedirs(args['outDir'])
    
    #add more agents as they are implemented
    assert args['agentType'] == 'straightMU' or\
           args['agentType'] == 'targetPriceDist' or\
           args['agentType'] == 'riskAware',\
        "Unknown Agent Type {0}".format(args['agentType'])
        
    #instantiate the worker object
#    sDPP = symmetricDPPworker(args['agentType'], args['m'])
    sDPP = symmetricDPPworker({'agentType' : args['agentType'],
                               'm'         : args['m'],
                               'method'    : args['method'],
                               'nSamples'  : args['nSamples'],
                               'nAgents'   : args['nAgents']})

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
    # keep the binEdges for later histograms
    del p,a,tempDist
        
      
    if verbose:
        print'Computing Symmetric Self Confirming Point Price Prediction.'
        
        print'Agent Type                   = {0}'.format(args['agentType'])
        
        print 'Termination Threshold (d)    = {0}'.format(args['d'])
        
        print'Number of Iterations        = {0}'.format(args['L'])
        
        print'Number of Games             = {0}'.format(args['g'])
        
        print'Number of Items per Auction = {0}'.format(args['m'])
        
        print 'Using Dampining             = {0}'.format(args['noDampen'])
        
        if args['serial']:
            print 'Using serial implementation'
        else:
            print'Number of Parallel Cores    = {0}'.format(args['NUM_PROC'])
            
        
        print'Output Directory            = {0}'.format(args['outDir'])
    
    
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
        
        if verbose:
            print 'Iteration: {0}'.format(t)
            
        # set up the dampining constant if so specified
        if dampen:
            kappa = float(L-t)/L
                    
        if verbose:
            print 'kappa = {0}'.format(kappa)
            gamesStart = time.clock()
            
        result = []
        if args['serial']:
            # use serial 1 core implementation
            result = numpy.atleast_2d([r for r in itertools.imap(sDPP, itertools.repeat(currentDist,times=g))]).astype(numpy.float)
        else:
            pool = multiprocessing.Pool(processes=args['NUM_PROC'])
            # Run all games in parallel
            result = numpy.atleast_2d( pool.map(sDPP, itertools.repeat(currentDist,times=g)) ).astype(numpy.float)
            pool.close()
            pool.join()
            
        if verbose:
            gamesFinish = time.clock()
            print 'Finished {0} games in {1} seconds.'.format(g, gamesFinish-gamesStart)
   
        if verbose:
            histStart=time.clock()  
                   
        histData = [] 
        histCount = []
        for m in xrange(result.shape[1]):
            histData.append(numpy.histogram(result[:,m],binEdges,density=True))
            histCount.append(numpy.histogram(result[:,m],binEdges,density=False))
            
        if verbose:
            histFinish = time.clock()
            print 'Histogramed {0} marginal distributions of {1} games {2} seconds'.\
                format(result.shape[1],g,histFinish-histStart)
                
        if verbose:
            updateStart = time.clock()
            
        updatedDist = updateDist(currDist = currentDist, 
                                 newDist = margDistSCPP(histData), 
                                 kappa = kappa, 
                                 verbose = verbose)
        
        if verbose:
            updateFinish = time.clock()
            print 'Updated distribution in {0} seconds.'.format(updateFinish-updateStart)
            
        
        if verbose:
            ksStart = time.clock()
                
        ksStat[t] =  ksStatistic(margDist1 = currentDist, margDist2 = updatedDist)
        
        if verbose:
            ksFinish = time.clock()
            print 'Calculated KS Statistic in {0} seconds.'.format(ksFinish-ksStart)
        
        
        
        if verbose:
            print 'Previous Expected Prices = {0}'.format(currentDist.expectedPrices())
            print 'New expected Prices      = {0}'.format(updatedDist.expectedPrices())
            print 'KS Statistic between Successive Iterations = {0}'.format(ksStat[t])
            
        
        if ksStat[t] <= delta:
            pricePredictionPklFilename = os.path.join(args['outDir'], 
                                                      'distPricePrediction_{0}_{1}_{2}_{3}_{4}_{5}.pkl'.format(args['agentType'],
                                                                                                               args['g'],
                                                                                                               date.today().year,
                                                                                                               date.today().month,
                                                                                                               date.today().day,
                                                                                                               int(time.time())))
            updatedDist.savePickle(pricePredictionPklFilename)
            
            if args['writeTxt']:
                pricePredictionTxtFilename = os.path.join(args['outDir'],
                                                          'distPricePrediction_{0}_{1}_{2}_{3}_{4}_{5}.txt'.format(args['agentType'],
                                                                                                                   args['g'],
                                                                                                                   date.today().year,
                                                                                                                   date.today().month,
                                                                                                                   date.today().day,
                                                                                                                   int(time.time())))
                #this section could be improved....
                testdata = []
                for m in xrange(updatedDist.m):
                    if m == 0:
                        textdata = numpy.vstack([updatedDist.data[m][0],updatedDist.data[m][1][:-1]])
                    else:
                        textdata = numpy.vstack([textdata, numpy.vstack([updatedDist.data[m][0],updatedDist.data[m][1][:-1]])])
                        
                numpy.savetxt(pricePredictionTxtFilename,textdata)
            
            print ''
            print'Terminated after {0} Iterations'.format(t)
            print'Final Expected Price Vector = {0}'.format(updatedDist.expectedPrices())
            
            if args['plot']:
                title = '{0} Self Confirming Price Distribution'.format(args['agentType'])
                updatedDist.graphPdf({'title':title})
                
            sys.exit()
            
            
        else:
            currentDist = updatedDist
            del updatedDist
            
        
if __name__ == "__main__":
    main()
        
        

