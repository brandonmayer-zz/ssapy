from ssapy.agents.agentFactory import agentFactory
from ssapy.pricePrediction.margDistSCPP import margDistSCPP
from ssapy.pricePrediction.jointGMM import jointGMM

import numpy

import multiprocessing

def hobAuction(**kwargs):
    """
    Function to simulate an auction and record other highest agent bids.
    
    Parameters
    ----------
    agentTypeList : list of strings, required
        Types of agents in the auction.
        
    selfIdx : int, zero indexed, 0 <= selfIdx < len(agentTypeList)
        Index for agent in list representing self.
        
    nGames : int, optional 
        Number of simulations to run. Defaults to 10,000
        
    parallel : bool, optional
        Run simulations in parallel or serial (mainly for debugg). Defaults True.
        simulateAuctionJointGMM
    pricePrediction : Either margDistSCPP or jointGMM instance 
        Price Predictions for agents to use.
                
    m := int, optional
        Number of goods up for auction. Defaults to 5.
        
    vmin : float, optional 
        Minimum allowable valuation. Defaults to 0.
        
    vmax : float, optional
        Maximum allowable valuation. Defaults to 50.
           
    outputs
    -------
    highestOtherBids : ndarray (nGames,m)
        Array of highest other agent bids.
    """
    
    agentTypeList   = kwargs.get('agentTypeList')
    selfIdx         = kwargs.get('selfIdx')
    nGames          = kwargs.get('nGames')
    parallel        = kwargs.get('parallel',True)
    pricePrediction = kwargs.get('pricePrediction')
    
    m    = kwargs.get('m',5)
    vmin = kwargs.get('vmin',0)
    vmax = kwargs.get('vmax',50)
    
    highestOtherBids = numpy.zeros(nGames,m)
    
    if parallel:
        pass
    
    else:
        n = len(agentTypeList)
    
        agents = [agentFactory(agentType = agentType, m = m, vmin = vmin, vmax = vmax) for agentType in agentTypeList]
    
        otherAgents = numpy.delete(numpy.arange(n),selfIdx,0)
    
        bids = numpy.zeros(n,m)
        
        for itr in xrange(nGames):
            
            if isinstance(pricePrediction,list):
                for idx, agent, pp in zip(numpy.arange(n),agents,pricePrediction):
                    #draw a new valuation
                    agent.randomValuation()
                    bids[idx] = agent.bid(pricePrediction = pp)
            else:
                for idx, agent in enumerate(agents):
                    #draw a new valuation
                    agent.randomValuation()
                    bids[idx] = agent.bid(pricePrediction = pricePrediction)
                
                
            highestOtherBids = numpy.max(bids[otherAgents],0)
            
    return highestOtherBids

if __name__ == "__main__":
    
            
    
    
    
    
    
    
        
     
    
    