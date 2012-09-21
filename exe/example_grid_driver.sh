#!/bin/bash

qsub -l short -V -cwd ~/bmProjects/exe/bayesSCPPexe.sh --oDir ~/testBayesSCPP --agentType straightMU8 --nGames 100 --tol 0.001
