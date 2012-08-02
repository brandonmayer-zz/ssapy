from ssapy.multiprocessingAdaptor import Consumer
from ssapy.agents.agentFactory import margAgentFactory
from ssapy.pricePrediction.margDistSCPP import margDistSCPP

from ssapy.pricePrediction.util import klDiv, ksStat, updateDists

def simulateAuction( **kwargs ):
    agentType     = kwargs.get('agentType')
    nAgents       = kwargs.get('nAgnets')
    m             = kwargs.get('m')
    margDist = kwargs.get('margDist')
    
    agentList = [margAgentFactory(agentType = agentType, m = m) for i in xrange(nAgents)]
    
    bids = numpy.atleast_2d([agent.bid(margDistPrediction = margDist) for agent in agentList])
    
    return numpy.max(bids,0)

class yw2Task(object):
    def __init__(self, **kwargs):
        agentType = kwargs.get('agentType')
        nAgents   = kwargs.get('nAgents')
        m         = kwargs.get('m')
        margDist  = kwargs.get('margDist')
        nGames    = kwargs.get('nGames')
        
    def __call__(self):
        
        winningBids = numpy.array((nGames,m))
        for i in xrange(nGames):
            winningBids[i,:] = simulateAuction(agentType, nAgents, m, margDist, nGames)
            
        return winningBids
    
if __name__ == "__main__":
    tempDist = []
    p = float(1)/round(maxPrice - minPrice)
    a = [p]*(maxPrice - minPrice)
#    binEdges = [bin for bin in xrange( int(minPrice - maxPrice)+1 ) ]
    binEdges = numpy.arange(minPrice,maxPrice+1,1)
    for i in xrange(m):
        tempDist.append((numpy.atleast_1d(a),numpy.atleast_1d(binEdges)))
    
    margDist = margDistSCPP(tempDist)
    
    ywTask(agentType = "straightMU8",nAgents = 8, m = 5, margDist = margDist)
        
    winningBids = ywTask()
    
    pass    
             
        