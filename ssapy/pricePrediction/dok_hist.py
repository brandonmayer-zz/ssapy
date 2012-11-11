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
#            self.bins = numpy.asarray([numpy.concatenate(([0], numpy.arange(0,51,1)))\
#                                       for i in xrange(m)])
            
            self.bins = []
            for i in xrange(m):
                self.bins.append([0])
                for j in xrange(0,51):
                    self.bins[i].append(j)
                    
        self.c = {}
        
    def extent(self):
        return [(bins[0], bins[-1]) for bins in self.bins]
    
    def dim(self):
        return len(self.bins)
    
    def range_from_val(self, val):
        """
        Search for the range of the bins corresponding to val
        in each dimension using a binary search.
        """
        aval = numpy.atleast_1d(val)
        
        if(aval.shape[0] != self.dim()):
            raise ValueError("val.shape[0] = {0} != self.dim() = {1}".\
                             format(aval.shape[0], self.dim()))
            
        r = []
        
        #loop over all dimensions
        for dim_idx, bin_list in enumerate(self.bins):
            
            v = aval[dim_idx]
            
            #bounds check
            if v < bin_list[0]:
                raise ValueError("v = {0} < bin_list[0][0] = {1}".format(v, bin_list[0][0]))
            
            if v > bin_list[-1]:
                raise ValueError("v = {0} > bin_list[-1][1] = {1}".format(v, bin_list[-1][0]))
            
            first = 0
            last  = len(bin_list)
            while True:
                
                mid = first + int((last-first)/2)
                
                if first >= last:
                    raise ValueError("No bin found for v = {0} in\nbins = {1}".format(v, bin_list))
                
                if bin_list[mid] < v and v <= bin_list[mid+1]:
                    break
                elif (bin_list[mid] == bin_list[mid+1]) and v == bin_list[mid]:
                    #This condition allows for bins of 0 width;
                    #counting exact values instead of ranges.
                    break
                else:
                    if v > bin_list[mid]:
                        first = mid
                    else:
                        last = mid  
                               
            r.append( (bin_list[mid], bin_list[mid+1]) )
            
        return r
                 
    def upcount(self, val, mag = 1.0):
        r = tuple(self.range_from_val(numpy.atleast_1d(val)))
        
        try:
            self.c[r] += mag
        except KeyError:
            self.c[r] = mag
                
    def counts(self, val):
        r = tuple(self.range_from_val(numpy.atleast_1d(val)))
        
        c = self.c.get(r)
        
        if c == None:
            return 0
        else:
            return c
        
    
def main():
    hist = dok_hist(m=1)
#    key = hist.key_from_val(0)
    val = 25
    r = hist.range_from_val(val) 
    print 'r = {0}'.format(r)

if __name__ == "__main__":
    main()
    
        