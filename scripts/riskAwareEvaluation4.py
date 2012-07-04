from auctionSimulator.hw4.auctions.simultaneousAuction import *
from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.agents.riskAwareTP8      import *
from auctionSimulator.hw4.agents.riskAwareExpTP8   import *
from auctionSimulator.hw4.agents.riskAwareTMVS8    import *
from auctionSimulator.hw4.agents.riskAwareExpTMVS8 import *
from auctionSimulator.hw4.agents.straightMU8 import *
from auctionSimulator.hw4.agents.targetMU8 import *
from auctionSimulator.hw4.agents.targetMUS8 import *
from auctionSimulator.hw4.agents.targetPriceDist import *

import numpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import multiprocessing
import time
import itertools

class parallelWorker(object):
    def __init__(self, margDistPrediction = None, nGames = 100, A = 10):
        numpy.testing.assert_(isinstance(margDistPrediction, margDistSCPP),
                              msg='Must Specify a marginal price prediction distribution')
        
        numpy.testing.assert_(isinstance(nGames,int),
                              msg='Must specify an integer number of games')
        
        self.margDistPrediction = margDistPrediction
        self.nGames = nGames
        self.A = A
        
    def __call__(self,dummy=0):
        
        agentList = []
        
        agentList.append(targetPriceDist(margDistPricePrediction = self.margDistPrediction,
                                         name                    = 'targetPrice'))
        
        agentList.append(riskAware(margDistPricePrediction = self.margDistPrediction,
                                   A                       = self.A,
                                   name                    = 'riskAware_A={0}'.format(self.A)))
        
        agentList.append(riskAwareTP8(margDistPricePrediction = self.margDistPrediction,
                                      A                       = self.A,
                                      name                    = 'riskAware_A={0}'.format(self.A)))
        
        agentList.append(riskAwareTMVS8(margDistPricePrediction = self.margDistPrediction,
                                        A                       = self.A,
                                        name                    = 'riskAware_A={0}'.format(self.A)))
        
        agentList.append(riskAwareExpTP8(margDistPricePrediction = self.margDistPrediction,
                                         A                       = self.A,
                                         name                    = 'riskAware_A={0}'.format(self.A)))
        
        agentList.append(riskAwareExpTMVS8(margDistPricePrediction = self.margDistPrediction,
                                           A                       = self.A,
                                           name                    = 'riskAware_A={0}'.format(self.A)))
        
        
        agentList.append(straightMU8(margDistPricePrediction = self.margDistPrediction,
                                    name                    = 'straighMU8'))
        
        agentList.append(targetMU8(margDistPricePrediction = self.margDistPrediction,
                                    name                    = 'targetMU8'))
        
        agentList.append(targetMUS8(margDistPricePrediction = self.margDistPrediction,
                                    name                    = 'targetMUS8'))
        
        agentSurplus = []
        
        for g in range(0,self.nGames):
#            print 'Iteration = {0}'.format(g)
            v = numpy.random.random_integers(low=0,high=50,size=5)
            v.sort() 
            #sort is in ascending order, 
            #switch around for descending
            v = v[::-1] 
            l = numpy.random.random_integers(low=1,high=5)
            
            #each game set all the valuations and lambdas to be equal 
            #for fair evaulation (symmetric game)
            for agent in agentList:
                agent.v = v
                agent.l = l
                
            auction = simultaneousAuction(agentList)
            
            auction.runAuction()
            
            auction.notifyAgents()
            
            agentSurplus.append(auction.agentSurplus())
            
        return numpy.atleast_2d(agentSurplus).astype(numpy.float)
            
def main():
    nGames = 1000
    
    NUM_PROC = 10
    
#    A = 20
    
    margDistPkl = "C:\\bmProjects\\courses\\fall2011\\csci2951\\" +\
                  "auctionSimulator\\hw4\\pricePrediction\\margDistPredictions\\" +\
                  "distPricePrediction_straightMU_10000_2011_12_4_1323040769.pkl"
                  
    margDistPrediction = margDistSCPP()
    
    margDistPrediction.loadPickle(margDistPkl)
    
    parallel = True
    
    colors = ['r','g','b','k','c','y']
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    alpha = 0.8
     
    agentNames = []
    agentNames.append('targetPrice')
    agentNames.append('riskAware')
    agentNames.append('riskAwareTP8')
    agentNames.append('riskAwareTMVS8')
    agentNames.append('riskAwareExpTP8')
    agentNames.append('riskAwareExpTMVS8')
    agentNames.append('straighMU8')
    agentNames.append('targetMU8')
    agentNames.append('targetMUS8')
    
    ind = numpy.arange(len(agentNames))
    
    for A in xrange(0,100,10):
        
        pw = parallelWorker(margDistPrediction = margDistPrediction, 
                            nGames             = nGames,
                            A                  = A)
        
        pool = multiprocessing.Pool(processes = NUM_PROC)
        
        
        
        print 'Computing Result for A = {0}'.format(A)
        
        start = time.clock()
        if parallel:
            result = numpy.atleast_2d( pool.map(pw,xrange(0,NUM_PROC)) ).astype(numpy.float)
            
            pool.close()
            pool.join()
        else:
            result = numpy.atleast_2d([r for r in itertools.imap(pw,xrange(0,NUM_PROC))]).astype(numpy.float)
        finish = time.clock()
        
        print 'Finished {0} games in {1}'.format(nGames*NUM_PROC,finish-start)
        
        result = numpy.reshape( result,(result.shape[0]*result.shape[1],result.shape[2]) )
        
        surplusMean = numpy.mean(result,0)
        
        #
  
        #pick a color randomly
        c = colors[numpy.random.random_integers(0,len(colors)-1)]
        
        ax.bar(ind,
               surplusMean,
               zs = A,
               zdir='y',
               color    = [c]*ind.shape[0],
               alpha = alpha) 

#        
#    width = 0.35
#    
#    fig = plt.figure()
#    ax = fig.add_subplot(111)
#    ax.bar(ind,surplusMean,width)
    plt.xticks(ind + .5,tuple(agentNames))
    ax.set_zlabel('Average Surplus')
    ax.set_ylabel('A')
    plt.title('Symmetric Valuation, $\lambda$, and Distribution Prediction {0} games for all values of A'.format(nGames*NUM_PROC))
    
    plt.show()
    
if __name__ == "__main__":
    main()