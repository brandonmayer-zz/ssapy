import numpy
import itertools
from ssapy.util.padnums import pprint_table
import sys

def listBundles(m = 5):
    """
    Return a numpy 2d array of all possible bundles that the agent can
        bid on given the number of auctions.
        
    The Rows represent the bundle index.
        
    The Columns Represent the good index.        
        
    Return bundles as booleans for storage and computational efficiency
    
    Inputs
    ------
        m        := (int) number of goods.
    
    Returns
    -------
        bundles  := (2d numpy array dtype = bool)
    """
    return numpy.atleast_2d([b for b in itertools.product([False,True],repeat=m)]).astype(bool)

def bundle2idx(bundle = None):
        numpy.testing.assert_(bundle.dtype == bool,
                              msg="bundle.dtype = {0} != bool".format(bundle.dtype))
        idx = 0
        for i in xrange(bundle.shape[0]):
            idx = (2**((bundle.shape[0]-1)-i))*bundle[i]
            
        return idx
    
def idx2bundle(index=None, nGoods = 5):
    """Convert to decimal rather than enumerating power set
       and selecting correct bundle
    """
    
    assert index != None and nGoods != None,\
        "simYW::bundleFromIndex must specify all arguments."
        
    assert isinstance(index,int) and index >= 0,\
        "simYW::bundleFromIndex index must be a positive integer."
        
    assert isinstance(nGoods,int) and nGoods >0,\
        "simYw::bundleFromIndex nGoods must be a strictly positive integer."
    
    binList = []
    n = index
    while n > 0:
        binList.insert(0,n%2)
        n = n >> 1
        
    # just checking the index wasn't
    # past the maximum bundle
    if len(binList) > nGoods: raise ValueError, "simYW::bundleFromIndex Error: Dec-Binary Conversion"
    
    for i in xrange(nGoods-len(binList)):
        binList.insert(0,0)
        
    return numpy.atleast_1d(binList)

def cost(bundles, price):
    """Compute the price of a list of bundles given closing prices of each good
    
    Inputs
    ------
    bundles: array_like, shape (n_bundles, n_goods)
        List of collection of goods. Each row is collection, each column a good index.
        A 1 in the i^{th} row and j^{th} column implies the good j is contained in the 
        i^{th} listed bundle.
        
    price: array_like, shape (n_goods)
        A list of closing prices, one for each 
        possible good (e.g. price.shape[0] == bundles.shape[1])
    
    Returns
    -------
    cost: array_list, shape (n_bundles)
        A 1d array such that cost[i] is the price of aquiring 
        the collection of goods indicated by bundles[i]
    """
    bundles = numpy.atleast_2d(bundles)
    
    price = numpy.atleast_1d(price).astype(numpy.float)
    
    if (price == float('inf')).any():
        # if there are items which are unobtainable (cost = inf)
        # then the cost for the bundles containing that good should
        # be inf but the bundles not containing those goods should be the 
        # cost of other goods
        
        # lists are mutable, deep copy the original price vector
        # in order to preserve the argument
        unobtainableGoods = numpy.nonzero(price == float('inf'))[0]
        # make a deep copy so not to mutate func. argument
        priceInfZero = numpy.atleast_1d(numpy.array(price))
        priceInfZero[unobtainableGoods] = 0
        
        cost = []
        for idx in xrange(bundles.shape[0]):
            if (bundles[idx][unobtainableGoods] == 0).all():
                cost.append(numpy.dot(bundles[idx],priceInfZero))
            else:
                cost.append(float('inf'))
                
        return numpy.atleast_1d(cost)
    else:
        return numpy.atleast_1d([numpy.dot(bundle,price) for bundle in bundles])
    
def surplus(bundles, valuation, priceVector):
        """
        Calculate the surplus for a given array of bundles, prices and a valuation (scalar).
        Surplus equals valuation less cost.
        
        INPUTS
        ------
            bundles       :=     (2d array-like)
                                 rows indicate individual bundles
                                 columns are individual goods
                                 
            valuation     :=     (1d array-like)
                                 an numpy array of valuations, one for each bundle
                                 
            priceVector   :=     (1d array-like) 
                                 A point price prediction. Each element corresponds to a good 
                                 priceVector.shape[0] == bundles.shape[1] == number of goods
                                 
        Returns
        -------
            surplus       :=     (1d array-like)
                                 List of surplus 1:1 correspondence with bundles.
                                 surplus = revenue - cost
        """
                   
        bundles = numpy.atleast_2d(bundles)
        
        valuation = numpy.atleast_1d(valuation)
        
        return valuation - cost(bundles = bundles, price = priceVector)
    
