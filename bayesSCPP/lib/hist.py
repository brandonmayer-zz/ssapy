import numpy

class hist(object):
    def __init__(self, minVal = 0, maxVal = 50, dim = 1, delta = 1 ):
        self.dim = dim
        self.minVal = minVal
        self.maxVal = maxVal
        self.delta  = delta
        
    def binFromVal(self,val):
          