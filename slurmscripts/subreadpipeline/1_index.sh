#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=1
#SBATCH --mem=24G
#SBATCH --time=02:00:00
#SBATCH --output /gpfs/home/isears1/Repos/ecmo-rnaseq/logs/subread-%j.log

cd /gpfs/scratch/isears1/rnaseq_outputs/subread
module load subread
subread-buildindex -v
subread-buildindex -F -B -o grch38_release98 /gpfs/data/shared/databases/refchef_refs/grch38_release98/primary/Homo_sapiens.GRCh38.dna.primary_assembly.fa

echo '[+] Build Index completed'