import numpy

from ssapy.strategies.targetMV import targetMV

def targetMU(**kwargs):
    pricePrediction = kwargs.get('pricePrediction')
    if pricePrediction == None:
        raise KeyError("targetMU.SS(...) - must specify pricePrediction")
    
    bundles = kwargs.get('bundles')
    if bundles == None:
        raise KeyError("targetMU.SS(...) - must specify bundles")
            
    valuation = kwargs.get('valuation')
    if valuation == None:
        raise KeyError("targetMU - must specify valuation")
    
    n_samples = kwargs.get('n_samples')
    if n_samples == None:
        raise KeyError("Must specify number of samples")
    
    samples = pricePrediction.sample(n_samples = n_samples)
    
    expectedPrices = numpy.mean(samples,0)
    
    return targetMV( bundles         = bundles,
                     valuation       = valuation,
                     pricePrediction = expectedPrices)
    
    
def targetMU8(**kwargs):
    kwargs.update({'n_samples':8})
    
    return targetMU(**kwargs)

def targetMU64(**kwargs):
    kwargs.update({'n_samples':64})
    
    return targetMU(**kwargs)

def targetMU256(**kwargs):
    kwargs.update({'n_samples':256})
    
    return targetMU(**kwargs)