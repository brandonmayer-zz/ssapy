import argparse
import numpy
import os

from ssapy.strategies.downHillSimplex import downHillSS

from ssapy import listBundles, msListRevenue, msDictRevenue
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
    
    parser.add_argument('-es','--evalSamples',dest='evalFile',
                        required=True,type=str,
                        help='Evaluation samples file.')
    
    parser.add_argument('-ib','--initBidFile',dest='initBidFile',
                        required=True,type=str,
                        help='Initial Bids txt file.')
    
    parser.add_argument('-o','--odir',dest='odir',
                        required=True,type=str,
                        help='Output directory.')
    
    parser.add_argument('-mcs','--maxCandidateSamples', dest='maxCandidateSamples',
                        required=False, default=-1, type=int,
                        help='Limit the number of samples used as candidates.')
    
    parser.add_argument('-mes','--maxEvalSamples',dest='maxEvalSamples',
                        required=False, default=-1,type=int,
                        help='Limit the number of evaluation samples used.')
    
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
    
    numSamples = jointSamples.shape[0]
    m = jointSamples.shape[1]
    
    if args.maxCandidateSamples > 0:
        if args.maxCandidateSamples < jointSamples.shape[0]:
            test = jointSamples[:args.maxCandidateSamples,:]
               
    print jointSamples.shape    
    bids = numpy.zeros(vmat.shape)
    es   = numpy.zeros(vmat.shape[0])
    
    for itr, initBid, v, l in zip(xrange(vmat.shape[0]),initBids,vmat,lmat):
        print 'iteration {0}'.format(itr)
        bundleRevenueDict = msDictRevenue(v,l)
        
        bid = downHillSS(bundleRevenueDict,
                         initBid = initBid,
                         evalSamples = jointSamples,
                         ret = 1) 
        
        print '\t bid = {0}'.format(bid)
            
            
        bids[itr,:] = bid
        es[itr] = expectedSurplus_(bundleRevenueDict, bid, evalSamples)
        
    numpy.savetxt(os.path.join(args.odir,'downHillBids.txt'), bids)
    numpy.savetxt(os.path.join(args.odir,'downHillExpectedSurplus.txt'),es)
    
    with open(os.path.join(args.odir,'downHillStats.txt'),'w') as f:
        print >> f, numpy.mean(es)
        print >> f, numpy.var(es)


if __name__ == "__main__":
    main()