"""
this is /experiments/convergence/convergence.py

Author: Brandon A. Mayer
Date: 1/3/2013

Experiment to test convergence of joint and conditional local bid.

1) generate price samples uniformly on the interval [0,50] for 5 goods
2) generate N random valuations
3) generate I initial bids
4) compute bids via condLocal and jointLocal algorithms
5) compute number of times (and to what bid) the algorithms converge (or diverge).

"""

from ssapy import listBundles
from ssapy import msListRevenue, msRandomValueVector
from ssapy.strategies.condLocal import condLocal
from ssapy.strategies.jointLocal import jointLocal

import uuid
import os

import numpy
def main():
    m = 5 #number of goods
    vmin = 0  #min valuation
    vmax = 50 #max valuation
    
    nPriceSamples = 100
    
    nInitBids = 1000
    
    nRevFun = 1

    bundles = listBundles(m)
    
    priceSamples = numpy.random.rand(nPriceSamples,m)*50
    
    maxItr = 100
    tol = 0.003
    
    for valIdx in xrange(nRevFun):
        print "valIdx = {0}".format(valIdx)
        oDir = os.path.realpath(os.path.join(".",str(uuid.uuid4())))
        os.makedirs(oDir)
        
        v, l = msRandomValueVector(vmin, vmax, m)
        
        revenue = msListRevenue(bundles, v, l)
        
        numpy.savetxt(os.path.join(oDir,'bundles'), bundles)
        numpy.savetxt(os.path.join(oDir,'revenue'), revenue)
        
        for initBidIdx in xrange(nInitBids):
            print "\t initial bid number {0}".format(initBidIdx)
            initialBid = numpy.random.rand(m)*50
            
            jbid, jconv, jitr, jl = jointLocal(bundles, revenue, initialBid, priceSamples, maxItr, tol, True)
            cbid, cconv, citr, cl = condLocal(bundles, revenue, initialBid, priceSamples, maxItr, tol, True)
            
            with open(os.path.join(oDir,'initialBids.txt'),'a') as f:
                f.write("{0}\n".format(initialBid))
                
            with open(os.path.join(oDir,"jointLocalBids.txt"),'a') as f:
                f.write("{0}\n".format(jbid))
                
            with open(os.path.join(oDir,'jointLocalConverge.txt'),'a') as f:
                f.write("{0}\n".format(jconv))
                
            with open(os.path.join(oDir,'jointLocalItr.txt'),'a') as f:
                f.write("{0}\n".format(jitr))
                
            with open(os.path.join(oDir,'jointLocalDist.txt'),'a') as f:
                f.write("{0}\n".format(jl))
                
            with open(os.path.join(oDir,'condLocalBids.txt'),'a') as f:
                f.write("{0}\n".format(cbid))
                
            with open(os.path.join(oDir,'condLocalConverge.txt'),'a') as f:
                f.write("{0}\n".format(cconv))
            
            with open(os.path.join(oDir,'condLocalItr.txt'),'a') as f:
                f.write("{0}\n".format(citr))
                
            with open(os.path.join(oDir,'condLocalDist.txt'),'a') as f:
                f.write("{0}\n".format(cl))
        
        
        
        
        
        
        
        

if __name__ == "__main__":
    main()