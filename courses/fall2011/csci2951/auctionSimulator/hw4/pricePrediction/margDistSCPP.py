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
    def __init__(self, margDistData = None):
        """
        marginalDistributionPrediction should be a list of size m of tuples
        each tuple specifies a normalized histogram count and bin edges
        """          
        # initialize as empty
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
    
    
    def expectedPrices(self):
        """
        Calculate the expected price vector using the center bin avg method
        """
        e = []
        for hist, binEdges in self.data:
            e.append(self.centerBinAvg(hist,binEdges))
            
        return numpy.atleast_1d(e)
    
    @staticmethod
    def centerBinAvg(hist = None, binEdges = None):
        """
        A helper function for computing averages with a histogram
        take the value of a histogram bin to be equal to its center than 
        calculate the average as avg = \sum_i^n binCenter*prob(binCenter)
        
        Note:
            The histograms must be properly normalized.
        """
        
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
    
    def iTsample(self,nSamples = None):
        """
        Function to sample independently from marginal distributions
        """
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
    
    def graphPdf(self,args={}):
        """
        Function to plot the data using matplot lib
        """
        if 'colorStyles' in args:
            numpy.testing.assert_(len(args['colorStyles']), len(self.data))
            colorStyles = args['colorStyles']
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
            
        if 'xlabel' in args:
            plt.xlabel(args['xlabel'])
        else:
            plt.xlabel('Prices')
            
        if 'ylabel' in args:
            plt.ylabel(args['ylabel'])
        else:
            plt.ylabel('Probability')
        
        if 'title' in args:
            plt.title(args['title'])
        else:
            plt.title('Price Distribution')
            
        plt.legend()
        
        plt.show()
        
    def graphCdf(self,args={}):
        if 'colorStyles' in args:
            numpy.testing.assert_(len(args['colorStyles']), len(self.data))
            colorStyles = args['colorStyles']
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
            
        if 'xlabel' in args:
            plt.xlabel(args['xlabel'])
        else:
            plt.xlabel('Prices')
            
        if 'ylabel' in args:
            plt.ylabel(args['ylabel'])
        else:
            plt.ylabel('Probability')
        
        if 'title' in args:
            plt.title(args['title'])
        else:
            plt.title('Price Distribution')
            
        plt.legend()
        
        plt.show()
            
            
            
        
        
        
                
    
        
    
                