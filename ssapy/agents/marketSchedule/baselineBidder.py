import numpy
from . import msAgent

class baselineBidder(msAgent):
    """
    Bids for goods < \lambda_i at price v_i^(\lambda_i)/\lambda_i
    """
    def __init__(self, **kwargs):
        super(baselineBidder, self).__init__(**kwargs)
        
    def bid(self, **kwargs):
        
        bids = numpy.zeros(self.m)
        
        for i in xrange(self.m):
            if i < self.l:
                bids[i] = float(self.v[self.l-1]/self.l)
                
        return bids
            
        
    