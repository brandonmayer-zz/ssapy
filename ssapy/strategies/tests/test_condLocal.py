import unittest
import numpy

from ssapy.strategies.condLocal import condLocalUpdate, condLocal, plotCondLocal
from ssapy import listBundles, msListRevenue


class test_condLocalBid(unittest.TestCase):
    def setUp(self):
        self.samples2d = numpy.atleast_2d([[1,1],   [20,3], [10,7], [15,5],
                                           [10,30], [15,26],[17,33], [2,40],
                                           [30,30], [27,42],[30,38], [29,40],
                                           [42,20], [38,7], [40,15], [33,10]])
        
        self.bundles2d = listBundles(2)
        self.l2d = 1
        self.v2d = [20,10] 
        self.revenue2d = msListRevenue(self.bundles2d, self.v2d, self.l2d)
    
    def test_condLocalUpdate(self):
        ibids = [25.,25.]
        print ibids
        targetBid = 0
        ibids[targetBid] = condLocalUpdate(self.bundles2d, self.revenue2d, 
                                           ibids, targetBid, self.samples2d, True)
        
        print ibids
        
    def test_condLocal(self):
        ibids = [25.,25.]
        print ibids
        newBids,converged,itr,l = condLocal(self.bundles2d, self.revenue2d, ibids, 
                                            self.samples2d, 100, 0.001, True)
        
        print newBids
        print converged
        print itr
        print l
        
#    def test_plotCondLocal(self):
#        ibids = [25.,25.]
#        
#        plotCondLocal(self.bundles2d, self.revenue2d, ibids, 
#                      self.samples2d, 100, 0.001, True)
        
    def test_ericCounterExample(self):
        """
        From Eric Sodomka's counter example of suboptimality.
        Sould converte to [25,25]
        """
        m = 2
        v = [0,50]
        l = 2
        bundles = listBundles(m)
        revenue = msListRevenue(bundles, v, l)
        initialBids = numpy.asarray([25.,25.],dtype = 'float')
        targetBid = 0
        nSamples = 300
        samples = numpy.zeros((nSamples,m))
        samples[:100,:] = [30,10]
        samples[100:200,:] = [10,30]
        samples[200:300,:] = [10,10]
        
        b1 = condLocalUpdate(bundles, revenue, initialBids, targetBid, samples, True)
        
        decimal = 5
        
        numpy.testing.assert_almost_equal(b1, 25, decimal, "condLocal - test_ericCounterExample Failed")
        
        
        ret = condLocal(bundles,revenue, initialBids, samples, verbose = True)
        
        numpy.testing.assert_almost_equal(ret[0],numpy.asarray([25.,25.]),decimal)
        
        numpy.testing.assert_equal(ret[1], True, "condLocal - test_ericCounterExample Failed" )
        
        
        
        
    
if __name__ == "__main__":
    unittest.main()