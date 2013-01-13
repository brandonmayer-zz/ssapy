import unittest
import numpy

from ssapy import agentFactory

class test_agentFactory(unittest.TestCase):
    def test_straightMV(self):
        agentType = "msStraightMV"
        pp = numpy.asarray([5.,5.])
        v = [20.,10.]
        l = 1
        
        agent = agentFactory(agentType = agentType, v = v, l = l, pricePrediction = pp )
        
        numpy.testing.assert_equal(agent.bid(), numpy.asarray([15.,0.],dtype='float'), "test_agentFactory.test_straightMV failed.", True)
        
        
if __name__ == "__main__":
    unittest.main()