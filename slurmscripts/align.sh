#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --time=10:00:00
#SBATCH --output ./logs/alignment-%j.log

cd /gpfs/data/ceickhof/ECMO_RNASeq/aligned

/users/isears1/Repos/STAR/source/STAR --version

r1_names=`ls /gpfs/data/ceickhof/ECMO_RNASeq/30-573159527/00_fastq/*R1_001.fastq.gz | paste -s -d,`
r2_names=`ls /gpfs/data/ceickhof/ECMO_RNASeq/30-573159527/00_fastq/*R2_001.fastq.gz | paste -s -d,`

/users/isears1/Repos/STAR/source/STAR \
    --runThreadN 32 \
    --genomeDir /gpfs/data/shared/databases/refchef_refs/grch38_release98/STAR_2_7_10a \
    --readFilesIn $r1_names $r2_names \
    --readFilesCommand "gunzip -c"
    / 

echo '[+] Alignment completed'
