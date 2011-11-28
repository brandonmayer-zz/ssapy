from pointSCPP import *

from types import * #for type checking

class margDistSCPP(pointSCPP):
    """
    Wrapper for marinal distribution self confirming price predictions.
    
     There should be one tuple per good, that is
        len(self.data) == self.m
        NOTE:
            If bins are [1,2,3,4] then the first bin
            contains all values within the range [1,2)
            (including 1 excluding 2), [2,3) and 
            [3,4] notice the last bin edge is inclusive
    
    savePickle and loadPickle are inherited from the pointSCPP class
    """
    def __init__(self, margDistData = None):
        """
        marginalDistributionPrediction should be a list of size m of tuples
        each tuple specifies a normalized histogram count and bin edges
        """          
        # initialize as empty
        if margDistData == None:
            self.data = None
            self.m = None
        else:
            if self.validateData(margDistData=margDistData):
                self.data = margDistData
                if isinstance(margDistData,list):
                    self.m = len(margDistData)
                else:
                    self.m = 1
    
    @staticmethod
    def type():
        return "marginalDistributionSCPP"
    
    
    def expectedPrices(self):
        """
        Calculate the expected price vector using the center bin avg method
        """
        e = []
        for hist, binEdges in self.data:
            e.append(self.centerBinAvg(hist,binEdges))
            
        return numpy.atleast_1d(e)
    
    @staticmethod
    def centerBinAvg(hist = None, binEdges = None):
        """
        A helper function for computing averages with a histogram
        take the value of a histogram bin to be equal to its center than 
        calculate the average as avg = \sum_i^n binCenter*prob(binCenter)
        
        Note:
            The histograms must be properly normalized.
        """
        
        assert isinstance(hist,numpy.ndarray) or isinstance(binEdges,numpy.ndarray),\
            "hist and binEdges must be of type numpy.ndarray"
            
        numpy.testing.assert_almost_equal( numpy.sum(hist*numpy.diff(binEdges),dtype=numpy.float), 
                                           numpy.float(1.0) )
        
        numpy.testing.assert_equal( binEdges.shape[0], (hist.shape[0]+1) )
    
        return numpy.dot(hist, .5*binEdges[:-1]+binEdges[1:])
        
    def setPricePrediction(self, margDistData):
        if self.validateData(margDistData):
            self.data = margDistData
            
            if isinstance(margDistData,list):
                self.m = len(margDistData)
            else:
                self.m = 1
                
    @staticmethod
    def validateData(margDistData = None):
        assert isinstance(margDistData, list) or\
                isinstance(margDistData, tuple),\
                "{1} is not a list or tuple".format(margDistData)
        
        if isinstance(margDistData,list):
                      
            for hist,binEdges in margDistData:
                assert isinstance(hist,numpy.ndarray) and\
                        isinstance(binEdges,numpy.ndarray),\
                            "hist and binEdges must be numpy arrays."               
            
                numpy.testing.assert_almost_equal( 
                    numpy.sum(hist*numpy.diff(binEdges),dtype=numpy.float), 
                    numpy.float(1.0),
                    err_msg = "Marginal Distribution Data must be a valid PDF." )
                
        elif isinstance(margDistData,tuple):
            numpy.testing.assert_almost_equal(
                    numpy.sum( margDistData[0]*numpy.diff(margDistData[1]),dtype=numpy.float),
                    numpy.float(1.0),
                    err_msg = "Marginal Distribution Data must be a valid PDF." ) 
                                               
        # if you made it here you are good to go
        return True
    
    
        
    
                