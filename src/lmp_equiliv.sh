#!/bin/bash

export CUDA_VISIBLE_DEVICES="0"
export OMPI_ALLOW_RUN_AS_ROOT=1


LMPLOGFILE="lmp_equiliv.log"
PYLOGFILE="lmp_equiliv.log"
 
if [ -e $LMPLOGFILE ]; then
  rm $LMPLOGFILE
fi

if [ -e $PYLOGFILE ]; then
  rm $PYLOGFILE
fi

mpirun --allow-run-as-root -np 2 /program/lammps201029/build/lmp -sf gpu -pk gpu 1 -in lmp_equiliv.in |& tee $LMPLOGFILE

python lmp2data.py 'equiliv' |& tee $PYLOGFILE
