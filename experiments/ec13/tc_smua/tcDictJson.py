import numpy
import os
import glob
import json

def main():
    
    rootDir = os.path.realpath(".")
    
    tcFiles = glob.glob(os.path.join(rootDir, "tc_*.txt"))

    tableFile = os.path.join(rootDir,'table.tex')
    if os.path.exists(tableFile):
        os.remove(tableFile)
    
    tcDict = {}
    for fyle in tcFiles:
        h,t = os.path.split(fyle)
        base,ext = os.path.splitext(t)
        base = base.split('_')
        m = int(base[5])
        n = int(base[6])
        
        if base[15] != 'None':
            l = int(base[15])
        else:
            l = base[15]
        
        with open(fyle,'r') as f:
            lynes = f.readlines()
            
        tc_mean = lynes[1].strip()
        tc_var  = lynes[2].strip()
        
        
        tcDict["{0}_{1}_{2}".format(m,n,l)] = [float(tc_mean),float(tc_var)]
        
    tcFile = os.path.join(rootDir,'tcDict.json')
    
    with open(tcFile,'w+') as f:
        json.dump(tcDict,f)
    
#    print tcDict
        
            

if __name__ == "__main__":
    main()