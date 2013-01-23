import argparse
import numpy
import os
import pickle
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from ssapy import timestamp_
from ssapy.strategies.jointLocal import jointLocal
from ssapy.strategies.margLocal import margLocal
from ssapy.strategies.condLocal import condLocal
from ssapy.strategies.straightMU import straightMUa
from ssapy.pricePrediction.jointGMM import jointGMM, expectedSurplus_
from ssapy.agents.marketSchedule import randomValueVector, listRevenue, listBundles
from ssapy import listBundles
from ssapy.util.padnums import pprint_table

def localSearchDominance(nbids = 100, n_samples = 1000, rootDir = ".",
                         scppFile = None, vfile = None, lfile = None,
                         njs = 1000, nms = 1000):
         
    scppFile = os.path.realpath(scppFile)                
    with open(scppFile,'r') as f:
        scpp = pickle.load(f)
        
    m = scpp.m()
    
    bundles = listBundles(m)
    
    
    
    rootDir = os.path.realpath(rootDir)
    oDir = os.path.join(rootDir,timestamp_())
    if not os.path.exists(oDir):
        os.makedirs(oDir)
        
    table = [["parameter", "value"]]
    table.append(["nbids", nbids])
    table.append(["n_samples",n_samples])
    table.append(["m",m])
    table.append(["njs",njs])
    table.append(["nms",nms])
    table.append(["vfile",vfile])
    table.append(["lfile",lfile])
    table.append(["sccpFile", scppFile])
    
    
    
    pprint_table(sys.stdout,table)
    
    with open(os.path.join(oDir,'params.txt'),'a') as f:
        pprint_table(f,table)
    
    jointBidFile = os.path.join(oDir,"jointLocalBids.txt")
    condBidFile = os.path.join(oDir,"condLocalBids.txt")
    margBidFile = os.path.join(oDir,"margLocalBids.txt")
    
    useExternalValuations = False
    if vfile == None and lfile == None:
        vfile = os.path.join(oDir,'v.txt')
        lfile = os.path.join(oDir,'l.txt')
    else:
        vmat = numpy.loadtxt(vfile)
        lmat = numpy.loadtxt(lfile)
        nbids = lmat.shape[0]
        useExternalValuations = True
        
    surplusSamples = scpp.sample(n_samples = n_samples)
    numpy.savetxt(os.path.join(oDir,'ppSamples.txt'),surplusSamples)
    
    jsdir = os.path.join(oDir,'jointSamples')
    if not os.path.exists(jsdir):
        os.makedirs(jsdir)
        
    msdir = os.path.join(oDir,'margSamples')
    if not os.path.exists(msdir):
        os.makedirs(msdir)
    
    es = numpy.zeros((nbids,3))
    for i in xrange(nbids):
        print 'Bid number {0}'.format(i)
        
        if useExternalValuations:
            v = vmat[i,:]
            l = lmat[i]
            
        else:
            print 'randomizing valuation'
            v,l = randomValueVector(m=m)    
            with open(vfile,'a') as f:
                numpy.savetxt(f, v.reshape(1,v.shape[0]))
