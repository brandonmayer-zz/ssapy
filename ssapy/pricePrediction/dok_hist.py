import numpy
from scipy.sparse import dok_matrix

import os

isnumber = lambda n: isinstance(n, (int, float, long, complex))

class dok_hist(object):
    """
    A dictionary of keys sparse histogram.
    
    Binning Convention (for compatability with Wellman):
        [0], (0,1], (1,2], ...
        
    [0] gets its own bin
    
    for all others:
    val belongs to bin i implies:
    bin[i] < val < bin[i+1]
    
    all other bins follow the lower exclusive upper inclusive pattern.
    """
    def __init__(self, **kwargs):
        extent = kwargs.get('extent')
        
        if extent == None:
            m = kwargs.get('m')
            if m == None:
                raise ValueError("Must specify number of dimentions - m")
            self.bins = numpy.asarray([numpy.concatenate(([0], numpy.arange(0,51,1)))\
                                       for i in xrange(m)])
            
        self.counts = {}
        
    def extent(self):
        return [(bins[0], bins[1]) for bins in self.bins]
    
    def dim(self):
        return self.bins.shape[0]
    
    def range_from_val(self, val):
        key = self.key_from_val(val)
        return self.range_from_key(key)
                
    def range_from_key(self,key):
        r = []
        for i, k in enumerate(key):
            r.append((self.bins[i,k-1],self.bins[i,k]))
        
        return r
        
    def key_from_val(self, val):
        
        if isnumber(val):
            aval = numpy.asarray([val])
        else:
            aval = numpy.asarray(val)
            
        if not aval.shape[0] == self.bins.shape[0]:
            raise ValueError("val.shape[0] = {0} != bins.shape[0] = {1}".\
                             format(aval.shape[0], self.bins.shape[0]))
            
        ret = numpy.zeros(aval.shape, dtype=numpy.int)
        
        if numpy.all(aval == 0):
            return ret
            
        for i in xrange(aval.shape[0]):
            if aval[i] < self.bins[i][0] or aval[i] > self.bins[i][-1]:
                raise ValueError("{0} out of range".format(aval))
            
            greater_bins = int(numpy.nonzero( aval[i] <= self.bins[i])[0][0])
            
            #the first bin greater than the value
            ret[i] = greater_bins
            
        return ret
            
    
    def upcount(self, val, mag = 1.0):
        key = self.key_from_val(numpy.asarray(val))
        
        key = tuple(key) 
        
        if not key in self.counts.keys():
            self.counts[key] = mag
        else:
            self.counts[key] += mag    
    
def main():
    hist = dok_hist(m=1)
    k  = hist.key_from_val(4)
    print k
    r = hist.range_from_val(4)
    print r
    
    print hist.range_from_val(4.5)
    print hist.range_from_val(50)
    pass
#    hist.upcount([1,2],5)
#    print'{0}'.format(hist.range_from_val([1,2]))
#    pass
#    pass

if __name__ == "__main__":
    main()
    
        