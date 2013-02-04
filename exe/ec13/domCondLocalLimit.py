import argparse
import numpy
import os

from ssapy.strategies.condLocal import condLocalLimit

from ssapy import listBundles, msListRevenue
from ssapy.pricePrediction.jointGMM import expectedSurplus_

def main():
    desc="Compute jointLocal bids given v's, l's initial bids and parameters"
    
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument('-s','--samplesFile',dest='samplesFile',
                        required=True,type=str,
                        help='Samples (text file)')
    
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
    
    args = parser.parse_args()
    
    args.odir = os.path.realpath(args.odir)
    
    jointSamples = numpy.loadtxt(os.path.realpath(args.samplesFile))
    initBids     = numpy.loadtxt(os.path.realpath(args.initBidFile))
    vmat         = numpy.loadtxt(os.path.realpath(args.vfile))
    lmat         = numpy.loadtxt(os.path.realpath(args.lfile))
    evalSamples  = numpy.loadtxt(os.path.realpath(args.evalFile))
    
    m = initBids.shape[1]
    
    bundles = listBundles(m)
    
    bids = numpy.zeros(initBids.shape)
    es   = numpy.zeros(initBids.shape[0])
    
    for itr, initBid, v, l in zip(xrange(vmat.shape[0]),initBids,vmat,lmat):
        print 'iteration {0}'.format(itr)
        revenue = msListRevenue(bundles,v,l)
        
        bids[itr,:] = \
            condLocalLimit(bundles,revenue,initBid,jointSamples,
                        args.maxitr,args.tol,args.verbose,'bids')
        
        brd = {}
        for b,r in zip(bundles,revenue):
            brd[tuple(b)] = r
        
        es[itr] = expectedSurplus_(brd, bids[itr,:], evalSamples)
        
    numpy.savetxt(os.path.join(args.odir,'condMVLocalBids.txt'), bids)
    numpy.savetxt(os.path.join(args.odir,'condMVLocalExpectedSurplus.txt'),es)
    
    with open(os.path.join(args.odir,'condMVLocalStats.txt'),'w') as f:
        print >> f, numpy.mean(es)
        print >> f, numpy.var(es)


if __name__ == "__main__":
    main()