import unittest
import numpy

from ssapy.agents.marketSchedule.straightMU import straightMUa
from ssapy.pricePrediction.jointGMM import jointGMM

class test_straightMUa(unittest.TestCase):
    def test_straightMUa_jointGMM(self):
        pricePrediction = jointGMM()
        pricePrediction.means_  = numpy.asarray([[10,5], [0,5]],dtype='float')
        pricePrediction.weights_ = numpy.asarray([0.5,0.5],dtype = 'float')
        
        print pricePrediction.expectedValue()
        
        agent = straightMUa(pricePrediction = pricePrediction, v = [20.,10.], l = 1)
        
        numpy.testing.assert_equal(agent.bid(),[15.,0.], "test_straightMUa.test_straightMUa_jointGMM - failed.",True)
        
if __name__ == "__main__":
    unittest.main()
        