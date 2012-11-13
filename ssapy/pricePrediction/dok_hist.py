import numpy
from scipy.sparse import dok_matrix

import os

isnumber = lambda n: isinstance(n, (int, float, long, complex))

machine_precision = numpy.finfo(numpy.double).eps

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
    
    This TERRIBLE convention was not my choice! It is to maintain
    compatability with Dr. Wellman's code.
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
                    
        self.type = kwargs.get(type, 'discrete')
        
        
        self.c = {}
        
        self.isnormed = False
        
        self.counts_accum = 0.0
        
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
                
    def key_from_val(self,val):
        return tuple(self.range_from_val(numpy.atleast_1d(val)))
     
    def upcount(self, val, mag = 1.0):
        k = self.key_from_val(val)
        
        try:
            self.c[k] += mag
        except KeyError:
            self.c[k] = mag
            
        self.counts_accum += mag
        
    def norm_constant(self, type = 'discrete'):
        """
        Compute and return the normalization constant
        given the current state of the histogram.
        
        type can be either 'discrete' or 'density'
        
        type = 'discrete' 
        Implies we are approximating the true
        distribution with point masses at the center of each bin. 
        The normalization constant is then just the sum of all counts
        for all bins.
        
        type = 'density' 
        Assume each bin is uniformly distributed over its interval. 
        The normalization constant is then the the counts assocaited with the interval
        multiplied by the area of the bin. 
        """
        z = 0.0
        
        if type == 'discrete':
            for counts in self.c.values():
                z += counts
                
        if type == 'density':
            for intervals, counts in self.c.iteritems():
                a = 1.0
                for interval in intervals:
                    a*=(interval[1] - interval[0]) 
                z += counts
                
        return z
                
    def normalize(self, type = 'discrete'):
        """
        Normalize the counts, return normalization constant.
        """
        
        z = self.norm_constant(type)
        for key in self.c.keys():
            self.c[key]/=z
            
        self.isnormed = True
        
        return z
            
    def eval(self, val):
        k = self.key_from_val(val)
        
        c = self.c.get(k)
        
        if c == None:
            return 0
        else:
            return c / self.counts_accum
        
        
    def counts(self, val):
        k = self.key_from_val(val)
        
        c = self.c.get(k)
        
        if c == None:
            return 0
        else:
            return c
        
    def sample(self, n_samples = 1):
        dim = self.dim()
        keys = self.c.keys()
        counts = self.c.values()
        p = counts/numpy.sum(counts,dtype=numpy.float)
        
        #1. sample ranges
        range_samples = []
        for i in xrange(n_samples):
            range_samples.append(keys[numpy.random.multinomial(1,p).argmax()])
            
        #2. sample uniformly from ranges
        samples = []
        for r in range_samples:
            if dim == 1:
                if r[0][0] == r[0][1]:
                    sample = r[0][0]
                else:
                    # because we used obscene convention (x,y] and samplers
                    # use the correct convention [x,y), add the machine precision to 
                    # get desired functionality
                    sample = r[0][0] + machine_precision + numpy.random.uniform()
            else:
                sample = numpy.zeros(dim)
                for dim_idx in xrange(len(r)):
                    if r[dim_idx][0] == r[dim_idx][1]:
                        sample[dim_idx] = r[dim_idx][0]
                    else:
                        sample[dim_idx] = r[dim_idx][0] + machine_precision + numpy.random.uniform()
                
            samples.append(sample)
            
        return samples
    
    def expected_cost(self, bid):
        """
        Compute the expected cost given a vector of bids.
        Approximating \int_{q=0}^bqp(q)dq.
        """
        dim = self.dim()
        
        if self.isnormed:
            raise NotImplementedError
        else:
            ec = numpy.zeros(dim)
            for bin_range, counts in self.c:
                bin_valid = True
                for d in xrange(dim):
                    if bid[d] < bin_range[d][1]:
                        bin_valid = False
                        
    def bin_centers(self):
        bin_centers = []
        for bin_list in self.bins:
            bin_centers.append(bin_list[0:-1] + numpy.diff(bin_list)/2.0)
        return bin_centers
    
    def marginal(self, target_dim):
        bin_centers = self.bin_centers()
        
        target_bin_centers = bin_centers[target_dim]
        marg = {}
        for target_bin_center in target_bin_centers:
            
        
     
                        
                    
                    
                     
 

    
    
def main():
    import matplotlib.pyplot as plt
        
    hist = dok_hist(m=1)
    for i in xrange(1,51):
        hist.upcount(i, 1.0)
        
    print 'counts = {0}'.format(hist.c)
    
    samples = hist.sample(100)

    h,b = numpy.histogram(samples, bins = range(0,51))
    plt.bar(b[0:-1],h)
    plt.show()
        
    print 'samples = {0}'.format(samples)


if __name__ == "__main__":
    main()
    
        