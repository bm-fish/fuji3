#!/bin/sh
#SBATCH -J test
#SBATCH -p F1cpu
#SBATCH -N 1
#SBATCH -n 128
#SBATCH -c 1
#SBATCH --exclusive

# Option to use dual rail
#export MPI_IB_RAILS=2

#MKL_DEBUG_CPU_TYPE=5
ulimit -s unlimited
module purge
module load oneapi_compiler/2023.0.0 oneapi_mkl/2023.0.0 openmpi/4.1.5-oneapi-2023.0.0-classic
export KMP_STACKSIZE=512m
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/local/ap/hdf5-openmpi/1.10.10/lib
export UCX_TLS='self,sm,ud'

# standard version
# srun /home/issp/vasp/vasp6/vasp.6.4.1_hybrid/bin/vasp_std > stdout.log 2>&1 

# gamma-point only
srun /home/issp/vasp/vasp6/vasp.6.4.1_hybrid/bin/vasp_gam > stdout.log 2>&1

#srun /home/issp/vasp/vasp6/vasp.6.4.1_hybrid/bin/vasp_gam > stdout.log 2>&1 

# noncollinear
#srun /home/issp/vasp/vasp6/vasp.6.4.1_hybrid/bin/vasp_ncl > stdout.log 2>&1 

