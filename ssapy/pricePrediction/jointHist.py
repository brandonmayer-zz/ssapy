import numpy

class jointHist(object):
    def __init__(self,**kwargs):
        
        #a list of (min,max,step) for bins 1 per dimension
        #default will be 0:1:50 on all dimensions
        extent = kwargs.get('extent')
        if extent == None:
            m = kwargs.get('m')
            if m == None:
                raise ValueError("Must specify number of dimentions - m")
            self.bins = []
            for i in xrange(m):
                self.bins.append(numpy.arange(0,51,1))
            
        dims = []
        for i in xrange(m):
            dims.append(self.bins[i].shape[0]-1)
        
        self.counts = numpy.zeros(dims)
    
    def extent(self):
        ext = []
        for bins in self.bins:
            ext.append((bins[0],bins[-1]))
            
        return ext
        
    def dim(self):
        return self.counts.shape
    

    
    def bin_at_val(self, values):
        """
        Return the indicies in the self.counts matrix
        corresponding to the array val
        """
        values = numpy.atleast_2d(values)
        
        if not values.shape[1] == len(self.bins):
            raise ValueError("val.shape = {0} != len(self.bins) = {1}".\
                             format(values.shape[0],len(self.bins)))
            
        binArray = numpy.zeros(values.shape)
        
        for i, valueArray in enumerate(values):
            for j, value in enumerate(valueArray):

                if value < self.bins[j][0]:
                    raise ValueError("values[{0},{1}] = {2} < self.bins[{0},0] = {3}".\
                                     format(i, j, value, self.bins[j][0]))
                elif value > self.bins[j][-1]:
                    raise ValueError("values[{0},{1}] = {2}  > self.bins[{0},-1] = {3}".\
                                     format(i, j, value, self.bins[j][-1]))
                
            lowerBound = numpy.nonzero(self.bins[j] < value)[0]
            if len(lowerBound) == 0:
                binArray[i,j] = 0
            else:
                #greatest lower bound
                binArray[i,j] = lowerBound[-1]
                
        if binArray.shape[0] == 1:
            return binArray[0]
        else:
            return binArray   
            
        
#    def upcount(self, val, mag=1.0):
#        pass
            
                
if __name__ == "__main__":
    h = jointHist(m=2)
    print 'h.bins   = {0}'.format(h.bins)
    print 'h.counts = {0}'.format(h.counts)
    pass