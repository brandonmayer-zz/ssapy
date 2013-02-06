import numpy
import os
import glob

def main():
    
    rootDir = os.path.realpath(".")
    
    tcFiles = glob.glob(os.path.join(rootDir, "tc_*.txt"))

    tableFile = os.path.join(rootDir,'tcTable.tex')
    if os.path.exists(tableFile):
        os.remove(tableFile)
    
    table = []
    
    with open(tableFile,'a+') as f:
        print >> f, "\\begin{table}[ht!]"
        print >> f, "\\centering"
        print >> f, "\\begin{tabular}{|c|c|c|}"
        print >> f, "\\hline"
        print >> f, "Environment & Total Correlation Mean& Total Correlation Variance\\\\"
        print >> f, "\\hline"
        print >> f, "\\hline"
        
    for fyle in tcFiles:
        h,t = os.path.split(fyle)
        base,ext = os.path.splitext(t)
        base = base.split('_')
        m = base[5]
        n = base[6]
        l = base[15]
        
        with open(fyle,'r') as f:
            lynes = f.readlines()
            
        tc_mean = float(lynes[1].strip())
        tc_var  = float(lynes[2].strip())
        
        row = []
        if l == 'None':
            row.append("U[{0},{1}] &".format(int(m),int(n)))
#            row = ['U[{0},{1}] &'.format(m,n), tc_mean + '&', tc_var + '\\']
        else:
#            row = [r"\lambda_{1}[%s,%s] &'%(m,n)", '{0} &'.format(tc_mean), '{0} \\'.format(tc_var)]
            row.append("$\lambda_{1}$[%s,%s] &" % (int(m),int(n)))
            
        row.append('{0:.4}&'.format(tc_mean))
        row.append('{0:.4}\\\\'.format(tc_var))
            
#        print row
        
        with open(tableFile,'a+') as f:
#            print >> f, row
            f.write(''.join(row))
            f.write('\n')
            
    with open(tableFile,'a+') as f:
        print >> f, "\\hline"
        print >> f, "\\end{tabular}"
        print >> f, "\\end{table}"

if __name__ == "__main__":
    main()