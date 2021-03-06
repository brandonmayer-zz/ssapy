#!/usr/bin/env python
from ssapy.pricePrediction.bayesSCPP import bayesSCPP
               
import multiprocessing                
import argparse
import os
    
    
def main():
    """
    Formats of txt files:
        for probability distributions;
            rows alternate probability distribution - bins
            e.g. row 1 is probability distribution for good 1
                 row 2 is bins for prob. in row 1
                 row 3 is probability distribution for good 2
                 row 4 is bins for prob. in row 2
                 
                 
        for histograms, it is the same pattern only replacing probabilities with integer counts. 
    """
    desc = 'Given Price Prediction strategy, search for self-confirming price prediction using marginal bayesian method'
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument( '--oDir', action = 'store', dest = 'oDir', required = True,
                         help = "Must provide output directory" )
                
    parser.add_argument( '--agentType', action = 'store', dest = 'agentType', required = True,
                         help = "Must provide agent type")
    
    parser.add_argument( '--nAgents', action = 'store', dest = 'nAgents', default = 8, type = int,
                         help = "Number of agents in the game")
    
    parser.add_argument( '--m', action = 'store', dest = 'm', default = 5, type = int,
                         help = "Number of goods up for auction")
    
    parser.add_argument( "--minPrice", action = 'store', dest = 'minPrice', default = 0, type = float)
    
    parser.add_argument( "--maxPrice", action = 'store', dest = 'maxPrice', default = 50, type = float)
    
    parser.add_argument( "--maxSim", action = 'store', dest = 'maxSim', default = 1000000, type = int,
                         help = "Maximum number of updates allowed before termination.")
    
    parser.add_argument( "--nGames", action = 'store', dest = 'nGames', default = 100, type = int,
                         help = "Number of auctions simulated prior to checking convergence.")
    
    parser.add_argument( "--parallel", action = 'store', dest = 'parallel', default = False, type = bool,
                         help = "In general this should be false as it is only an approximation to the algorithm")
    
    parser.add_argument("--nProc",action = 'store', dest = 'nProc', default = multiprocessing.cpu_count() - 1, type = int,
                        help = "In general parallel should be false and this shoud not be used." )
    
    parser.add_argument("--tol", action = 'store', dest = 'tol', default = 0.001, type = float,
                        help = "KL-divergence tolerance for scpp")
    
    parser.add_argument("--saveBayesTxt", action = 'store', dest = 'saveBayesTxt', default = True, type = bool,
                        help = "Save a text file of the bayes marginal probability distribution after every iteration.")
    
    parser.add_argument("--saveBayesPkl", action = 'store', dest = 'saveBayesPkl', default = True, type = bool,
                        help = "Save a pickle dump of the margDistSCPP class with the current bayes marginal distribution after every iteration.")
    
    parser.add_argument("--saveHistPkl", action = 'store', dest = 'saveHistPkl', default = True, type = bool,
                        help = "Save a pickle dump of the original hist class (raw counts not bayes prob dist) after every iteration.")

    parser.add_argument("--plot", action = 'store', dest = 'plot', default = False, type = bool,
                        help = "When running on the grid, this should be set to false")
    
    parser.add_argument("--log", action = 'store', dest = 'log', default = True, type = bool,
                        help = "Output a log file of parameters and results." )
    
    parser.add_argument("--verbose", action = 'store', dest = 'verbose', default = True, type = bool,
                        help = "Ouput diagnostics to std out.")
    
    args = parser.parse_args().__dict__
    
    bayesSCPP(**args)
        
if __name__ == "__main__":
    main()    
    
