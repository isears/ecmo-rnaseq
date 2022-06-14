#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=30
#SBATCH --mem=40G
#SBATCH --time=10:00:00
#SBATCH --output ./logs/alignment-%j.log

cd /gpfs/data/ceickhof/ECMO_RNASeq/aligned

/users/isears1/Repos/STAR/source/STAR --version

for fname in /gpfs/data/ceickhof/ECMO_RNASeq/30-573159527/00_fastq/*R1_001.fastq.gz; do
    id=`echo $fname | cut -d'/' -f8 | cut -d'.' -f 1 | cut -d'_' -f1`
    echo "Handling " $id
    mkdir /gpfs/data/ceickhof/ECMO_RNASeq/aligned_apart/$id
    cd /gpfs/data/ceickhof/ECMO_RNASeq/aligned_apart/$id
    paired_fname=`echo $fname | cut -d'_' -f1,2,3`_R2_001.fastq.gz

    /users/isears1/Repos/STAR/source/STAR \
        --runThreadN 30 \
        --genomeDir /gpfs/data/shared/databases/refchef_refs/grch38_release98/STAR_2_7_10a \
        --readFilesIn $fname $paired_fname \
        --readFilesCommand "gunzip -c"
        / 

done

echo '[+] Alignment completed'