def acq(bundles, revenue, priceVector, verbose = False, ties = 'random'):
    """
    Given the number of goods, a price vector over each good
    and a valuation for each good, compute the optimal acquisition
    as described in Boyan and Greenwald 2001.
    
    Enumerates surplus for each listed bundle and 
    returns argmax (a bundle) and max surplus.
    
    INPUTS:
        bundles       :=     (2d array-like)
                             rows indicate individual bundles
                             columns are individual goods
                             
        valuation     :=     (1d array-like)
                             an numpy array of valuations, one for each bundle
                             
        priceVector   :=     (1d array-like) 
                             A point price prediction. Each element corresponds to a good 
                             priceVector.shape[0] == bundles.shape[1] == number of goods
        
        verbose       :=     output debugging info to stdout
        
        ties          :=     a flag on deciding how bunldes with same utility are decided
                             valid options = 'random'
        
        
    Returns
    -------
        optimalBundle, optimalSurplus
    
    """   
    
    b = numpy.atleast_2d(bundles)
         
    rev = numpy.atleast_1d(revenue)

    pp = numpy.atleast_1d(priceVector)
           
    splus = surplus(bundles     = bundles,
                    valuation   = rev,
                    priceVector = priceVector)
    
    optBundleIdxList = numpy.nonzero(splus == numpy.max(splus))[0] 
    
    argMax = None
    
    if optBundleIdxList.shape[0] == 1:
        argMax = optBundleIdxList
    else:
        if ties == 'random':
            retIdx = numpy.random.random_integers(0,optBundleIdxList.shape[0]-1,1)
            argMax = optBundleIdxList[retIdx]

     
    optBundle  = bundles[argMax][0]       
    optSurplus = splus[argMax]
     
    if verbose:
        print "acq(...): Computing Optimal Bundle"
        table = []
        table.append(["Bundles", "Revenue", "Cost", "Surplus", "argmax"])
        
        costs = cost(bundles, pp)
        binaryArgMax = numpy.zeros(bundles.shape[0])
        binaryArgMax[argMax] = 1
        for bundle, val, c, s, am in zip(b,rev,costs,splus,binaryArgMax):
            table.append(["{0}".format(bundle.astype('int')), val, c, s, am])
        
        pprint_table(sys.stdout, table)
        
    return optBundle, optSurplus
            
        
def marginalUtility(bundles, revenue, priceVector, goodIdx):
    """
    Computes the marginal utility of a specific good given a revenue function
    represented as a list of bundles and revenue arrays and a point price prediction.
    
    INPUTS:
        bundles       :=     (2d array-like)
                             rows indicate individual bundles
                             columns are individual goods
                             
        valuation     :=     (1d array-like) 
                             a list of revenues in 1:1 correspondence 
                             with bundles (rows). E.g. valuation.shape[0] = bundles.shape[0]
                             
        priceVector   :=     (1d array-like) 
                             A point price prediction. Each element corresponds to a good 
                             priceVector.shape[0] == bundles.shape[1] == number of goods
                             
        goodIdx       :=     (int) 
                             A specific good index for which to compute marginal utility
    Returns
    -------
        marginal utility (float)
    """
#        priceVector = numpy.atleast_1d(priceVector)
    priceVector = numpy.asarray(priceVector,dtype = numpy.float)
    
    tempPriceInf = priceVector.copy()
    tempPriceInf[goodIdx] = numpy.float('inf')
    
    tempPriceZero = priceVector.copy()
    tempPriceZero[goodIdx] = numpy.float(0.0)
    

    predictedSurplusInf = acq(bundles, revenue,
                              tempPriceInf)[1]                                               
                                                    
    predictedSurplusZero = acq(bundles, revenue,
                               tempPriceZero)[1]   
                                                      
    margUtil = predictedSurplusZero - predictedSurplusInf
    if margUtil < 0:
        raise ValueError("simYW.marginalUtility(...) - Negative Marginal Utility (shouldn't happen).")
    
    return margUtil