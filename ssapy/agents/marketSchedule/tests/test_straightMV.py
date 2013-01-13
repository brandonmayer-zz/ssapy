import unittest
import numpy

from ssapy.agents.marketSchedule.straightMV import straightMV

class test_straightMV(unittest.TestCase):
    def test1(self):
        pp = numpy.asarray([5.,5.], dtype = 'float')
        m = 2
        l = 1
        v = [20,10]
        agent = straightMV(m = m, l = l, v = v, pricePrediction = pp)
        numpy.testing.assert_equal(agent.bid(), numpy.asarray([15.,0.],dtype = 'float'), "test_straightMV - test1 failed.", True)
        
if __name__ == "__main__":
    unittest.main()
        