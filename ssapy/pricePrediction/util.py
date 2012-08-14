import numpy
from ssapy.agents.straightMU import *
from ssapy.agents.targetMU import *
from ssapy.agents.targetMUS import *
from ssapy.agents.targetPriceDist import *
from ssapy.agents.riskAware import *
from ssapy.pricePrediction.margDistSCPP import margDistSCPP
from sklearn import mixture
import matplotlib.pyplot as plt

import time
import os
import itertools

def apprxMargKL(clf1, clf2, nSamples = 1000):
    
    kl = 0
    for idx, c1 in enumerate(clf1):
        c2 = clf2[idx]
        samples1 = c1.sample(nSamples)
        samples2 = c2.sample(nSamples)
        f1 = c1.eval(samples1)[0]
        g1 = c2.eval(samples1)[0]
        f2 = c1.eval(samples2)[0]
        g2 = c2.eval(samples2)[0]
        d1 = numpy.mean(f1/g1)
        d2 = numpy.mean(f2/g2)
        kl += (d1 + d2)
    return kl

def plotMargGMM(**kwargs):
    clfList = kwargs.get('clfList')
    oFile   = kwargs.get('oFile')
    minPrice = kwargs.get('minPrice',0)
    maxPrice = kwargs.get('maxPrice',50)
    colors   = kwargs.get('colors', ['r','g','b','k','m','c','y'])
    
    title   = kwargs.get('title', "Marginal Gaussian")
    xlabel  = kwargs.get('xlabel', "price")
    ylabel  = kwargs.get(r"$p(closing price)$")
    
    colorCycle = itertools.cycle(colors)
    m = len(clfList)
    x = numpy.linspace(minPrice, maxPrice, (maxPrice-minPrice)*5 , endpoint = True)
    
    fig = plt.figure()
    ax = plt.subplot(111)
    for idx, clf in enumerate(clfList):
#        a = clf.eval(x)
        plt.plot(x,numpy.exp(clf.eval(x)[0]),
                 color=next(colorCycle),
                 label = 'good {0}'.format(idx))
        
    leg = ax.legend(loc = 'best',fancybox = True)
    leg.get_frame().set_alpha(0.5)
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.savefig(oFile)
    
#    fig.remove()
    
def aicFit(X, compRange = range(1,6), minCovar = 9, verbose = True):
    if verbose:
        print 'starting aicFit(...)'
        print 'compRange = {0}'.format(compRange)
        print 'minCovar  = {0}'.format(minCovar)
        start = time.time()
        
    clfList = [mixture.GMM(n_components = c, min_covar = minCovar) for c in compRange]
    
    [clf.fit(X) for clf in clfList]
    
    aicList = [clf.aic(X) for clf in clfList]
    
    argMinAic = numpy.argmin(aicList)
    
    if verbose:
        print 'Finished aicFit(...) in {0} seconds'.format(time.time()-start)
        
    return clfList[argMinAic], aicList, compRange

def drawGMM(clf, nSamples = 8, minPrice = 0, maxPrice = 50):
    
    samples = []
#    for i in xrange(nSamples):
    while len(samples) < nSamples:
        s = clf.sample(1)[0]
        if s < maxPrice and s > minPrice:
            samples.append(s)
    samples = numpy.atleast_2d(samples)     
    return samples
    
def ksStat(margDist1 = None, margDist2 = None):
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

def klDiv(margDist1, margDist2):
    assert isinstance(margDist1, margDistSCPP) and\
            isinstance(margDist2, margDistSCPP),\
        "margDist1 and margDist2 must be instances of margDistSCPP"
        
    numpy.testing.assert_equal(margDist1.m, 
                               margDist2.m)
    
    kldSum = 0.0
    for idx in xrange(margDist1.m):
        # test that the distributions are over the same bin indices
        # if they are not this calculation is meaninless
        numpy.testing.assert_equal(margDist1.data[idx][1],
                                   margDist2.data[idx][1])
        
        #test that the distributions have the same number of bins
        numpy.testing.assert_equal(len(margDist1.data[idx][0]),
                                   len(margDist2.data[idx][0]))
        
        m1 = margDist1.data[idx][0]
        m1[m1==0] = numpy.spacing(1)
        m2 = margDist2.data[idx][0]
        m2[m2==0] = numpy.spacing(1)
        
             
        kldSum += numpy.sum(margDist1.data[idx][0] * (numpy.log(margDist1.data[idx][0]) 
                                               - numpy.log(margDist2.data[idx][0])))

        
    return kldSum

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
        
        elif self.args['agentType'] == 'straightMU8':
            agentList = [straightMU8(m=self.args['m']) for i in xrange(self.args['nAgents'])]
            
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
        
        elif self.args['agentType'] == 'targetMUS8':
            agentList = [targetMUS8(m=self.args['m']) for i in xrange(self.args['nAgents'])]
            
            bids = numpy.atleast_2d([agent.bid(margDistPrediction = margDistPrediciton) for agent in agentList])
            
            return numpy.max(bids,0)
        
        elif self.args['agentType'] == 'targetMU8':
            agentList = [targetMU8(m=self.args['m']) for i in xrange(self.args['nAgents'])]
            
            bids = numpy.atleast_2d([agent.bid(margDistPrediction = margDistPrediciton) for agent in agentList])
            
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