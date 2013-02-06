import os
import glob
import json
import math

def main():
    root = os.path.realpath('.')
    
    subDirs = glob.glob('jointGmmScpp_*')
    
    with open(os.path.realpath('../../tc_smua/tcDict.json') ,'r') as f:
        tcDict = json.load(f)
    
    domTableFile = os.path.join(root,'dominanceTable.tex')
    
    with open(domTableFile,'w+') as f:
        print >> f, "\\begin{table}[ht!]"
        print >> f, "\\centering"
        print >> f, "\\begin{tabular}{|c|c|c|c|c|}"
        print >> f, "\\hline"
        print >> f, "Environment & TC& \local\ & \condMVLocal\ & \joint\ \\\\"
        print >> f, "\\hline"
        print >> f, "\\hline"
        
    for d in subDirs:
        subPath = os.path.join(root,d)
        
        params = d.split("_")
        
        m = int(params[2].strip())
        n = int(params[3].strip())
        l = params[12].strip()
        
        tc = tcDict.get("{0}_{1}_{2}".format(m,n,l))
        
        margLocalStatsFile = os.path.join(subPath,'margLocalBidsStats.txt')
        if os.path.exists(margLocalStatsFile):
            with open(margLocalStatsFile,'r') as f:
                margLocalStats = f.readlines()
                margLocalMean  = float(margLocalStats[0].strip())
                margLocalVar   = math.sqrt(float(margLocalStats[1].strip()))
        else:
            margLocalMean = 'N/A'
            margLocalVar  = 'N/A'
            
        jointLocalStatsFile = os.path.join(subPath, 'jointLocalStats.txt')
        if os.path.exists(jointLocalStatsFile):
            with open(jointLocalStatsFile,'r') as f:
                jointLocalStats = f.readlines()
                jointLocalMean  = float(jointLocalStats[0].strip())
                jointLocalVar   = math.sqrt(float(jointLocalStats[1].strip()))
        else:
            jointLocalMean = 'N/A'
            jointLocalVar  = 'N/A'
            
        condMVLocalStatsFile = os.path.join(subPath, 'condMVLocalStats.txt')
        if os.path.exists(condMVLocalStatsFile):
            with open(condMVLocalStatsFile,'r') as f:
                condMVLocalStats = f.readlines()
                condMVLocalMean = float(condMVLocalStats[0].strip())
                condMVLocalVar  = math.sqrt(float(condMVLocalStats[1].strip()))
        else:
            condMVLocalMean = 'N/A'
            condMVLocalVar  = 'N/A'
            
        if l == 'None':
            env = "U[{0},{1}]".format(m,n)
        else:
            env = "$\lambda_{%s}$[%s,%s]" %(l,m,n)
            
            
        if tc == None:
            tc = 'N/A'
        else:
            tc = tc[0]
        
        with open(domTableFile,'a') as f:
            print >> f, "{0}&{1:.3}&({2:.4}, {3:.4})&({4:.4}, {5:.4})&({6:.4}, {7:.4})\\\\".\
                format(env, tc, margLocalMean, margLocalVar,
                       condMVLocalMean, condMVLocalVar,
                       jointLocalMean, jointLocalVar)

        
    with open(domTableFile,'a') as f:
        print >> f, "\\hline"
        print >> f, "\\end{tabular}"
#        print >> f, "\\caption{(mean, std) of Expected Surplus for 10000 bids in each environment.}"
        print >> f, "\\end{table}"

if __name__ == "__main__":
    main()