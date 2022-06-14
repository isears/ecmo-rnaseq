#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=24:00:00
#SBATCH --output ./logs/qual_report-%j.log

export PYTHONUNBUFFERED=TRUE
source ~/VirtualEnvironments/rnaseq/bin/activate

cd /users/isears1/scratch/rnaseq_outputs/qual_report

python -m HTSeq.scripts.qa ~/Repos/ecmo-rnaseq/data/aligned/Aligned.out.sam

echo 'Done'