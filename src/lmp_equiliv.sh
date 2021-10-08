#!/bin/bash

export CUDA_VISIBLE_DEVICES="0"
export OMPI_ALLOW_RUN_AS_ROOT=1

mpirun --allow-run-as-root -np 2 /program/lammps201029/build/lmp -sf gpu -pk gpu 1 -in lmp_equiliv.in > lmp_equiliv.log 2>&1

python lmp2data.py 'equiliv' >> lmp2data_equiliv.log 2>&1
