from pointSCPP import *

class marginalDistributionSCPP(pointSCPP):
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
        self.data = marginalDistributionPrediction
        self.m = len(marginalDistributionPrediction)
        
    def setPricePrediction(pricePrediction):
        if self.validateMarginalDistribution(pricePrediction):
            self.data = pricePrediction
            self.m = len(pricePrediction)
        
    @staticmethod
    def type():
        return "marginalDistributionSCPP"
    
    @staticmethod
    def validateMarginalDistribution(marginalDistribution,tol = 0.00001):
        if not isinstance(marginalDistribution,list):
            print "----Warning----"
            print "marginalDistributionSCPP.validateMarginalDistribution"
            print "input is not a list."
            return False
        
        for idx in marginalDistribution:
            
            if not isinstance(marginalDistribution,tuple):    
                print "----Warning----"
                print "marginalDistributionSCPP.validateMarginalDistribution"
                print "marginal distribution entry is not a tuple."
                return False
            
            hist,binEdges = marginalDistribution[idx]
            
            if not numpy.abs( numpy.sum( hist*numpy.diff(binEdges),dtype=numpy.float ) 
                              - numpy.float(1.0) ) <= tol:
                print "----Warning----"
                print "marginalDistributionSCPP.validateMarginalDistribution"
                print "invalid PDF."
                return False
            
        return True
        
    
                