#!/bin/bash

export CUDA_VISIBLE_DEVICES="0"
export OMPI_ALLOW_RUN_AS_ROOT=1

export NP_NUM=$1
export GPU_NUM=$2
export LMP_BIN=$3
export INFILE=$4
export LOGFILE_PATH=$5
export PYFILE=$6

echo NP_NUM is $NP_NUM
echo GPU_NUM is $GPU_NUM
echo LMP_BIN is $LMP_BIN
echo INFILE is $INFILE
echo LOGFILE is $LOGFILE
echo PYFILE is $PYFILE

LMPLOGFILE="lmp_equiliv.log"
PYLOGFILE="lmp_equiliv.log"

# mpirun --allow-run-as-root -np $NP_NUM $LMP_BIN -sf gpu -pk gpu $GPU_NUM -in $INFILE |& tee $LOGFILE_PATH
mpirun --allow-run-as-root -np $NP_NUM $LMP_BIN -sf gpu -pk gpu $GPU_NUM -in $INFILE > $LOGFILE_PATH

python $PYFILE 'equiliv' >> $LOGFILE_PATH
