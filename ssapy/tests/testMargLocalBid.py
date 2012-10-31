from ssapy import getStrategy
from ssapy.agents.simYW import randomValueVector,valuation
from ssapy import allBundles

import pickle
import os
from idlelib.SearchEngine import get

def main():
    pricePredictionFile = os.path.realpath("./jointGmmScppHob_straightMU8_m5_n8_00013.pkl")
    with open(pricePredictionFile,'r') as f:
        pricePrediction = pickle.load(f)
        
    m = 5
    bundles = allBundles(m)
    v,l = randomValueVector()
    val = valuation(bundles,v,l)
    
    strategy = getStrategy('margLocalBid')
    
    bids = strategy(pricePrediction = pricePrediction,
                    bundles = bundles, valuation = val)
    
    print 'bids = {0}'.format(bids)
    

if __name__ == "__main__":
    main() 