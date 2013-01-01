import numpy
import itertools

def listBundles(m = 5):
    """
    Return a numpy 2d array of all possible bundles that the agent can
        bid on given the number of auctions.
        
    The Rows represent the bundle index.
        
    The Columns Represent the good index.        
        
    Return bundles as booleans for storage and computational efficiency
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
    # convert to decimal rather than enumerating power set
    # and selecting correct bundle
    
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
    
    Parameters
    ----------
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
    
def surplus(bundles=None, valuation = None, priceVector = None):
        """
        Calculate the surplus for a given array of bundles, prices and a valuation (scalar).
        Surplus equals valuation less cost.
        """
                   
        bundles = numpy.atleast_2d(bundles)
        
        valuation = numpy.atleast_1d(valuation)
        
        return valuation - cost(bundles = bundles, price = priceVector)
    
def acq(**kwargs):
    """
    Given the number of goods, a price vector over each good
    and a valuation for each good, compute the optimal acquisition
    as described in Boyan and Greenwald 2001.
    
    INPUTS:
        bundles       :=     a numpy 2d array
                             rows indicate individual bundles
                             columns are individual goods
                             
        priceVector   :=     vector of prices over goods.
                             priceVector.shape[0] == bundles.shape[1] == number of goods
        
        valuation     :=     an numpy array of valuations, one for each bundle
        
        ties          :=     a flag on deciding how bunldes with same utility are decided
                             valid options = 'random'
        
        
    Returns
    -------
        optimalBundle, optimalSurplus
    
    """   
    
    revDict = kwargs.get('revDict')
    if revDict == None:
        bundles = numpy.atleast_2d(kwargs.get('bundles'))
         
        valuation = numpy.atleast_1d(kwargs.get('valuation'))
    else:
        bundles = numpy.atleast_2d(revDict.keys())
        valuation = numpy.atleast_1d(revDict.values())
    
    priceVector = numpy.atleast_1d(kwargs.get('priceVector'))
    
    ties = kwargs.get('ties','random')
    
    splus = kwargs.get('surplus')
    
    if splus == None:
        val = kwargs.get('valuation')
        
        if val == None:
            raise KeyError("Must specify either surplus or valuation.")
        
        splus = kwargs.get('surplus', surplus(bundles     = bundles,
                                              valuation   = valuation,
                                              priceVector = priceVector))
    
    optBundleIdxList = numpy.nonzero(splus == numpy.max(splus))[0] 
    
    if optBundleIdxList.shape[0] == 1:
        return bundles[optBundleIdxList][0], splus[optBundleIdxList] 
    else:
        if ties == 'random':
            retIdx = numpy.random.random_integers(0,optBundleIdxList.shape[0]-1,1)
            return bundles[optBundleIdxList[retIdx]][0], splus[optBundleIdxList[retIdx]]
        
def marginalUtility(bundles, priceVector, valuation, goodIdx):
#        priceVector = numpy.atleast_1d(priceVector)
    priceVector = numpy.asarray(priceVector,dtype = numpy.float)
    
    tempPriceInf = priceVector.copy()
    tempPriceInf[goodIdx] = numpy.float('inf')
    
    tempPriceZero = priceVector.copy()
    tempPriceZero[goodIdx] = numpy.float(0.0)
    

    predictedSurplusInf = acq(bundles     = bundles,
                              valuation   = valuation,
                              priceVector = tempPriceInf)[1]                                               
                                                    
        
    predictedSurplusZero = acq(bundles     = bundles,
                               valuation   = valuation,
                               priceVector = tempPriceZero)[1]   
                                                      
    margUtil = predictedSurplusZero - predictedSurplusInf
    if margUtil < 0:
        raise ValueError("simYW.marginalUtility(...) - Negative Marginal Utility (shouldn't happen).")
    
    return margUtil