#!/usr/bin/env python
import argparse
import pickle
import os

import numpy
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


from ssapy.pricePrediction.jointGMM import jointGMM

def main():
    """
    Script to compute the normalized sample correlation matrix for a given joint GMM.
    """
    desc = "Computes Normalized Sample Correlation Matrix given a joint mixture of Gaussians"
    
    parser = argparse.ArgumentParser(description = desc)
    
    parser.add_argument('-i', '--input', action = 'store', dest = 'input', required = True,
                        help = "Must specify an input .pkl file.")
    
    parser.add_argument('-n', '--n_samples', action = 'store', dest = 'n_samples',
                        default = 10000, required = False, type=int,
                        help = "Number of samples used to estimate normalized correlation matrix.")
    
    parser.add_argument('-o', '--output', action = 'store', dest = 'output',
                        default = None, required = False, type = str,
                        help = "Name of file to save visualized correlation matrix.")
    
    args = parser.parse_args()
    
    with open(args.input,'r') as f:
        scpp = pickle.load(f)
        
    if not isinstance(scpp,jointGMM):
        raise ValueError("Must specify jointGMM instance.")
    
    corr = scpp.sampleNormalizedCorrelation(args.n_samples)
    
    opdf = 'out.pdf'
    otxt = 'out.txt'
    
    if not args.output == None:
        d,basename=os.path.split(args.output)
        fname = os.path.splitext(basename)[0]
        opdf = os.path.join(d,'norm_corr_' + fname + '.pdf')
        otxt = os.path.join(d,'norm_corr_' + fname + '.txt')
        
        print 'opdf = {0}'.format(opdf)
        print 'otxt = {0}'.format(otxt)
    else:
        filename = os.path.basename(args.input).split('.')[0]
        basepath = os.path.dirname(args.input)
        opdf = os.path.join(basepath, filename + '_norm_corr.pdf')
        otxt = os.path.join(basepath, filename + '_norm_corr.txt')
        
        
    plt.matshow(corr)
    plt.title('Normalized Correlation Matrix')
    plt.colorbar()
    plt.savefig(opdf)
    
    with open(otxt,'w') as f:
        numpy.savetxt(f,corr)
        
    print corr
    
if __name__ == "__main__":
    main()