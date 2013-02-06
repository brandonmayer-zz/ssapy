from scipy.optimize import fmin
import numpy

def expectedSurplusSamples(bid, bundleRevenueDict, evalSamples):
    es = numpy.float64(0.)
    
    for sample in evalSamples:
        goodsWon = sample <= bid
        rev = bundleRevenueDict[(tuple(goodsWon))]
        cost = numpy.dot(goodsWon,sample)
        es += rev-cost
        
    return es/evalSamples.shape[0]

def downHillSS(bundleRevenueDict, initBid, evalSamples, 
                    maxiter = 100, disp = True,
                    clip = True, ret = 1):
    
    bid, expectedSurplus, nItr, nFncCalls, warnFlag = \
        fmin(expectedSurplusSamples, x0 = initBid, 
             args = (bundleRevenueDict,evalSamples), 
             maxiter = maxiter, disp = disp,
             full_output = True, retall = False )
        
#    bid = out[0]
    
#    out[0] = numpy.atleast_1d(out[0])
    if clip:
        bid = bid.clip(0)
        
    if ret == 1:
        return bid
    elif ret == 2:
        return bid, expectedSurplus
    elif ret == 3:
        return bid, expectedSurplus, nItr
    elif ret == 4:
        return bid, expectedSurplus, nItr, nFncCalls
    elif ret == 5:
        return bid, expectedSurplus, nItr, nFncCalls, warnFlag
    else:
        raise ValueError('Unknonw Return Code {0}'.format(ret))
        