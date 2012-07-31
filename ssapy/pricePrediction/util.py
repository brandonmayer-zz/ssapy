import numpy
#from aucSim.pricePrediction.margDistSCPP import * 
from ssapy.pricePrediction.margDistSCPP import margDistSCPP

def ksStat(margDist1 = None, margDist2 = None):
    """
    A helper function for computing the maximum Kolmogorov-Smirnov (KS)
    statistic over marginal price distributions
    
    KS(F,F') = max_x |F(x) - F'(x)|
    
    Yoon & Wellman 2011 take the maximum over each of the KS 
    statistics seperately for each good:
    KS_marg = max_j KS(F_j,F'_j)
    """
    
    assert isinstance(margDist1, margDistSCPP) and\
            isinstance(margDist2, margDistSCPP),\
        "margDist1 and margDist2 must be instances of margDistSCPP"
        
    #use numpy assertions b/c they can't be turned off at 
    #compile time
    numpy.testing.assert_equal(margDist1.m, 
                               margDist2.m)
       
    margKs = []
    for idx in xrange(margDist1.m):
        
        # test that the distributions are over the same bin indices
        # if they are not this calculation is meaninless
        numpy.testing.assert_equal(margDist1.data[idx][1],
                                   margDist2.data[idx][1])
        
        # cumulative sum of first distribution
        cs1 = numpy.cumsum(margDist1.data[idx][0])
        
        # cumulative sum of second distribution
        cs2 = numpy.cumsum(margDist2.data[idx][0])
        
        # record the maximum absoute difference between the 
        # cumulative sum over price probabilities
        margKs.append(numpy.max(numpy.abs(cs1-cs2)))
    
    # return the max over goods of the max absolute difference between
    # the cumulative sum over price probabilities
    return numpy.max(numpy.atleast_1d(margKs)) 

def klDiv(margDist1, margDist2):
    assert isinstance(margDist1, margDistSCPP) and\
            isinstance(margDist2, margDistSCPP),\
        "margDist1 and margDist2 must be instances of margDistSCPP"
        
    numpy.testing.assert_equal(margDist1.m, 
                               margDist2.m)
    
    kldSum = 0.0
    for idx in xrange(margDist1.m):
        # test that the distributions are over the same bin indices
        # if they are not this calculation is meaninless
        numpy.testing.assert_equal(margDist1.data[idx][1],
                                   margDist2.data[idx][1])
        
        #test that the distributions have the same number of bins
        numpy.testing.assert_equal(len(margDist1.data[idx][0]),
                                   len(margDist2.data[idx][0]))
        
        m1 = margDist1.data[idx][0]
        m1[m1==0] = numpy.spacing(1)
        m2 = margDist2.data[idx][0]
        m2[m2==0] = numpy.spacing(1)
        
             
        kldSum += numpy.sum(margDist1.data[idx][0] * (numpy.log(margDist1.data[idx][0]) 
                                               - numpy.log(margDist2.data[idx][0])))

        
    return kldSum