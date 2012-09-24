#!/usr/bin/env python
import argparse

from ssapy.tests.testCompareWellman import writeBidsFile

def main():
    desc = 'Given Price Prediction strategy, search for self-confirming price prediction using marginal bayesian method'
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument('--oDir', action = 'store', dest = 'oDir', required = True,
                        help = "Must provide output directory")
    
    parser.add_argument('--bidsFile', action = 'store', dest = 'bidsFile', required = True,
                        help = "Wellmans [agent-type]-bids.txt file to use as ground truth")
    
    parser.add_argument('--ppFile', action = 'store', dest = 'ppFile', required = True,
                        help = "Wellmans price prediction file [agentParameters].csv to use a price prediction")
    
    parser.add_argument('--agentType', action = 'store', dest = 'agentType', required = True,
                        help = "Mayer's equivalent agent type.")

    args = parser.parse_args().__dict__
    
    writeBidsFile(**args)

if __name__ == "__main__":
    main()