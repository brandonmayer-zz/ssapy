import numpy
#from scipy.sparse import dok_matrix

import matplotlib.pyplot as plt

#import os
#import copy

isnumber = lambda n: isinstance(n, (int, float, long, complex))

machine_precision = numpy.finfo(numpy.double).eps

class dokHist(object):
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
                    
        self.type = kwargs.get(type, 'discrete')
        
        self.isdensity = kwargs.get('isdensity',False)
        
        self.c = {}
        
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
    
    def center_from_range(self,r):
        """
        The range should be a list of tuples (each with 2 entries) or a single
        tuple (2 entries).
        
        For discrete entries: t[0] == t[1] -> just use the value of the discrete
        entry as the center. (just by convention)
        """
        if isinstance(r,tuple) and len(r) == 2:
            return r[0] + 0.5*numpy.diff(r)
        
        elif isinstance(r,list) and len(r) == self.dim():
            center = numpy.zeros(len(r))
            for idx, t in enumerate(r):
                if t[0] == t[1]:
                    center[idx] = t[0]
                elif t[1] > t[0]:
                    center[idx] = t[0] + 0.5*(t[1] - t[0])
                else:
                    raise ValueError("Could Not Compute Center of {0}".format(t))
                
            return center
        else:
            raise ValueError("Unknown range format {0}".format(r))
            
                
                
    def key_from_val(self,val):
        return tuple(self.range_from_val(numpy.atleast_1d(val)))
     
    def bin_centers(self):
        bin_centers = []
        for bin_list in self.bins:
            bin_centers.append(bin_list[0:-1] + numpy.diff(bin_list)/2.0)
        return bin_centers
    
    def upcount(self, val, mag = 1.0):
        k = self.key_from_val(val)
        
        try:
            self.c[k] += mag
        except KeyError:
            self.c[k] = mag
            
        self.counts_accum += mag
        
    def set(self, val, mag):
        if not isinstance(mag,int) and self.isdensity == False:
            s = "Histogram is not a density. Must provide " +\
                "an interger count to set(...)"
            raise ValueError(s)
        
        k = self.key_from_val(val)
        
        self.c[k] = mag
    
    def counts(self, val):
        k = self.key_from_val(val)
        
        c = self.c.get(k)
        
        if c == None:
            return 0
        else:
            return c
                                    
    def eval(self, val):
        """
        Backwards compatible wrapper around dokHist.density()
        """
        return self.density(val)
        
    def density(self, val):
        r = self.range_from_val(val)
        k = tuple(r)
        
        c = self.c.get(k)
        
        if c == None or c == 0.0:
            return 0.0
        elif self.isdensity:
            return numpy.float(c)
        else:
            dif = numpy.diff(r)
            dif[dif==0]=1
            volume = numpy.prod(dif) 
            return numpy.float(c) / numpy.float(self.counts_accum*volume)
        
    def counts_sum(self):
        """
        If the histogram is not a density, return the sum of all counts.
        """
        if self.isdensity:
            raise ValueError("Cannot Compute Sum of counts for density")
        
        z = 0.0
        for counts in self.c.itervalues():
            z += counts
            
        self.counts_accum = z
        
        return z
    
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
                        
    def marginal(self, target_dim):
        """
        Comput marginal distribution of given dimension.
        
        target_dim is zero indexed.
        """
        marg = dokHist(m=1)
        
        marg.isnormed = True
        
        marg.bins = [self.bins[target_dim]]
        
        for r in self.c.keys():
            center = self.center_from_range(list(r))
            target_center = center[target_dim]
            marg.upcount(target_center,self.density(center))
        
        return marg
        
    def show(self, filename = '', density = True):
        if self.dim() == 1:
            bin_centers = self.bin_centers()[0]
            
            y = []
            for bc in bin_centers:
                if density:
                    y.append(self.density(bc))
                else:
                    y.append(self.counts(bc))
                    
            plt.bar(bin_centers,y, align='center')
            
            if filename == '':
                plt.show()
            else:
                plt.savefig(filename)
        else:
            raise NotImplementedError("NOT IMPLEMENTED")
                    
            
        
