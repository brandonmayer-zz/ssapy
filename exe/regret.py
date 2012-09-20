from auctionSimulator.hw4.auctions.simultaneousAuction import *
from auctionSimulator.parallelWorker import *
from auctionSimulator.hw4.agents.riskAware import *


import numpy
import time
import itertools
import multiprocessing
import os

def main():
    desc = 'Parallel Implementation of Regret computation from Yoon & Wellman 2011'
    
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--S', action ='store', dest='S', default=[])

if __name__ == "__main__":
    main()