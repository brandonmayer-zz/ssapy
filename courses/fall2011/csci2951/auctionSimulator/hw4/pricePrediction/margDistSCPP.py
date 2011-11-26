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
    def __init__(self, marginalDistributionPrediction = None):
        """
        marginalDistributionPrediction should be a list of size m of tuples
        each tuple specifies a normalized histogram count and bin edges
        """          
        # initialize as empty
        if marginalDistributionPrediction == None:
            self.data = None
            self.m = None
        else:
            if self.validateData(marginalDistributionPrediction):
                self.data = marginalDistributionPrediction
                if isinstance(marginalDistributionPrediction,list):
                    self.m = len(marginalDistributionPrediction)
                else:
                    self.m = 1
    
    @staticmethod
    def type():
        return "marginalDistributionSCPP"
        
    def setPricePrediction(margDistData):
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
                    msg = "Marginal Distribution Data must be a valid PDF." )
                
        elif isinstance(margDistData,tuple):
            numpy.teseting.assert_almost_equal(
                    numpy.sum( margDistData[0]*numpy.diff(margDistData[0]),dtype=numpy.float),
                    numpy.float(1.0),
                    msg = "Marginal Distribution Data must be a valid PDF." ) 
                                               
        # if you made it here you are good to go
        return True
        
    
                