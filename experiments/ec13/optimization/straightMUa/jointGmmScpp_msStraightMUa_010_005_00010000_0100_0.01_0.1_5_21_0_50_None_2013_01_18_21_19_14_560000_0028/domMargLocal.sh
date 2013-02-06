#!/bin/bash

inputDir=$(ls -d jointGmmScpp_*)

rootDir=$(pwd)

echo $rootDir



margLocalScript=$(which domMargLocal.sh)
echo "margLocalScript = " ${margLocalScript}

# qout=${rootDir}/qout
# rm -rf ${qout}
# mkdir ${qout}

d=${rootDir}


indepSamples=${d}/indepSamples.txt
echo "indepSamples = " ${indepSamples}

initBids=${d}/initBids.txt
echo "initBids = " ${initBids}

v=${d}/v.txt
echo "v = " ${v}

l=${d}/l.txt
echo "l = " ${l}

evalSamples=${d}/evalSamples.txt
echo "evalSamples = " ${evalSamples}

qsub -l short -V -cwd -m abe -M b.mayer1@gmail.com \
    ${margLocalScript} -s ${indepSamples} -ib ${initBids} -es ${evalSamples} \
    -v ${v} -l ${l} -o ${d}

# for basename in $inputDir
# do
#     d=${rootDir}/${basename}
#     echo ${d}

#     jointSamples=${d}/jointSamples.txt
#     echo "jointSamples = " ${jointSamples}

    

    

    

    # qsub -l long -V -cwd -m abe -M b.mayer1@gmail.com -o ${qout} \
    # 	${jointLocalScript} -s ${jointSamples} -ib ${initBids} -es ${evalSamples} \
    # 	-v ${v} -l ${l} -o ${d}



    # qsub -l long -V -cwd -m abe -M b.mayer1@gmail.com -o ${qout} \
    # 	${condLocalScript} -s ${jointSamples} -ib ${initBids} -es ${evalSamples} \
    # 	-v ${v} -l ${l} -o ${d}

    # qsub -l short -V -cwd -m abe -M b.mayer1@gmail.com -o ${qout} \
    # 	${condLocalZeroScript} -s ${jointSamples} -ib ${initBids} -es ${evalSamples} \
    # 	-v ${v} -l ${l} -o ${d}

    # qsub -l long -V -cwd -m abe -M b.mayer1@gmail.com -o ${qout} \
    # 	${condMVLocalScript} -s ${jointSamples} -ib ${initBids} -es ${evalSamples} \
    # 	-v ${v} -l ${l} -o ${d}

    # qsub -l long -V -cwd -m abe -M b.mayer1@gmail.com -o ${qout} \
    # 	${condLocalLimitScript} -s ${jointSamples} -ib ${initBids} -es ${evalSamples} \
    # 	-v ${v} -l ${l} -o ${d}
# done
