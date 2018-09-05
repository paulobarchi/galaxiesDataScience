#!/bin/bash
#SBATCH -J copyK10figs
#SBATCH --partition=defq
#SBATCH -N 1 # request at least 2 nodes
#SBATCH --ntasks-per-node=40

# Work directory
workdir="${HOME}/saveImgs"

# Full path to application + application name
application="$workdir/copyK10figs.py"

# change the working directory (default is home directory)
cd $workdir
echo Running on host $(hostname)
echo Time is $(date)
echo Directory is $(pwd)
echo Slurm job ID is $SLURM_JOB_ID
echo This job runs on the following machines:
echo $SLURM_JOB_NODELIST

p=0
# actual runs
for i in {00..39}; do
	python $application k10_3classes_$i.csv 670k_catalog_divided/part$i.csv $i &
	((p++))
	if ((p==nproc)); then
		wait # until free the processing units
		p=0
	fi
done
wait
