from aucSim.agents.straightMU import *
from aucSim.agents.targetMU import *
from aucSim.agents.targetMUS import *
from aucSim.agents.targetPriceDist import *
from aucSim.agents.riskAware import *

from aucSim.pricePrediction.hist import *
from aucSim.pricePrediction.util import *

import numpy
import matplotlib.pyplot as plt
import subprocess
import argparse
import glob
import shutil
import multiprocessing

class Consumer(multiprocessing.Process):
    def __init__(self, task_q, result_q = None):
        multiprocessing.Process.__init__(self)
        self.task_q   = task_q
        self.result_q = result_q
        
    def run(self):
        while True:
            next_task = self.task_q.get()
            
            if next_task is None:
                print '{0}: Exiting'.format(self.name)
                self.task_q.task_done()
                break
            print '{0} - running task: '.format(self.name, next_task.__str__())
            
            if self.result_q != None:
                self.result_q.put(next_task())
            else:
                next_task()
            self.task_q.task_done()
            
        return
    
class evalTask(object):
    def __init__(self, **kwargs):
        #required
        self.args = kwargs
        self.scppType = kwargs.get('scppType')
        self.aType    = kwargs.get('aType')
        self.tol      = kwargs.get('tol')
        self.oDir     = kwargs.get('oDir')
        
        self.nEval    = kwargs.get('nEval', 100000)
        self.nAgents  = kwargs.get('nAgnets', 8)
        self.pmin     = kwargs.get('pmin', 0)
        self.pmax     = kwargs.get('pmax', 50)
        
        self.nEval    = kwargs.get('nEval', 100000)
        
        #bayes specific
        self.bSCPPpy  = kwargs.get( 'bSCPPpy', os.path.realpath('./bSCPP.py') )
        self.maxSim   = kwargs.get('maxSim' , 1000000)
        self.convStep = kwargs.get('convStep', 100)
        
        
        
        
    def __call__(self):
        try:
            print
            if self.scppType == 'bayes':
                print 'scppType = bayes'
                
                k = subprocess.Popen([sys.executable, self.bSCPPpy, '--aType', '{0}'.format(self.aType),
                                      '--oDir', '{0}'.format(self.oDir), '--tol', '{0}'.format(self.tol),
                                      '--maxSim', '{0}'.format(self.maxSim), '--minPrice', '{0}'.format(self.pmin),
                                      '--maxPrice', '{0}'.format(self.pmax), '--convStep', '{0}'.format(self.convStep)],
                                      '--nAgents', '{0}'.formaT(self.nAgents))
                
                print 'Waiting'
                
#                try: 
                k.wait()
                
 
                
                
#                finally:
                print 'Done Waiting'
                
                iFile = os.path.join(self.oDir,'output.txt')
                kl = None
                with open(iFile, 'r') as f:
                    lines = f.readlines()
                    kl = lines[-1].split()[-1]
                    
                pkl = glob.glob(os.path.join(self.oDir, '/*.pkl'))

                return (self.convStep, self.tol, kl, pkl, self.aTyp, self.nAgents, self.pmin, self.pmax)
            else:
                raise valueError
                
        except:
            print '---------------------'
            print 'UNKNOWN ERROR'
            raise
            
    def __str__(self):
        s = 'Running - tol = {0}\nscppType = {1}\naType = {2}\noDir = {3}'.format(self.tol,self.scppType,self.aType,self.oDir)
        

