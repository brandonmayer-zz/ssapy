import unittest
import numpy

from ssapy.auctions import simulateAuction,collectBids
from ssapy.pricePrediction.jointGMM import jointGMM

from ssapy import agentFactory


class test_simulateAuction(unittest.TestCase):
    def test_simulateAuction_straightMUa(self):
        agentType = "msStraightMUa"
        pricePrediction = jointGMM(n_components=2)
        pricePrediction.means_  = numpy.asarray([[10,5], [0,5]],dtype='float')
        pricePrediction.weights_ = numpy.asarray([0.5,0.5],dtype = 'float')
        
        bids = simulateAuction(agentType = agentType, nAgents = 5, nGames = 10, nProc = 5, m = 2, pricePrediction = pricePrediction, ret = 'bids')
        
#        print bids
        
    def test_collectBids(self):
        agentType = "msStraightMUa"
        pricePrediction = jointGMM(n_components=2)
        pricePrediction.means_  = numpy.asarray([[10,5], [0,5]],dtype='float')
        pricePrediction.weights_ = numpy.asarray([0.5,0.5],dtype = 'float')
        nAgents = 5
        v = [20.,10.]
        l = 1
        agentList = [agentFactory(agentType = agentType, pricePrediction = pricePrediction, v = v, l = l) for i in xrange(nAgents)]
        
        bids = collectBids(agentList)
        
        true_bids = numpy.asarray([[15.,0.],[15.,0.],[15.,0.],[15.,0.],[15.,0.]])
        
        numpy.testing.assert_equal(bids,true_bids)
        
        
        
        
        
if __name__ == "__main__":
    unittest.main()
    