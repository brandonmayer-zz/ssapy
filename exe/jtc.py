#!/usr/bin/env python
from ssapy.pricePrediction.jointGMM import jointGMM
import argparse
import pickle
import os
import numpy

def main():
    desc = "Computes Mutual Information of jointly Gaussian distributed random variables."
    
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument('-i', '--inFile', action = 'store', dest = 'inFile', required = True,
                        help = "Must specify an input .pkl file.")
    
    parser.add_argument('-n', '--nsamples', action = 'store', dest = 'nsamples', default = 10000, 
                        type = int, required = False, help = "Number of samples used in Mutual Information approximation.")
    
    parser.add_argument('-nt','--ntrials', action='store', dest='nt',default = 100,
                        type = int, required = False, 
                        help = "Number of trials to sample Mutual Information.")
    
    parser.add_argument('-o','--output',action='store',dest='output',default=None,
                        required=False, help = "Output directory. Default prints to stdout.")
    
    parser.add_argument('-v','--verbose',action='store',dest='verbose',
                        default=False,required=False, type=bool,
                        help = "Print debugging info.")
    

    args = parser.parse_args()
    with open(args.inFile,'r') as f:
        gmm = pickle.load(f)
        
    tclist, tcmean, tcvar = \
        gmm.totalCorrelationMC(nsamples=args.nsamples,
            ntrials=args.nt, verbose=args.verbose)
    
    if args.output == None:
        print ' '.join(map(str,tclist))
        print tcmean
        print tcvar
    else:
        oDir = os.path.realpath(args.output)
        numpy.savetxt(os.path.join(oDir,'tclist.txt'),tclist)
        numpy.savetxt(os.path.join(oDir,'tcmean.txt'),tcmean)
        numpy.savetxt(os.path.join(oDir,'tcvar.txt'),tcvar)
                        
if __name__ == "__main__":
    main()