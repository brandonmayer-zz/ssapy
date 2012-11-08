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
        else:
            raise NotImplemented("Not Yet!")
            
        self.counts = {}
        
        self.isnormed = False
        
        self.accum = 0.
        
    def extent(self):
        return [(bins[0], bins[1]) for bins in self.bins]
    
    def dim(self):
        return self.bins.shape[0]
    
    def range_from_val(self, val):
        
        aval = numpy.atleast_1d(val)
        
        if not aval.shape[0] == self.bins.shape[0]:
            raise ValueError("val.shape[0] = {0} != bins.shape[0] = {1}".\
                             format(aval.shape[0], self.bins.shape[0]))
            
        r = []
        for i, v in enumerate(aval):
            if v < self.bins[i][0] or v > self.bins[i][-1]:
                raise ValueError("{0} out of range".format(v))
            
            greater_bins = v <= self.bins[i]
            lower_bin_index = greater_bins[0]
            upper_bin_index = greater_bins[1]
            r.append(tuple(lower_bin_index, upper_bin_index))
        
        return r     
        
                
    def range_from_key(self,key):
        r = []
        for i, k in enumerate(key):
            if k == 0:
                r.append((0,0))
            else:
                r.append((self.bins[i,k-1],self.bins[i,k]))
        
        return r
    
    def bin_center_from_key(self,key):
        r = numpy.atleast_2d(self.range_from_key(key))
        bin_center = r[:,0] + (numpy.diff(r).flatten())*.5
        return bin_center 
        
    def key_from_val(self, val):
        
        aval = numpy.atleast_1d(val)
            
        if not aval.shape[0] == self.bins.shape[0]:
            pass
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
            
    def delta_from_val(self, val):
        """
        return the area of the bin in which the value falls
        """
        ranges = self.range_from_val(val)
        
        return numpy.diff(ranges).flatten()
    
    def bin_areal_from_val(self,val):
        return numpy.prod(self.delta_from_val(val))
            
        
    def upcount(self, val, mag = 1.0):
        key = self.key_from_val(numpy.atleast_1d(val))
        
        key = tuple(key) 
        
        if not key in self.counts.keys():
            self.counts[key] = mag
        else:
            self.counts[key] += mag    
            
        self.isnormed = False
        
        self.accum += (mag*self.bin_areal_from_val(val))
        
    def recompute_norm(self):
        self.accum = 0.0
        
        for val in self.counts.values():
            self.accum += val*self.bin_areal_from_val(val)
        
        self.isnormed = False
            
        return self.accum
    
    def norm_const(self):
        """
        Return the normalization constant
        """
        return self.accum
    
    def normalize(self,recompute_norm = False):
        """
        Normalize the distribution and 
        return the normalization constant
        """
        if recompute_norm:
            self.recompute_norm()
            
        for val in self.counts.values():
            val/=self.accum
            
        self.isnormed = True
    
        return self.accum
    
    def eval(self, val, norm = True, recompute_norm = False):
        
        key = tuple(self.key_from_val(numpy.asarray(val)))
        
        if not key in self.counts.keys():
            return 0.
        
        if recompute_norm:
            self.recompute_norm()
        
        if norm and not self.isnormed:    
            return self.counts[key]/self.accum
        else:
            return self.counts[key]
        
    def sample(self, n_samples = 1, recompute_norm = False):
        p = numpy.zeros(len(self.counts.keys()))
        
        if recompute_norm:
            self.recompute_norm()
            
        if self.isnormed:
            for i, v in enumerate(self.counts.values()):
                p[i] = v
        else:
            for i, k in enumerate(self.counts.key()):
                pass
                
            
            
        
        
        
        
def main():
    hist = dok_hist(m=2)
    r = hist.range_from_val([0,0])
    hist.upcount([30,30],6)
    hist.upcount([20,30],10)
    samples = hist.sample(5)
    pass
    
        
#    hist = dok_hist(m=1)
        
#    hist.upcount(4.5,3)
#    hist.upcount(50,10)
#    hist.upcount(10,4)
    

#    print hist.pmf(4)
#    print hist.pmf(4.1)
#    print hist.pmf(10)
#    print hist.pmf(50)
    


if __name__ == "__main__":
    main()
    
        