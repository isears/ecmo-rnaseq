#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G
#SBATCH --time=1:00:00
#SBATCH --output ./logs/alignment-%j.log

module load python/3.7.4

export PYTHONUNBUFFERED=TRUE
export PYTHONPATH=./:$PYTHONPATH

cd ~/Repos/ecmo-rnaseq/StarRunDir

/users/isears1/Repos/STAR/source/STAR --version
/users/isears1/Repos/STAR/source/STAR --runThreadN 2 --genomeDir /gpfs/data/shared/databases/refchef_refs/grch38_release98/STAR_2_7_10a --readFilesIn ../sampledata/sample.fastq

echo 'Alignment completed'