def marginal_expected_cost( hob_hist, bid):
    if hob_hist.dim() != 1:
        err_str = "Must provide marginal histogram," +\
                  "hob_hist.dim() = {0} != 1".format(hob_hist.dim())
        raise ValueError(err_str)
    if isnumber(bid):
        pass
    elif len(bid) != 1:
        raise ValueError("len(bid) = {0} ! = 1".format(len(bid)))
    
    ec = 0.0
    
    for r in hob_hist.c.keys():
        r = r[0]
         
        if r[0] < bid and r[1] <= bid:
            scale = 0.5*(r[1]**2 - r[0]**2)
            ec += hob_hist.density(r[1])*scale
        elif bid > r[0] and bid < r[1]:
            scale = 0.5*(bid**2 - r[0]**2)
            ec += hob_hist.density(r[1])*scale
            
    return ec
        
           
        
def expected_cost( hob_hist, bids ):
    """
    inputs:
        highest other agent bid histogram
        bid vector
    outputs:
        expected cost given bid
    """
    if isnumber(bids):
        bidv = numpy.asarray([bids])
    else:
        bidv = numpy.asarray(bids)
        
    if not bidv.shape[0] == hob_hist.dim():
        raise ValueError("hob_hist.dim() = {0} != bids.shape[0] = {1}".\
                         format(hob_hist.dim(), bidv.shape[0]))
        
    ec = 0.0
    for d, bid in enumerate(bidv):
        marg = hob_hist.marginal(d)
        ec += marginal_expected_cost(marg, bid)
        
    return ec

def expected_utility( hob_hist, bundles, valuations, bids):
    pass
    ev = 0.0
    for bundle, value in zip(bundles, valuations):
        ev += value*prob_win_given_bid(hob_hist, bundle, bids)
        
    ec = expected_cost(hob_hist, bids)
    
    return ev - ec
    
def prob_win_given_bid( hob_hist, bundle, bids):
    if not isinstance(hob_hist, dokHist):
        raise ValueError("Must provide dokHist instance.")
    
    bid_view = numpy.atleast_1d(bids)
    bundle_view = numpy.atleast_1d(bundle)
    
    if not (bid_view.shape[0] == bundle_view.shape[0]) \
         and not(bid_view.shape[0] == hob_hist.dim()):
        msg = "Dimension Mismatch:\n" +\
              "bid.shape[0] = {0}, bundle.shape[0] = {1}, hob_hist.dim() = {2}"\
            .format(bid_view.shape[0], bundle_view.shape[0], hob_hist.dim())
        raise ValueError(msg)
    
    
    pwin = 0.0
    for bin_range in hob_hist.c.keys():
        include = True
        
        if hob_hist.dim() == 1:
            bin_range = bin_range[0]
        
        volume = 1.0
        for good_idx, good in enumerate(bundle_view):
            if good and (bid_view[good_idx] < bin_range[good_idx][0]):
                #if you would loose the good but the target
                #bundle included the good
                include = False   
            elif not good and (bid_view[good_idx] > bin_range[good_idx][1]):
                #if you would win the good but it isn't included
                #in the bundle
                include = False
                
            if include == False:
                break
            else:
                if bin_range[good_idx][0] == bin_range[good_idx][1]:
                    pass
                else:
                    if good:
                        volume*=(numpy.min([bid_view[good_idx],bin_range[good_idx][1]]) - bin_range[good_idx][0])
                    else:
                        volume*=(bin_range[good_idx][1] - numpy.max([bid_view[good_idx], bin_range[good_idx][0]]))
            
        if include:
            centers = hob_hist.center_from_range(list(bin_range))
            density = hob_hist.density(centers)                
            pwin += density*volume
                    
    return pwin
                            
def main():
    h = dokHist(m=2, isdensity = True)
    h.set([2.5,2.5],.25)
    h.set([5.5,1.5],.75)
    
    


if __name__ == "__main__":
    main()
    
        