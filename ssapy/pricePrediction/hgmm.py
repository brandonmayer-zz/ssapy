import numpy
import sklearn.mixture
from scipy.stats import norm

import matplotlib.pyplot as plt

from .jointGMM import jointGMM

import time

class hgmm(jointGMM):
    def __init__(self,**kwargs):
        self.p0 = numpy.float(0.0)
        
        super(hgmm,self).__init__(**kwargs)
        
    def sample(self, **kwargs):
        minPrice = kwargs.get('minPrice', self.minPrice)
        maxPrice = kwargs.get('maxPrice', self.maxPrice)
        
        n_samples = kwargs.get('n_samples',1)
        
        random_state = kwargs.get('random_state',self.random_state)
        
        sampleFncPtr = super(jointGMM,self).sample
        
        samples = numpy.zeros((n_samples, self.means_.shape[1]))
        
        m = self.m()
        idx = 0
        while idx < n_samples:
            
            #flip a coin and choose all zeros or from 
            #non-zero price distribution
            if numpy.random.binomial(self.p0):
                samples[idx,:] = numpy.zeros(m)
                idx += 1
            else:
                s = sampleFncPtr(1,random_state)[0]
                if ~numpy.any(s > maxPrice) and ~numpy.any(s < minPrice):
                    samples[idx,:]=s
                    idx += 1
            
        return samples
    
    def aicFit(self, **kwargs):
        X               = kwargs.get('X')
        compRange       = kwargs.get('compRange',numpy.arange(1,6))
        
        #accept new mixture model params as arguments
        #and store on instance
        covariance_type = kwargs.get('covariance_type', 'full')
        random_state    = kwargs.get('random_state' , self.random_state)
        thresh          = kwargs.get('thresh', self.thresh)
        min_covar       = kwargs.get('min_covar', self.min_covar)
        n_iter          = kwargs.get('n_itr', self.n_iter)
        n_init          = kwargs.get('n_init', self.n_init)
        params          = kwargs.get('params',self.params)
        init_params     = kwargs.get('init_params',self.init_params)
    
        verbose         = kwargs.get('verbose',True)
        
        if verbose:
            print 'starting aicFit(...)'
            print 'compRange = {0}'.format(compRange)
            print 'minCovar  = {0}'.format(min_covar)
            start = time.time()
            
        clfList = [sklearn.mixture.GMM(n_components    = c, 
                                       covariance_type = covariance_type,
                                       random_state    = random_state,
                                       min_covar       = min_covar,
                                       thresh          = thresh,
                                       n_iter          = n_iter,
                                       n_init          = n_init,
                                       params          = params,
                                       init_params     = init_params)\
                                       for c in compRange] 
                                       
        
        [clf.fit(X) for clf in clfList]
        
        aicList = [clf.aic(X) for clf in clfList]
        
        argMinAic = numpy.argmin(aicList)
        
        # set the data of this class associated with the 
        # derived class to match the fitted distribution
        self.__dict__.update(clfList[argMinAic].__dict__)
        
        #not all versions of scikit store this so explicitly set it
        self.covariance_type = covariance_type
        
        if verbose:
            print 'Finished aicFit(...) in {0} seconds'.format(time.time()-start)
            print 'Minimum AIC = {0}'.format(aicList[argMinAic])
            print 'Number of components = {0}'.format(compRange[argMinAic])
                
        return clfList[argMinAic], aicList, compRange
