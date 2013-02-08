import argparse
import numpy
import os

from ssapy.strategies.margLocal import margLocalMc

from ssapy import listBundles, msListRevenue, msDictRevenue
from ssapy.pricePrediction.jointGMM import expectedSurplus_

def main():
    desc="Compute jointLocal bids given v's, l's initial bids and parameters"
    
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument('-s','--samplesFile',dest='samplesFile',
                        required=True,type=str,
                        help='Samples (text file)')
    
    parser.add_argument('-ms','--maxBidSamples',dest='maxBidSamples',
                        required=False,type=int, default=-1,
                        help='Maximum samples used to compute bids.')
    
    parser.add_argument('-v','--vfile',dest='vfile',
                        required=True,type=str,
                        help='Valuation v vector txt file.')
    
    parser.add_argument('-l','--lfile',dest='lfile',
                        required=True,type=str,
                        help='Valuation lambda txt file.')
    
    parser.add_argument('-ib','--initBidFile',dest='initBidFile',
                        required=True,type=str,
                        help='Initial Bids txt file.')
    
    parser.add_argument('-es','--evalSamples',dest='evalFile',
                        required=True,type=str,
                        help='Evaluation samples file.')
    
    parser.add_argument('-o','--odir',dest='odir',
                        required=True,type=str,
                        help='Output directory.')
        
    parser.add_argument('-mi','--maxitr', dest='maxitr',
                        required=False, default=100, type=int,
                        help='Maximum Update Iterations')
    
    parser.add_argument('-t','--tol',dest='tol',
                        required=False, default=1e-5,
                        type=float,help='L2 Update Stopping Tolerance')
    
    parser.add_argument('--verbose',dest='verbose',
                        required=False,default=False,
                        type=bool,help='Output debugg information')
    
    parser.add_argument('-n','--name',dest='name',
                        required=False, default='margLocalMc',
                        type=str,help='Output filename.')
    
    args = parser.parse_args()
    
    args.odir = os.path.realpath(args.odir)
    
    samples = numpy.loadtxt(os.path.realpath(args.samplesFile))
    initBids     = numpy.loadtxt(os.path.realpath(args.initBidFile))
    vmat         = numpy.loadtxt(os.path.realpath(args.vfile))
    lmat         = numpy.loadtxt(os.path.realpath(args.lfile))
    evalSamples  = numpy.loadtxt(os.path.realpath(args.evalFile))
    
    m = initBids.shape[1]
    
#    bundles = listBundles(m)
    
    if samples.shape[0] > args.maxBidSamples:
        samples = samples[:args.maxBidSamples,:]
    
    bids = numpy.zeros(initBids.shape)
    es   = numpy.zeros(initBids.shape[0])
    
    bidsFile   = os.path.join(args.odir, args.name + 'Bids.txt')
    if os.path.exists(bidsFile):
        os.remove(bidsFile)
        
    esFile    = os.path.join(args.odir, args.name + 'ExpectedSurplus.txt')
    if os.path.exists(esFile):
        os.remove(esFile)
        
    statsFile = os.path.join(args.odir, args.name + 'Stats.txt')
    if os.path.exists(statsFile):
        os.remove(statsFile)
    
    for itr, initBid, v, l in zip(xrange(vmat.shape[0]),initBids,vmat,lmat):
        print 'iteration {0}'.format(itr)
        brd = msDictRevenue(v,l)
        
        bids[itr,:], converged, nitr, d = \
            margLocalMc(brd,
                        initBid,samples,
                        maxItr = args.maxitr,
                        tol = args.tol,
                        verbose = args.verbose,
                        ret = 'all')
                             
        es[itr] = expectedSurplus_(brd, bids[itr,:], evalSamples)
        
        with open(bidsFile,'a+') as f:
            numpy.savetxt(f, bids[itr,:][None])
            
        with open(esFile,'a+') as f:
            numpy.savetxt(f,es[itr][None])
#            numpy.savetxt(f,es[itr])
        
        print '\t bid              = {0}'.format(bids[itr,:])
        print '\t converged        = {0}'.format(converged)
        print '\t nItr             = {0}'.format(nitr)
        print '\t d                = {0}'.format(d)
        print '\t Expected Surplus = {0}'.format(es[itr])
        
#    numpy.savetxt(os.path.join(args.odir, args.name +'Bids.txt'), bids)
#    numpy.savetxt(os.path.join(args.odir, args.name +'ExpectedSurplus.txt'),es)
    
    with open(os.path.join(args.odir,args.name + 'Stats.txt'),'w') as f:
        print >> f, numpy.mean(es)
        print >> f, numpy.var(es)
        
    print numpy.mean(es)
    print numpy.var(es)

if __name__ == "__main__":
    main()