#                print >> f, v
            with open(lfile,'a') as f:
                numpy.savetxt(f,numpy.atleast_1d(l))
        
        print 'v = {0}'.format(v)
        print 'l = {0}'.format(l)
        
        revenue = listRevenue(bundles, v, l)
        bundleRevenueDict = {}
        for b, r in zip(bundles,revenue):
            bundleRevenueDict[tuple(b)] = r
        
        jointSamples = scpp.sample(n_samples = njs)
        margSamples = scpp.sampleMarg(n_samples = nms)
        
        numpy.savetxt(
            os.path.join(jsdir,'jointSamples_{0:04}.txt'.format(i)),
                jointSamples)
        
        numpy.savetxt(
            os.path.join(msdir,'margSamples_{0:04}.txt'.format(i)),
                margSamples)
        
        initBid = straightMUa(bundles, revenue, scpp)
    
        jbid = jointLocal(bundles,revenue,initBid,jointSamples)
        cbid = condLocal(bundles, revenue, initBid, jointSamples)
        mbid = margLocal(bundles, revenue, initBid, margSamples)
        
        with open(jointBidFile,'a') as f:
            numpy.savetxt(f, jbid.T)
        
        with open(condBidFile,'a') as f:
            numpy.savetxt(f, cbid.T)
        
        with open(margBidFile,'a') as f:
            numpy.savetxt(f, mbid.T)
            
        es[i,0] = expectedSurplus_(bundleRevenueDict, jbid, surplusSamples)
        es[i,1] = expectedSurplus_(bundleRevenueDict, cbid, surplusSamples)   
        es[i,2] = expectedSurplus_(bundleRevenueDict, mbid, surplusSamples)
        
        with open(os.path.join(oDir,"jointLocalExpectedSurplus.txt"),'a') as f:
            numpy.savetxt(f,numpy.atleast_1d(es[i,0]))
            
        with open(os.path.join(oDir,"condLocalExpectedSurplus.txt"),'a') as f:
            numpy.savetxt(f,numpy.atleast_1d(es[i,1])) 
        
        with open(os.path.join(oDir,"margLocalExpectedSurplus.txt"),'a') as f:
            numpy.savetxt(f,numpy.atleast_1d(es[i,2])) 
        
    jmean = numpy.mean(es[:,0])
    jvar  = numpy.var(es[:,0])
    cmean = numpy.mean(es[:,1])
    cvar  = numpy.var(es[:,1])
    mmean = numpy.mean(es[:,2])
    mvar  = numpy.var(es[:,2])
    
    print 'jointLocal Expected Surplus Mean {0}'.format(jmean)
    print 'jointLocal Expected Surplus Variance {0}'.format(jvar)
    print 'condLocal Expected Surplus Mean {0}'.format(cmean)
    print 'condLocal Expected Surplus Variance {0}'.format(cvar)
    print 'margLocal Expected Surplus Mean {0}'.format(mmean)
    print 'margLocal Expected Surplus Variance {0}'.format(mvar)
    
    with open(os.path.join(oDir,'jointLocalStats.txt'),'a') as f:
        print >> f, 'mean ', jmean
        print >> f, 'var ', jvar
        
    with open(os.path.join(oDir,'condLocalStats.txt'),'a') as f:
        print >> f, 'mean ', cmean
        print >> f, 'var ', cvar
        
    with open(os.path.join(oDir,'margLocalStats.txt'),'a') as f:
        print >> f, 'mean ', mmean
        print >> f, 'var ', mvar
        
    with open(os.path.join(oDir,'stats.txt'),'a') as f:
        print >> f, 'jointLocal expected surplus mean: {0}'.format(jmean)
        print >> f, 'jointLocal expected surplus variation: {0}'.format(jvar)
        print >> f, 'condLocal expected surplus mean: {0}'.format(cmean)
        print >> f, 'condLocal expected surplus variation: {0}'.format(cvar)
        print >> f, 'margLocal expected surplus mean: {0}'.format(mmean)
        print >> f, 'margLocal expected surplus variation: {0}'.format(mvar)
        
        
    bins = range(int(es.min())-1, int(es.max())+1)
    
    jhist, jbins = numpy.histogram(es[:,0], bins, normed = True)
    chist, cbins = numpy.histogram(es[:,1], bins, normed = True)
    mhist, mbins = numpy.histogram(es[:,2], bins, normed = True)
    
    f,ax = plt.subplots(3,1, sharex = True)
    ax[0].bar( (jbins[:-1]+jbins[1:])/2, jhist, align = 'center')
    ax[0].set_title('jointLocal expected surplus')
    ax[1].bar( (cbins[:-1]+cbins[1:])/2, chist, align = 'center' )
    ax[1].set_title('condLocal expected surplus')
    ax[2].bar( (mbins[:-1]+mbins[1:])/2, mhist, align = 'center')
    ax[2].set_title('margLocal expected surplus')
    
    plt.savefig(os.path.join(oDir,'expectedSurplus.pdf'))
    
def main():
    desc = "Computes Expected Surplus of bids resulting form" +\
            "jointLocal, condLocal and margLocal with the same revenue function"
    
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument('-i', '--input', action = 'store', dest = 'input',
                        required = True, type = str,
                        help = "Full path to scpp pkl file.")
    
    parser.add_argument('-o', '--output', action = 'store', dest = 'output',
                        required = True, type = str,
                        help = 'Full path to root output directory.')
    
    parser.add_argument('-n', '--nitr', action = 'store', dest = 'n',
                        required = False, default = 100, type = int,
                        help = "Number of bids each agent will place")
    
    parser.add_argument('-ns', '--nsamples', action = 'store', dest = 'nsamples',
                        required = False, default = 1000, type = int,
                        help = 'Number of samples used to estimate expected surplus of each bid.')
    
    parser.add_argument('-njs','--njointsamples',action='store', dest='njs',
                        required = False, default = 1000, type = int,
                        help = 'Number of samples used for joint local bidders.')
    
    parser.add_argument('-nms','-nmargsamples',action='store',dest='nms',
                        required=False, default = 1000, type = int,
                        help = 'Number of samples used for marginal local bidders.')
    
    parser.add_argument('-v', '--vfile', action='store', dest = 'vfile',
                        required=False, default=None,
                        help = 'Valuation File')
    
    parser.add_argument('-l', '--lfile',action='store', dest='lfile',
                        required=False, default=None,
                        help = 'Lambda file.')
    
    args = parser.parse_args()
    
    localSearchDominance(nbids = args.n, n_samples = args.nsamples, 
                         rootDir = args.output, scppFile = args.input,
                         vfile = args.vfile, lfile = args.lfile,
                         njs=args.njs, nms=args.nms)
    
if __name__ == "__main__":
    main()