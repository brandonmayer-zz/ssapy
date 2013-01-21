#!/usr/bin/env python
from ssapy.pricePrediction.jointGMM import jointGMM
import argparse
import pickle
import os

def main():
    desc = "Computes Mutual Information of jointly Gaussian distributed random variables."
    
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument('-i', '--inFile', action = 'store', dest = 'inFile', required = True,
                        help = "Must specify an input .pkl file.")
    
    parser.add_argument('-n', '--n_samples', action = 'store', dest = 'n_samples', default = 10000, 
                        required = False, help = "Number of samples used in Mutual Information approximation.")
    

    args = parser.parse_args()
    with open(args.inFile,'r') as f:
        gmm = pickle.load(f)
        
    print gmm.mutualInformation(n_samples = args.n_samples)
                        
if __name__ == "__main__":
    main()