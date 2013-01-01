from ssapy.pricePrediction import dok_hist
import numpy

def jointLocalBid(bundles, valuation, pricePrediction, bids, verbose = False):
    pricePrediction = kwargs.get('pricePrediction')
    
    if pricePrediction == None:
        raise KeyError("Must specify pricePrediction.")
    

def jointLocalBidUpdate(bundles, valuation, pricePrediction,
                        bid_vector, update_index, verbose ):
    
    bundle_value_dict = dict([(tuple(b),v) for b,v, in zip(bundles,valuation)])
    
    
        
    new_bid = 0.0
    
    if verbose:
        print 'current bid = {0}'.format(bid_vector)
        print 'updating bid for good {0}'.format(update_index)
        print 'New bid initialized to {0}\n'.format(new_bid)
        
        
    
    for bundle1 in bundles[bundles[:,update_index] == True]:
        
        bundle1_index = numpy.all(bundles == bundle1,1).argmax()
        bundle0 = bundle1.copy()
        bundle0[update_index] = False
        bundle0_index = numpy.all(bundles == bundle0,1).argmax()
        
        if verbose:
            print 'bundle1_index = {0}'.format(bundle1_index)
            print 'bundle0_index = {0}'.format(bundle0_index)
        
        
        if verbose:
            print 'bundle0 = {0}'.format(bundle1)
            print 'bundle1 = {0}'.format(bundle0)
            
        v1 = valuation[bundle1_index]
        v0 = valuation[bundle0_index]
        
        if verbose:
            print 'v1 = {0}'.format(v1)
            print 'v0 = {0}'.format(v0)
        
        
        if isinstance(pricePrediction, dok_hist.dok_hist):
            p1 = dok_hist.prob_win_given_bid(pricePrediction, bundle1, bid_vector)
            p0 = dok_hist.prob_win_given_bid(pricePrediction, bundle0, bid_vector)
            
            if verbose:
                print 'p1 = {0}'.format(p1)
                print 'p0 = {0}'.format(p0)
            
            new_bid += (v1-v0)*(p1+p0)
            if verbose:
                print 'new_bid = {0}\n'.format(new_bid)
        else:
            raise TypeError("Unknown Price Prediction Type")
        
    return new_bid    