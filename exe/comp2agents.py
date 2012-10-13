#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy

from ssapy.auctions.compAgents import comp2Agents

import argparse
import os 
import pickle
    
def main():
    desc = 'Executable to compare two agents'
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument('--oDir', action = 'store', dest = 'oDir', required = True,
                        help = "Must provide output directory.")
    
    parser.add_argument('--agentType1', action = 'store', dest = 'agentType1', required = True,
                        help="Must provide agent type (strategy).")
    
    parser.add_argument('--pp1', action = 'store', dest = 'pp1', required = True,
                        help="Price prediction file 1.")
    
    parser.add_argument('--n1', action = 'store', dest = 'n1', default = 4, type = int,
                        help="Numer of agents of Type 1")
        
    parser.add_argument('--agentType2', action = 'store', dest = 'agentType2', required = True,
                        help="Must provide agent type (strategy).")
    
    parser.add_argument('--n2', action = 'store', dest = 'n2', default = 4, type = int,
                        help="Numer of agents of Type 2")
    
    parser.add_argument('--pp2', action = 'store', dest = 'pp2', required = True,
                        help="Price prediction file 2.")
    
    parser.add_argument('--nGames', action = 'store', dest = 'nGames', default = 10000, type = int,
                        help = "Number of auction simulations per iteration.")
    
    parser.add_argument('--verbose', action = 'store', dest = 'verbose', default = True, type = bool,
                        help = "Output run info to std out.")
    
    args = parser.parse_args().__dict__
    
    oDir       = args.get('oDir')
    agentType1 = args.get('agentType1')
    ppFile1    = args.get('pp1')
    n1         = args.get('n1')
    
    agentType2 = args.get('agentType2')
    ppFile2    = args.get('pp2')
    n2         = args.get('n2')

    nGames     = args.get('nGames')
    
    verbose    = args.get('verbose')
    
    if verbose:
        print 'In ssapy/exe/comp2agents.py'
        print 'oDir       = {0}'.format(oDir)
        print 'agentType1 = {0}'.format(agentType1)
        print 'ppFile1    = {0}'.format(ppFile1)
        print 'n1         = {0}'.format(n1)
        print 'agentType2 = {0}'.format(agentType2)
        print 'ppFile2    = {0}'.format(ppFile2)
        print 'n2         = {0}'.format(n2)
        print 'nGames     = {0}'.format(nGames)
    
    oDir = os.path.realpath(oDir)
    if not os.path.exists(oDir):
        os.makedirs(oDir)
    
    with open(ppFile1,'r') as f:
        pp1 = pickle.load(f)
    
    with open(ppFile2,'r') as f:
        pp2 = pickle.load(f)
        
    paramFile = os.path.join(oDir,'params.txt')
    
    with open(paramFile,'w') as f:
        f.write("{0}\n".format(agentType1))
        f.write("{0}\n".format(n1))
        f.write("{0}\n".format(ppFile1))
        
        f.write("{0}\n".format(agentType2))
        f.write("{0}\n".format(n2))
        f.write("{0}\n".format(ppFile2))
        
        f.write("{0}\n".format(nGames))
        
        
    surplus = comp2Agents( oDir       = oDir,
                           pp1        = pp1,
                           pp2        = pp2,
                           n1         = n1,
                           n2         = n2,
                           agentType1 = agentType1,
                           agentType2 = agentType2,
                           nGames     = nGames,
                           verbose    = True)
    
    
        
    s1 = numpy.mean(surplus[:,:n1],1)
    b1Min = int(s1.min()-1)
    b1Max = int(s1.max()+1)
    bins1 = numpy.arange(b1Min,b1Max)
    
    s2 = numpy.mean(surplus[:,n1:],1)
    b2Min = int(s2.min()-1)
    b2Max = int(s2.max()+1)
    bins2 = numpy.arange(b2Min,b2Max)
    
    h1, b1 = numpy.histogram(s1, bins=bins1, density=True)
    h2, b2 = numpy.histogram(s2, bins=bins2, density=True)
    
    f = plt.figure()
    ax = f.add_subplot(111)
    plt.plot(b1[:-1],h1, label = "{0}".format(agentType1))
    plt.plot(b2[:-1],h2, label = "{0}".format(agentType2))
    ax.set_title("{0} vs. {1} {2} auctions".format(agentType1, agentType2, nGames))
    ax.set_xlabel("Average Game Surplus")
    ax.set_ylabel(r"$p(\bar{\sigma})$")
    leg = ax.legend(loc = 'best', fancybox = True)
    leg.get_frame().set_alpha(0.5)
    
    pltFile = os.path.join(oDir,"{0}_{1}_{2}_{3}_{4}.pdf".format(agentType1, agentType2, n1, n2, nGames))
    plt.savefig(pltFile)
    
    

if __name__ == "__main__":
    main()