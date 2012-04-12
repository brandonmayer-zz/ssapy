
import numpy
import subprocess


def main():
    
    desc = 'Eval the efficatcy of SCPP with multiple runs with different params'
    
    parser.add_argument( '--aType',    action = 'store', dest = 'aType', required = True)
    parser.add_argument( '--oDir',     action = 'store', dest = 'oDir',  required = True)
    parser.add_argument( '--scppType', action = 'store', dest = 'sccpType', required = True)
    
    parser.add_argument( '--m',       action = 'store', dest = 'm',       default = 5,     type = int)
    parser.add_argument( '--pmin',    action = 'store', dest = 'pmin',    default = 0,     type = float)
    parser.add_argument( '--pmax',    action = 'store', dest = 'pmax' ,   default = 50,    type = float)
    parser.add_argument( '--nAgents', action = 'store', dest = 'nAgents', default = 8,     type = int)
    
    parser.add_argument( '--nEval',   action = 'store', dest = 'nEval',   default = 10000, type = int)
    
    #the min and max tolerance, we will use linspace(tmin,tmax) as our values to loop
    parser.add_argument( '--tmin',    action = 'store', dest = 'tmin',    default = 0.1,   type = float)
    parser.add_argument( '--tmax',    action = 'store', dest = 'tmax',    default = 0.001, type = float)
    
    parser.add_argument( '--plot',     action = 'store', dest = 'plot',     default = True, type = bool)
    parser.add_argument( '--verbose',  action = 'store', dest = 'verbose',  default = True, type = bool)
    parser.add_argument( '--writeTxt', action = 'store', dest = 'writeTxt', default = True, type = bool)
    
    
    #Bayes Specific Arguments
    #maximum number of bayesian samples
    parser.add_argument( '--maxBg',   action = 'store', dest = 'maxSim',   default = 1000000)
    parser.add_argument( '--convStep', action = 'store',  dest = 'convStep', default = 100)
    
    bayesExe = os.path.realpath('./bSCPP.py')
    ywExe    = os.path.realpath('./symDistSCPP')
    
    table = []
    table.append([])
    
    pass

if __name__ == '__main__':
    main()