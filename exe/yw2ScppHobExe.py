#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')

from ssapy.pricePrediction.algo.yw2Hob import yw2Hob

import numpy
import multiprocessing

import argparse

def main():
    desc = 'Given Price Prediction strategy, search to a joint self confirming price distribution of closing prices using highest other opponent bids'
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument('--oDir', action = 'store', dest = 'oDir', required = True,
                        help = "Must provide output directory.")
    
    parser.add_argument('--agentType', action = 'store', dest = 'agentType', required = True,
                        help="Must provide agent type (strategy).")
    
    parser.add_argument('--nAgents', action = 'store', dest = 'nAgents', default = 8, type = int,
                        help="Number of agents participating in auction.")
    
    parser.add_argument('--nGames', action = 'store', dest = 'nGames', default = 10000, type = int,
                        help = "Number of auction simulations per iteration.")
    
    parser.add_argument('--m', action = 'store', dest = 'm',default = 5, type = int,
                        help = "Number of goods up for auction; the dimensionality of the joint distribution of closing prices.")
    
    parser.add_argument('--selfIdx', action = 'store', dest = 'selfIdx', default = 0, type = int,
                        help = "Index of the agent to consider as \"self\". Maximum bids will exclude this agent's bids.")
    
    parser.add_argument('--minPrice', action = 'store', dest = 'minPriceString', default = "0", type = int,
                        help = "The minimum valid price for a good.")
    
    parser.add_argument('--maxPrice', action = 'store', dest = 'maxPriceString', default = "50", type = int,
                        help = "The maximum valid price for a good. inf -> no price ceiling.")
    
    parser.add_argument('--minValuation', action = 'store', dest = 'minValuation', default = "0", type = int,
                        help = "The minimum valuation for a good.")
    
    parser.add_argument('--maxValuation', action = 'store', dest = 'maxValuation', default = "50", type = int,
                        help = "The maximum valuation for a good.")
    
    parser.add_argument('--maxItr', action = 'store', dest = 'maxItr', default = 100, type = int,
                        help = "Backup stopping criteria for simulations which do not converge in the KL sense.")
    
    parser.add_argument('--tol', action = 'store', dest = 'tol', default = 0.001,
                        help = "Inter-iteration KL-Divergence tolerence.")
    
    parser.add_argument('--dampen', action = 'store', dest = 'dampen', default = True, type = bool,
                        help = "Use Y-W dampening schedule.")
    
    parser.add_argument('--parallel', action = 'store', dest = 'parallel', default = False, type = bool,
                        help = "Run the simulations in serial or parallel")
    
    parser.add_argument('--nProc', action = 'store', dest = 'nProc', default = multiprocessing.cpu_count(), type = int,
                        help = "Number of processors to use if parallel option is true. (Defaults to all available)")
    
    parser.add_argument('--savePkl', action = 'store', dest = 'savePkl', default = True, type = bool,
                        help = "Save a .pkl snapshot of the joint distribution at every iteration.")
    
    parser.add_argument('--saveTime', action = 'store', dest = 'saveTime', default = True, type = bool,
                        help = "Save the timing info to file.")
    
    parser.add_argument('--pltMarg', action = 'store', dest = 'pltMarg', default = True, type = bool,
                        help = "Plot the marginal distributions of each good from the corresponding joint distribution at each iteration.")
    
    parser.add_argument('--pltKld', action = 'store', dest = 'pltKld', default = True, type = bool,
                        help = "Plot K-L divergence to file at termination.")
    
    parser.add_argument('--pltKs', action = 'store', dest = 'pltKs', default = True, type = bool,
                        help = "Plot K-S statistic to file at termination.")
    
    parser.add_argument('--verbose', action = 'store', dest = 'verbose', default = True, type = bool,
                        help = "Ouput information to std out.")
    
    args = parser.parse_args().__dict__
    
    if args['selfIdx'] > args['nAgents']:
        raise ValueError("Error --- jointGmmScppHob_exe.py selfIdx exceed number of agents.")
        
    args['tol'] = numpy.float(args.get('tol'))
    
    args['pltMarg'] = bool(args.get('pltMarg'))
    
    yw2Hob(**args)

if __name__ == "__main__":
    main()