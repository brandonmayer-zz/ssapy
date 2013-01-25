import numpy
import os
import pickle
import matplotlib.pyplot as plt

from ssapy import timestamp_
from ssapy.strategies.jointLocal import jointLocal
from ssapy.strategies.margLocal import margLocal
from ssapy.pricePrediction.jointGMM import jointGMM, expectedSurplus
from ssapy.agents.marketSchedule import randomValueVector, listRevenue, listBundles
from ssapy import listBundles
from ssapy.util.padnums import pprint_table

def main():
    nrev = 1000
    n_samples = 10000
    m = 5
    es = numpy.zeros((nrev,2))
    
    rootDir = os.path.realpath(".")
    oDir = os.path.join(rootDir,timestamp_())
    if not os.path.exists(oDir):
        os.makedirs(oDir)
        
    table = [["parameter", "value"]]
    table.append(["nrev", nrev])
    table.append(["n_samples",n_samples])
    table.append(["m",m])
    
    
    with open(os.path.join(oDir,'params.txt'),'w') as f:
        pprint_table(f,table)
        
    scppFile = os.path.realpath("./jointGmmScppHob_msStraightMUa_0024.pkl")
    
    with open(scppFile,'r') as f:
        scpp = pickle.load(f)
        
    bundles = listBundles(m)
        
    for i in xrange(nrev):
        print 'iteration {0}'.format(i)
        
        v,l = randomValueVector(m=m)
        revenue = listRevenue(bundles, v, l)
        bundleRevenueDict = {}
        for b,r in zip(bundles,revenue):
            bundleRevenueDict[tuple(b)] = r
            
        jointSamples = scpp.sample(n_samples = n_samples)
        margSamples = scpp.sampleMarg(n_samples = n_samples)
        
        initBid = numpy.random.rand(m)*50
        
        jbid = jointLocal(bundles,revenue,initBid,jointSamples)
        with open(os.path.join(oDir,"jointLocalBids"),'a') as f:
            numpy.savetxt(f, jbid.T)
            
        mbid = margLocal(bundles,revenue,initBid,margSamples)
        with open(os.path.join(oDir,"margLocalBids"),'a') as f:
            numpy.savetxt(f, mbid.T)
        
        es[i,0]= expectedSurplus(bundleRevenueDict, jbid, scpp, n_samples)
        es[i,1] = expectedSurplus(bundleRevenueDict, mbid, scpp, n_samples)
        
        with open(os.path.join(oDir,"jointLocalExpectedSurplus.txt"),'a') as f:
            numpy.savetxt(f,numpy.atleast_1d(es[i,0]))
        
        with open(os.path.join(oDir,"margLocalExpectedSurplus.txt"),'a') as f:
            numpy.savetxt(f,numpy.atleast_1d(es[i,1])) 
    
    with open(os.path.join(oDir,'stats.txt'),'w') as f:
        print >> f, "jointLocal Expected Surplus Mean {0}".format(numpy.mean(es[:,0]))
        print >> f, "jointLocal Expected Surplus Variance {0}".format(numpy.var([es[:,0]]))
        print >> f, "margLocal Expected Surplus Mean {0}".format(numpy.mean(es[:,1]))
        print >> f, "margLocal Expected Surplus Variance {0}".format(numpy.var(es[:,1]))
            
    bins = range(int(es.min())-1,int(es.max())+1)
    jhist,jbins = numpy.histogram(es[:,0], bins,normed=True)
    mhist,mbins = numpy.histogram(es[:,1], bins,normed=True)
    
    f,ax = plt.subplots(2,1,sharex = True)
    ax[0].bar((jbins[:-1]+jbins[1:])/2,jhist,align='center')
    ax[0].set_title("jointLocal")
    ax[1].bar((mbins[:-1]+mbins[1:])/2,mhist,align='center')
    ax[1].set_title("margLocal")
    
    plt.savefig(os.path.join(oDir,"ExpectedSurplus.pdf"))
    plt.show()
    
    

if __name__ == "__main__":
    main()