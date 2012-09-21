#!/bin/bash

qsub -l short -V ~/bmProjects/exe/bayesSCPPexe.sh --oDir /home/bamayer/auctionExp/testBayesSCPP --agentType straightMU8 --nGames 100 