def main():
    
    desc = 'Eval the efficatcy of SCPP with multiple runs with different params'
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument( '--aType',    action = 'store', dest = 'aType', required = True)
    parser.add_argument( '--oDir',     action = 'store', dest = 'oDir',  required = True)
    parser.add_argument( '--scppType', action = 'store', dest = 'scppType', required = True)
    
    parser.add_argument( '--m',       action = 'store', dest = 'm',       default = 5,     type = int)
    parser.add_argument( '--pmin',    action = 'store', dest = 'pmin',    default = 0,     type = float)
    parser.add_argument( '--pmax',    action = 'store', dest = 'pmax' ,   default = 50,    type = float)
    parser.add_argument( '--nAgents', action = 'store', dest = 'nAgents', default = 8,     type = int)
    
    parser.add_argument( '--nEval',   action = 'store', dest = 'nEval',   default = 10000, type = int)
        
    #the min and max tolerance, we will use linspace(tmin,tmax) as our values to loop
    parser.add_argument( '--tmin',    action = 'store', dest = 'tmin',    default = 0.1,   type = float)
    parser.add_argument( '--tmax',    action = 'store', dest = 'tmax',    default = 0.01,  type = float)
    parser.add_argument( '--tnum',    action = 'store', dest = 'tnum',    default = 5,     type = float)
    
    parser.add_argument( '--csMin',   action = 'store', dest = 'csMin',   default = 100,   type = int)
    parser.add_argument( '--csMax',   action = 'store', dest = 'csMax',   default = 1000,  type = int)
    parser.add_argument( '--csDelta', action = 'store', dest = 'csDelta', default = 5,    type = int)
    
    parser.add_argument( '--plot',     action = 'store', dest = 'plot',     default = True, type = bool)
    parser.add_argument( '--verbose',  action = 'store', dest = 'verbose',  default = True, type = bool)
    parser.add_argument( '--writeTxt', action = 'store', dest = 'writeTxt', default = True, type = bool)
    parser.add_argument( '--nProc',    action = 'store', dest = 'nProc',    default = multiprocessing.cpu_count() - 1, type = int)
    
    
    #Bayes Specific Arguments
    #maximum number of bayesian samples
    parser.add_argument( '--maxSim',   action = 'store',   dest = 'maxSim',   default = 1000000, type = int)
    #parser.add_argument( '--convStep', action = 'store',   dest = 'convStep', default = 100,     type = int )
    
    args = parser.parse_args().__dict__
    
    bayesExe = os.path.realpath('./bSCPP.py')
    ywExe    = os.path.realpath('./symDistSCPP')
    tlist = numpy.linspace(args['tmin'], args['tmax'], args['tnum'])
    
    cslist = None
    if args['csMin'] == args['csMax']:
        cslist = numpy.atleast_1d(args['csMin'])
    else:
        cslist = numpy.linspace(args['csMin'], args['csMax'], args['csDelta']).astype(int)
    
    nProc = args['nProc']
    if len(tlist)*len(cslist) < nProc:
        nProc = len(tlist)
    
    
    table = []
    table.append(['aType',      '{0}'.format(args['aType'])])
    table.append(['oDir',       '{0}'.format(args['oDir'])])
    table.append(['sccpType',   '{0}'.format(args['scppType'])])
    table.append(['nEval',      '{0}'.format(args['nEval'])])
    
    table.append(['tmin',       '{0}'.format(args['tmin'])])
    table.append(['tmax',       '{0}'.format(args['tmax'])])
    table.append(['tnum',       '{0}'.format(args['tnum'])])
    table.append(['tlist',      '{0}'.format(tlist)])
    
    table.append(['csMin',      '{0}'.format(args['csMin'])])
    table.append(['csMax',      '{0}'.format(args['csMax'])])
    table.append(['csDelta',    '{0}'.format(args['csDelta'])])
    table.append(['csList',     '{0}'.format(cslist)])
    
    table.append(['nEvals',     '{0}'.format(len(cslist)*len(tlist))])
    table.append(['m',          '{0}'.format(args['m'])])
    table.append(['pmin',       '{0}'.format(args['pmin'])])
    table.append(['pmax',       '{0}'.format(args['pmax'])])
    table.append(['plot',       '{0}'.format(args['plot'])])
    table.append(['maxSim',     '{0}'.format(args['maxSim'])])
    table.append(['nProc',      '{0}'.format(nProc)])
    table.append(['verbose',    '{0}'.format(args['verbose'])])
    table.append(['writeTxt',   '{0}'.format(args['writeTxt'])])
    
    if args['verbose']:
        ppt(sys.stdout, table)
    
    if not os.path.exists(os.path.realpath(args['oDir'])):       
        os.makedirs(os.path.realpath(args['oDir']))
        
    fout = os.path.realpath(os.path.join(args['oDir'],'evalOut.txt'))
    with open(fout,'w') as of:
        ppt(of,table)
        
    del fout
        
    tasks   = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
        
    consumers = [Consumer(tasks,results) for i in xrange(nProc)] 
    
    for w in consumers:
        w.start()
        
    try:
        if args['scppType'] == 'bayes':
            idx = 0
            for cs in  cslist:
                for tol in tlist:
                    oDir = os.path.realpath(os.path.join(args['oDir'],'task_{0}'.format(idx)))   
                    if not os.path.exists(oDir):
                        os.makedirs(oDir) 
                    
                    tasks.put( evalTask( scppType = 'bayes',
                                         aType    = args['aType'],
                                         oDir     = oDir,
                                         tol      = tol,
                                         convStep = cs,
                                         maxSim   = args['maxSim'],
                                         pmin     = args['pmin'],
                                         pmax     = args['pmax'],
                                         nEval    = args['nEval']  ) )
                    idx += 1 
                
            for i in xrange(nProc):
                tasks.put(None)
                
            tasks.join()
            
            if args['verbose']:
                print
                print 'TASKS DONE!!'
                print
            
            r = []
            d = {}
            while not results.empty():
                r = (results.get())
                if r[0] not in d:
                    d[r[0]] = numpy.atleast_1d((r[1],r[2]))
                else:
                    d[r[0]] = numpy.vstack( (d[r[0]],numpy.atleast_1d( (r[1],r[2]) )) )
                
                
#            r = sorted(r,key=lambda r:r[0])
#            r = numpy.atleast_2d(r)
                
            fig = plt.figure()
            ax = fig.add_subplot(111)
            colors = numpy.linspace(0,1,len(cslist))
            cm = plt.get_cmap('jet')
            pcount = 0
            for key,value in d.iteritems():
                value = numpy.atleast_2d(sorted(value,key=lambda v:v[0]))
                ax.plot(value[:,0],value[:,1],linestyle='dashed', marker='o', color=cm(colors[pcount]),label="convStep = {0}".format(key))
                pcount+=1
                
            ax.set_xlabel('Tolerance')
            ax.set_ylabel('KL Divergence')
            pout = os.path.realpath(os.path.join(args['oDir'],'fig.png'))
            plt.savefig(pout)
#            plt.show()
            
        else:
            print 'scppType: {0} Not Yet Implemented'.format(args['scppType'])
            
    except:
        print 'UNKNOWN ERROR'
        [w.terminate() for w in consumers]
        raise
      


if __name__ == '__main__':
    main()