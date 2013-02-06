import argparse
import numpy
import os

from ssapy.strategies.condLocal import condLocal
from ssapy.strategies.bidEval import bidEvalS

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
    
    parser.add_argument('-o','--odir',dest='odir',
                        required=True,type=str,
                        help='Output directory.')
    
    parser.add_argument('-mcs','--maxCandidateSamples', dest='maxCandidateSamples',
                        required=False, default=-1, type=int,
                        help='Limit the number of samples used as candidates.')
    
    parser.add_argument('--verbose',dest='verbose',
                        required=False,default=False,
                        type=bool,help='Output debugg information')
    
    
    
    args = parser.parse_args()
    
    args.odir = os.path.realpath(args.odir)
    
    jointSamples = numpy.loadtxt(os.path.realpath(args.samplesFile))

    vmat         = numpy.loadtxt(os.path.realpath(args.vfile))
    lmat         = numpy.loadtxt(os.path.realpath(args.lfile))
    evalSamples  = numpy.loadtxt(os.path.realpath(args.evalFile))
    
    numSamples = jointSamples.shape[0]
    m = jointSamples.shape[1]
    
    if args.maxCandidateSamples > 0:
        if args.maxCandidateSamples < jointSamples.shape[0]:
            jointSamples = jointSamples[:args.maxCandidateSamples,:]
        
    bids = numpy.zeros(m)
    es   = numpy.zeros(numSamples)
    
    for itr, v, l in zip(xrange(vmat.shape[0]),vmat,lmat):
        print 'iteration {0}'.format(itr)
        bundleRevenueDict = msDictRevenue(v,l)
        
        bids[itr,:],es[itr] = \
            bidEvalS(bundleRevenueDict,
                     jointSamples,
                     evalSamples,
                     ret = 'all')
        
    numpy.savetxt(os.path.join(args.odir,'bidEvalBids.txt'), bids)
    numpy.savetxt(os.path.join(args.odir,'bidEvalExpectedSurplus.txt'),es)
    
    with open(os.path.join(args.odir,'bidEvalStats.txt'),'w') as f:
        print >> f, numpy.mean(es)
        print >> f, numpy.var(es)


if __name__ == "__main__":
    main()