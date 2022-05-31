#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --time=6:00:00
#SBATCH --output ./logs/alignment-%j.log

module load python/3.7.4

export PYTHONUNBUFFERED=TRUE
export PYTHONPATH=./:$PYTHONPATH

cd ~/Repos/ecmo-rnaseq

# Do something here

echo 'slurmscript completed'