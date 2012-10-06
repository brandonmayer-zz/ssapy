#!/usr/bin/env python

from ssapy.pricePrediction.algo.jointGmmSCPP import jointGaussSCPP
import numpy

import matplotlib
matplotlib.use('Agg')

import argparse
import multiprocessing
import os

def main():
    desc = 'Given Price Prediction strategy, search to a joint self confirming price distribution of closing prices'
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
    
    parser.add_argument('--minPrice', action = 'store', dest = 'minPriceString', default = "0",
                        help = "The minimum valid price for a good.")
    
    parser.add_argument('--maxPrice', action = 'store', dest = 'maxPriceString', default = "inf",
                        help = "The maximum valid price for a good. inf -> no price ceiling.")
    
    parser.add_argument('--parallel', action = 'store', dest = 'parallel', default = False, type = bool,
                        help = "Run the simulations in serial or parallel")
    
    parser.add_argument('--nProc', action = 'store', dest = 'nProc', default = multiprocessing.cpu_count(), type = int,
                        help = "Number of processors to use if parallel option is true. (Defaults to all available)")
    
    parser.add_argument('--klSamples', action = 'store', dest = 'klSamples', default = 10000, type = int,
                        help = "Number of samples drawn from current and old distributions to approximate KL-Divergence.")
    
    parser.add_argument('--maxItr', action = 'store', dest = 'maxItr', default = 100, type = int,
                        help = "Backup stopping criteria for simulations which do not converge in the KL sense.")
    
    parser.add_argument('--tol', action = 'store', dest = 'tol', default = 0.001,
                        help = "Inter-iteration KL-Divergence tolerence.")
    
    parser.add_argument('--covarType', action = 'store', dest = 'covarType', default = 'full',
                        help = "Complexity of covariance matrix: 'full', 'diag', 'sphere'")
    
    parser.add_argument('--savePkl', action = 'store', dest = 'savePkl', default = True, type = bool,
                        help = "Save a .pkl snapshot of the joint distribution at every iteration.")
    
    parser.add_argument('--verbose', action = 'store', dest = 'verbose', default = True, type = bool,
                        help = "Ouput information to std out.")
    
    parser.add_argument('--aicCompMin', action = 'store', dest = 'aicCompMin', default = 1, type = int,
                        help = "Minimum number of components to check")
    
    parser.add_argument('--aicCompMax', action = 'store', dest = 'aicCompMax', default = 10, type = int,
                        help = "Maximum number of components for GMM to evaluate.")
    
    parser.add_argument('--aicMinCovar', action = 'store', dest = 'aicMinCovar', default = 1.0,
                        help = "Minimum diagonal covariance to avoid sinularities in GMM EM fitting algorithm.")
    
    parser.add_argument('--pltSurf', action = 'store', dest = 'pltSurf', default = False, type = bool,
                        help = "Make surface plot of joint probability distribution every iteration. Only works if m = 2.")
    
    parser.add_argument('--pltMarg', action = 'store', dest = 'pltMarg', default = False, type = bool,
                        help = "Plot the marginal distributions of each good from the corresponding joint distribution at each iteration.")
    
    args = parser.parse_args().__dict__
    
    args['minPrice'] = numpy.float(args.get('minPriceString'))
    args['maxPrice'] = numpy.float(args.get('maxPriceString'))
    args['aicMinCovar'] = numpy.float(args.get('aicMinCovar'))
    args['tol'] = numpy.float(args.get('tol'))
    args['pltSurf'] = bool(args.get('pltSurf'))
    args['pltMarg'] = bool(args.get('pltSurf'))
    
    jointGaussSCPP(**args)
    
if __name__ == "__main__":
    main()