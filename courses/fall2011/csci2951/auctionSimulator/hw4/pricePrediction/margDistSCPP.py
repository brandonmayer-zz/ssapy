from pointSCPP import *
from types import * #for type checking
import matplotlib.pyplot as plt
import itertools

class margDistSCPP(pointSCPP):
    """
    Wrapper for marinal distribution self confirming price predictions.
    
     There should be one tuple per good, that is
        len(self.data) == self.m
        NOTE:
            If bins are [1,2,3,4] then the first bin
            contains all values within the range [1,2)
            (including 1 excluding 2), [2,3) and 
            [3,4] notice the last bin edge is inclusive
    
    savePickle and loadPickle are inherited from the pointSCPP class
    """
#    def __init__(self, margDistData = None):
    def __init__(self, **kwargs):
        """
        marginalDistributionPrediction should be a list of size m of tuples
        each tuple specifies a normalized histogram count and bin edges
        """          
        # initialize as empty
        margDistData = kwargs['margDistData']
        if margDistData == None:
            self.data = None
            self.m = None
        else:
            if self.validateData(margDistData=margDistData):
                self.data = margDistData
                if isinstance(margDistData,list):
                    self.m = len(margDistData)
                else:
                    self.m = 1
    
    @staticmethod
    def type():
        return "marginalDistributionSCPP"
    
    
    def expectedPrices(self,**kwargs):
        """
        Calculate the marginal expected price vector.
        
        By default will calculate the expected value as a sum of probabilities time
        bin centers
        
        iTsample will use the inverse transform sampling method to sample from the 
        distribution then the expected value will be computed as an average of these
        points
        
        Optional Inputs:
            kwargs['method'] = average or iTsample
            
            if kwargs['method'] == iTsample 
                the default number of samples is 8
            
            kwargs['nSamples'] the number of samples to use
                if kwargs['method'] == iTsample
        """
        
        method = kwargs.get('method','average')
                        
        if method == 'average':
            e = []
            for hist, binEdges in self.data:
                e.append(self.centerBinAvg(hist     = hist,
                                           binEdges = binEdges))
                
            return numpy.atleast_1d(e)
        
        elif method == 'iTsample':
            
            nSamples = kwargs.get('nSamples',8)
                            
            samples = self.iTsample(nSamples=nSamples)
                
            #return the mean over marginal samples
            return numpy.mean(samples,0)
            
        else:
            print 'margDistSCPP.expectedPrices()'
            print 'Unknown method'
            raise AssertionError
    
    @staticmethod
    def centerBinAvg(**kwargs):
        """
        A helper function for computing averages with a histogram
        take the value of a histogram bin to be equal to its center than 
        calculate the average as avg = \sum_i^n binCenter*prob(binCenter)
        
        Note:
            The histograms must be properly normalized.
        """
        hist     = kwargs['hist']
        binEdges = kwargs['binEdges']
        
        assert isinstance(hist,numpy.ndarray) or isinstance(binEdges,numpy.ndarray),\
            "hist and binEdges must be of type numpy.ndarray"
            
        numpy.testing.assert_almost_equal( numpy.sum(hist*numpy.diff(binEdges),dtype=numpy.float), 
                                           numpy.float(1.0) )
        
        numpy.testing.assert_equal( binEdges.shape[0], (hist.shape[0]+1) )
    
        return numpy.dot(hist, .5*(binEdges[:-1]+binEdges[1:]))
        
    def setPricePrediction(self, margDistData):
        if self.validateData(margDistData):
            self.data = margDistData
            
            if isinstance(margDistData,list):
                self.m = len(margDistData)
            else:
                self.m = 1
                
    @staticmethod
    def validateData(margDistData = None):
        assert isinstance(margDistData, list) or\
                isinstance(margDistData, tuple),\
                "{1} is not a list or tuple".format(margDistData)
        
        if isinstance(margDistData,list):
                      
            for hist,binEdges in margDistData:
                assert isinstance(hist,numpy.ndarray) and\
                        isinstance(binEdges,numpy.ndarray),\
                            "hist and binEdges must be numpy arrays."               
            
                numpy.testing.assert_almost_equal( 
                    numpy.sum(hist*numpy.diff(binEdges),dtype=numpy.float), 
                    numpy.float(1.0),
                    err_msg = "Marginal Distribution Data must be a valid PDF." )
                
        elif isinstance(margDistData,tuple):
            numpy.testing.assert_almost_equal(
                    numpy.sum( margDistData[0]*numpy.diff(margDistData[1]),dtype=numpy.float),
                    numpy.float(1.0),
                    err_msg = "Marginal Distribution Data must be a valid PDF." ) 
                                               
        # if you made it here you are good to go
        return True
    
    def margUps(self,**kwargs):
        """
        Will be in units of prices
        """
        expectedPrices = kwargs['expectedPrices']
        return numpy.sqrt(self.margUpv(expectedPrices = expectedPrices))
    
    def margUpv(self,**kwargs):
        """
        Given a vector of marginal expected prices, computed either by sampling or
        arithmetically, calculate the upper partial 
        variance associated with each marginal distribution.
        
        will be in units of price**2
        """
        expectedPrices = kwargs['expectedPrices']
        
        numpy.testing.assert_(expectedPrices.shape[0] == len(self.data), 
                              msg = "expectedPrice.shape[0] = {0} != len(self.data) = {1}".\
                              format(expectedPrices.shape[0],len(self.data)))
        
        upv = []
        for idx in xrange(expectedPrices.shape[0]):
            #get the prices
            binEdges = numpy.atleast_1d(self.data[idx][1])
            
            #get all bin indicies with prices greated than marginal expected value
            upperPriceIndicies = numpy.nonzero(binEdges>expectedPrices[idx])[0]
            
            #convert from indicies to prices
            upperPrices = numpy.atleast_1d(binEdges[upperPriceIndicies[:-1]])
            
            #the probability associated with each upper price
            upperPriceProb = numpy.atleast_1d(self.data[idx][0][upperPriceIndicies[:-1]])
            
            upv.append( numpy.sum( ((upperPrices-expectedPrices[idx])**2)*upperPriceProb ) )
            
        return numpy.array(upv)
    
    def iTsample(self, **kwargs):
        """
        Function to sample independently from marginal distributions
        """
        nSamples = None
        if 'nSamples' not in kwargs:
            nSamples = 8
        else:
            nSamples = kwargs['nSamples']
            
        numpy.testing.assert_equal(isinstance(nSamples,int),
                                   True)
        m = len(self.data)
        
        samples = numpy.zeros( (nSamples,m) )
        
        for m in xrange(len(self.data)):
            #calculate the cdf
            hist,binEdges = self.data[m]
            cdf = numpy.cumsum(hist)
            
            #get some random numbers (0.0,1.0]
            randNumbers = numpy.random.random_sample(nSamples)
            
            for idx in xrange(randNumbers.shape[0]):
                binIdx = numpy.nonzero(cdf > randNumbers[idx])[0][0]
                samples[idx][m] = binEdges[binIdx]
                
        return samples
    
    def graphPdf(self,**kwargs):
        """
        Function to plot the data using matplot lib
        """
        if 'colorStyles' in kwargs:
            numpy.testing.assert_(len(kwargs['colorStyles']), len(self.data))
            colorStyles = kwargs['colorStyles']
        else:
            #pick some random styles
            colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
            lineStyles = ['-', '--', '-.', ':']
            markerStyles = ['o', 'v', '^', '<', '>', 's', 'p', '*', 'h', 'H', 'x', '+', 'D']
            colorStyles = [j[0] + j[1] for j in itertools.product(markerStyles,[i[0] + i[1] for i in itertools.product(colors,lineStyles)])]
            numpy.random.shuffle(colorStyles)
            colorStyles = colorStyles[:len(self.data)]
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        for i in xrange(len(self.data)):
            ax.plot(.5*(self.data[i][1][:-1]+self.data[i][1][1:]),self.data[i][0],colorStyles[i],label='Slot {0}'.format(i))
            
        if 'xlabel' in kwargs:
            plt.xlabel(kwargs['xlabel'])
        else:
            plt.xlabel('Prices')
            
        if 'ylabel' in kwargs:
            plt.ylabel(kwargs['ylabel'])
        else:
            plt.ylabel('Probability')
        
        if 'title' in kwargs:
            plt.title(kwargs['title'])
        else:
            plt.title('Price Distribution')
            
        plt.legend()
        
        plt.show()
        
    def graphCdf(self,**kwargs):
        if 'colorStyles' in kwargs:
            numpy.testing.assert_(len(kwargs['colorStyles']), len(self.data))
            colorStyles = kwargs['colorStyles']
        else:
            #pick some random styles
            colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
            lineStyles = ['-', '--', '-.', ':']
            markerStyles = ['o', 'v', '^', '<', '>', 's', 'p', '*', 'h', 'H', 'x', '+', 'D']
            colorStyles = [j[0] + j[1] for j in itertools.product(markerStyles,[i[0] + i[1] for i in itertools.product(colors,lineStyles)])]
            numpy.random.shuffle(colorStyles)
            colorStyles = colorStyles[:len(self.data)]
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        for i in xrange(len(self.data)):
            ax.plot(.5*(self.data[i][1][:-1]+self.data[i][1][1:]),numpy.cumsum(self.data[i][0]),colorStyles[i],label='Slot {0}'.format(i))
            
        if 'xlabel' in kwargs:
            plt.xlabel(kwargs['xlabel'])
        else:
            plt.xlabel('Prices')
            
        if 'ylabel' in kwargs:
            plt.ylabel(kwargs['ylabel'])
        else:
            plt.ylabel('Probability')
        
        if 'title' in kwargs:
            plt.title(kwargs['title'])
        else:
            plt.title('Price Distribution')
            
        plt.legend()
        
        plt.show()
            
            
            
        
        
        
                
    
        
    
                
                