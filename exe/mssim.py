import argparse
import multiprocessing
import os
import pickle
import time

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy

from ssapy.auctions import simulateAuction
from ssapy.pricePrediction.jointGMM import jointGMM

def main():
    desc = "Simulates a homogenous auction randomizing over valuations."
    
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument('-i','--input', action = 'store', dest = 'input', required = True,
                        help = "Full path to price prediction pickle file.")
    
    parser.add_argument('-a','--agentType', action = 'store', dest = 'agentType', required = True,
                        help = "The participating agent's strategy type.")
    
#    parser.add_argument('-m', action = 'store', dest = 'm', required = False, default = 5,
#                        help = "The number of goods at auction.")
    
    parser.add_argument('-na', '--nAgents', action = 'store', dest = 'n', required = False,
                        default = 5, help = "Number of participating agents")
    
    parser.add_argument('-ng', '--nGames', action = 'store', dest = 'ng', required = False, type=int,
                        default = 10000, help = "Number of Simulations (games) to run.")
    
#    parser.add_argument('-o', '--output', action = 'store', dest = 'output', required = False,
#                        help = "Basename (or path) for output files.")
    
    parser.add_argument('-p', '--parallel', action = 'store', dest = 'parallel', required = False,
                        type = bool, default = True, 
                        help = "Run simulations in parallel or serially.")
    
    parser.add_argument('-np', '--nProc', action = 'store', dest = 'nProc', required = False,
                        default = multiprocessing.cpu_count() - 1, 
                        help = "Number of processes to spawn if running in parallel mode.")
    
    parser.add_argument('-vmin', '--minValuation', action = 'store', dest = 'vmin', required = False,
                        default = 0, help = "Minimum Valuation.")
    
    parser.add_argument('-vmax', '--maxValuation', action = 'store', dest = 'vmax', required = False,
                        default = 50, help = "Maximum Valuation.")
    
    parser.add_argument('-v', '--verbose', action = 'store', dest = 'verbose', type = bool,
                        required = False, default = True, help = "Output runtime info to stdout.")
    
    parser.add_argument('-nc','--normCorr', action = 'store', dest = 'nc', type = bool,
                        required = False, default = True, help = "Comput Sample normalized correlation matrix.")
    
    parser.add_argument('-si', '--selfIdx', action = 'store', dest = 'si', type = int,
                        required = False, default = 0, help = "Compute highest other agent bid wrt this agents' index.")
    
    args = parser.parse_args()
    
    
    
    with open(args.input,'r') as f:
        pp = pickle.load(f)
        
    if isinstance(pp,jointGMM):
        m = pp.m()
    else:
        raise ValueError("Unknown Price Prediction Type.")
    
    start = time.time()
    bids = simulateAuction(pricePrediction = pp,
                           nGames          = args.ng,
                           agentType       = args.agentType,
                           nAgents         = args.n,
                           m               = m,
                           minValuation    = args.vmin,
                           maxValuation    = args.vmax,
                           parallel        = args.parallel,
                           nProc           = args.nProc,
                           verbose         = args.verbose)
    end = time.time()
    
    if args.verbose:
        print 'Finished {0} simulations in {1} seconds.'.format(args.ng, end-start)
    
    oDir     = os.path.dirname(os.path.realpath(args.input))
    basename = os.path.basename(args.input).split('.')[0]
    basename = basename + "_{0}_{1}".format(args.agentType,args.ng)
    
    obids = os.path.join(oDir,basename + "_bids.npz")
    ohob  = os.path.join(oDir,basename + "_hob.txt")
    
    with open(obids,'w') as f:
        numpy.save(f, bids)
        
    idx2keep = numpy.arange(args.n)
    idx2keep = numpy.delete(idx2keep,args.si)
    hob = numpy.max(bids[:,idx2keep,:],1)
    
    with open(ohob,'w') as f:
        numpy.savetxt(f, hob)
        
    if args.nc:
        nc = numpy.corrcoef(hob.T)
        
        ocorr = os.path.join(oDir, basename + "_normcorr.txt")
        numpy.savetxt(ocorr, nc)

        ofig = os.path.join(oDir,basename + "_normcorr.pdf")
        plt.matshow(nc)
        plt.title('Normalized Correlation Matrix')
        plt.colorbar()
        plt.savefig(ofig)
    
        print 'Normalized Correlation Matrix:'
        print nc

if __name__ == "__main__":
    main()