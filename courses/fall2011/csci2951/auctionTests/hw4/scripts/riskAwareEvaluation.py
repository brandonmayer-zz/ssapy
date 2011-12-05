from auctionSimulator.hw4.auctions.simultaneousAuction import *
from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.agents.straightMU import *
from auctionSimulator.hw4.agents.targetPriceDist import *

import numpy
import matplotlib.pyplot as plt

def main():
    
    margDistPkl = "C:\\bmProjects\\courses\\fall2011\\csci2951\\" +\
                  "auctionSimulator\\hw4\\pricePrediction\\margDistPredictions\\" +\
                  "distPricePrediction_straightMU_10000_2011_12_4_1323040769.pkl"
    
    margDistPrediction=margDistSCPP()
    
    margDistPrediction.loadPickle(margDistPkl)

    # i know this looks weird but I wanted to shuffle the agents
    # b/c we choose the winner of the auction by numpy.argmax(bids)
    # which returns the first highest argmax unfairly biasing the results
    # to whichever agent occupies the first spot in agentList
    # therefore I rancomly shuffle the agents but record results in a dictionary
        
    

    for i in xrange(20):
        print 'Iteration = {0}'.format(i)
        
        agentList = []
        
        riskAware1 = riskAware(margDistPricePrediction = margDistPrediction,
                           A                       = 0,
                           name                    = 'riskAware_A={0}'.format(0))
    
    
    
        agentList.append(targetPriceDist(margDistPricePrediction = margDistPrediction,
                                     v                       = riskAware1.v,
                                     name                    = 'targetPrice',
                                     l                        = riskAware1.l))
    
        agentDict[riskAware1.name] = []
        agentList.append(riskAware1)
    
        for A in xrange(1,30,2):
            agentList.append(riskAware(margDistPricePrediction = margDistPrediction,
                                   A                       = A,
                                   name                    = 'riskAware_A={0}'.format(A),
                                   v                       = riskAware1.v,
                                   l                       = riskAware1.l))
            
        if i == 0:
            for agent in agentList:
                agentDict[agent.name] = []
                
        numpy.random.shuffle(agentList)
                     
        auction = simultaneousAuction(agentList)
        
        auction.runAuction()
        
        auction.notifyAgents()
        
        for agent in agentList:
            agentDict[agent.name].append(agent.finalSurplus())
        

    agentNames = []
    agentMeans = []
    
    for agentName, surplusVector in agentDict.iteritems():
        agentNames.append(agentName)
        agentMeans.append(numpy.mean(surplusVector))
        
    
    ind = numpy.arange(len(agentNames))+.5
        
    width = 0.35
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(ind,agentMeans,width)
    plt.xticks(ind+width,tuple(agentNames))
    
    plt.show()
    
    
    
    
    
    

if __name__ == "__main__":
    main()