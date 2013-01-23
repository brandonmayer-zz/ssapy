import argparse
import numpy
import os
import pickle
import sys
from ssapy import agentFactory

def msbid(ss, ppfile, vfile, lfile, agentArgs=None):
    vmat = numpy.loadtxt(vfile)
    lmat = numpy.loadtxt(lfile)
    
    ppfile = os.path.realpath(ppfile)
    
    with open(ppfile,'rb') as f:
        pricePrediction = pickle.load(f)
    
    agent = agentFactory(agentType = ss,m=vmat.shape[1])
    agent.pricePrediction = pricePrediction
    
    if agentArgs != None:
        agentArgsDict = {}
        for s in agentArgs.split(' '):
            k=s.split('=')[0]
            v=s.split('=')[1]
            agentArgsDict[k]=v
            
    for v, l in zip(vmat,lmat):
        agent.v = v
        agent.l = l
        
        if agentArgs == None:
            bid = agent.bid()
            numpy.savetxt(sys.stdout, bid.reshape(1,bid.shape[0]))
        else:
            print agent.bid(**agentArgsDict)
            
def main():
    """
    Executable to compute bids given revenue function, price prediction and 
    agent type. Prints to std out.
    """
    desc = "Computes bids give price prediction, revenue function and agent type."
    
    parser = argparse.ArgumentParser(description = desc)
    
    parser.add_argument('-i','--input', action='store', dest='input',required=True,
                        help = "Must specify input price prediction pkl file.")
    
    parser.add_argument('-a', '--agentType', action='store',
                        dest='ss',required=True,
                        help = "Must specify agent type.")
    
    parser.add_argument('-o','--output',action='store',dest='output',
                        default='.',required=False,type=str,
                        help='Output root directory')
    
    parser.add_argument('-v','--valuation',action='store',dest='vfile',
                        required=True, type=str,
                        help="Valuation Vector txt file.")
    
    parser.add_argument('-l', '--lambda', action='store', dest='lfile',
                        required=True, type=str,
                        help="Lambda txt file")
    
    parser.add_argument('-args','--agentArgs',action='store',dest='args',
                        default=None,required=False,type=str,
                        help='Additional Agent arguments key=value seperated by spaces.')
    
    args=parser.parse_args()
    
    msbid(args.ss, args.input, args.vfile,
          args.lfile, args.args)
    
    
if __name__ == "__main__":
    main()