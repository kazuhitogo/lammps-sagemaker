#!/bin/bash
#PBS -q APG
#PBS -N title
#PBS -l select=1:ncpus=2:mpiprocs=2:ngpus=1


wget https://raw.githubusercontent.com/lammps/lammps/master/examples/melt/in.melt
export OMP_NUM_THREADS=1
lmp -sf gpu -pk gpu 1 -in in.melt