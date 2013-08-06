import numpy
import sklearn.mixture

from scipy.stats import norm

#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

import itertools
import time

class igmm(object):
    """
    A wrapper to store independent mixtures for each dimension
    """
    def __init__(self, **kwargs):
        self.minPrice        = kwargs.get('minPrice',0)
        self.maxPrice        = kwargs.get('maxPrice',numpy.float('inf'))
        
        self.m = kwargs.get('m',None)
        
        self.gmmlist = None
        
        if self.m != None:
            self.gmmlist = [sklearn.mixture.GMM(n_components    = kwargs.get('n_components',1),
                                              covariance_type = kwargs.get('covariance_type','diag'),
                                              random_state    = kwargs.get('random_state',None),
                                              thresh           = kwargs.get('thresh', 1e-2),
                                              min_covar       = kwargs.get('min_covar',1e-3),
                                              n_iter          = kwargs.get('n_iter',100),
                                              n_init          = kwargs.get('n_init',1),
                                              params          = kwargs.get('params','wmc'),
                                              init_params     = kwargs.get('init_params','wmc')) for d in xrange(self.m)]
            
    def sample(self,**kwargs):
        minPrice = kwargs.get('minPrice', self.minPrice)
        maxPrice = kwargs.get('maxPrice', self.maxPrice)
        
        n_samples = kwargs.get('n_samples',1)
        
        if self.gmmlist == None:
            raise ValueError('self.gmmlist == None')
        
        samples = numpy.zeros((n_samples,self.m))
        
        for d in xrange(self.m):
            gmm = self.gmmlist[d]
            cnt = 0
            while cnt < n_samples:
                s = gmm.sample(1)
                if s > minPrice and s < maxPrice:
                    samples[cnt,d] = s
                    cnt += 1
                     
        return samples
    
    def d(self):
        return len(self.gmmlist)
    
    def expectedValue(self):
        ev = numpy.zeros(len(self.gmmlist))
        for d, gmm in enumerate(self.gmmlist):
            for m,w in zip(gmm.means_, gmm.weights_):
                ev[d] += m*w
                
        return ev
    
    def aicFit(self, X = None, compRange = numpy.arange(5,21), 
               min_covar = 0.1, n_iter = 100, n_init = 1, thresh = 0.01,
               verbose = True):
        
        if verbose:
            print 'starting aicFit(...)'
            print 'compRange = {0}'.format(compRange)
            print 'minCovar  = {0}'.format(min_covar)
            start = time.time()
            
        m = X.shape[1]
        
        minAicList = []
        nCompList = []
        for d in xrange(m):
            if verbose:
                print 'Fitting dimension {0}'.format(d)
            clfList = [sklearn.mixture.GMM(n_components    = c, 
                                           covariance_type = 'diag',
                                           min_covar       = min_covar,
                                           thresh          = thresh,
                                           n_iter          = n_iter,
                                           n_init          = n_init)\
                                           for c in compRange] 
                                       
            [clf.fit(X[:,d]) for clf in clfList]
            
            aicList = [clf.aic(X) for clf in clfList]
        
            argMinAic = numpy.argmin(aicList)
            
            minAicList.append(aicList[argMinAic])
            
            self.gmmlist[d] = clfList[argMinAic]
            
            nCompList.append(self.gmmlist[d].n_components)
            
        if verbose:
            end = time.time()
            print 'Finished aicFit(...) in {0} seconds'.format(end - start)
            print 'Number of Components in each dimension: {0}'.format(nCompList)
            
        return minAicList, nCompList
    
    def plt(self, ofile = None, minPrice = 0, maxPrice = 50, npts = 1000, colors = None, 
            title = 'Independen Gaussian Mixture', xlabel = 'q', ylabel = r'$p(q)$'):
        
        if not colors:
            cmap = plt.get_cmap('hsv')
            colorStyles = [cmap(i) for i in numpy.linspace(0,0.9,self.d())]
            colorCycle = itertools.cycle(colorStyles)
            
        xx = numpy.linspace(minPrice, maxPrice, npts)
        
        fig, ax = plt.subplots()
        
        for j, gmm in enumerate(self.gmmlist):
            ll,resp = numpy.exp(gmm.eval(xx))
            del resp
            p = numpy.exp(ll)
            ax.plot(xx,p,color=next(colorCycle),label='good {0}'.format(j))
            
        leg = ax.legend(loc = 'best',fancybox = True)
        leg.get_frame().set_alpha(0.5)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        if ofile is None:
            plt.show()
        else:
            plt.savefig(ofile)
            
        return ax
            
        
def main():
    import pickle
    from ssapy.pricePrediction.jointGMM import jointGMM 
    with open("C:/Users/bm/Dropbox/data/aamas13/normCorrelation/straightMU8/jointGmmScppHob_msStraightMU8_m_005_0005.pkl",'r') as f:
        jgmm = pickle.load(f)
        
    samples = jgmm.sample(n_samples=10000)
    
    idep = igmm()
    idep.aicFit(samples)
    
    idep.plt()
        
        
if __name__ == "__main__":
    main()
        
        
        
