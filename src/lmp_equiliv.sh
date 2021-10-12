#!/bin/bash

# export CUDA_VISIBLE_DEVICES="0"
# export OMPI_ALLOW_RUN_AS_ROOT=1

export NP_NUM=$1
export GPU_NUM=$2
export LMP_BIN=$3
export INFILE=$4
export LOGFILE_TMP_PATH=$5
# export PYFILE=$6
# export LOGFILE_PATH=$7

echo NP_NUM is $NP_NUM
echo GPU_NUM is $GPU_NUM
echo LMP_BIN is $LMP_BIN
echo INFILE is $INFILE
echo LOGFILE_TMP_PATH is $LOGFILE_TMP_PATH
echo PYFILE is $PYFILE
echo LOGFILE_PATH is $LOGFILE_PATH

mpirun --allow-run-as-root -np $NP_NUM $LMP_BIN -sf gpu -pk gpu $GPU_NUM -in $INFILE > $LOGFILE_TMP_PATH
