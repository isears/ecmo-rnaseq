#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=32
#SBATCH --mem=32G
#SBATCH --time=6:00:00
#SBATCH --output /gpfs/home/isears1/Repos/ecmo-rnaseq/logs/subread-%j.log

module load subread
subread-align -v

for fname in /gpfs/data/ceickhof/ECMO_RNASeq/30-573159527/00_fastq/*R1_001.fastq.gz; do
    id=`echo $fname | cut -d'/' -f8 | cut -d'.' -f 1 | cut -d'_' -f1`
    echo "Handling " $id
    mkdir /gpfs/scratch/isears1/rnaseq_outputs/subread/$id
    paired_fname=`echo $fname | cut -d'_' -f1,2,3`_R2_001.fastq.gz

    echo "First input: " $fname
    echo "Second input: " $paired_fname

    # -t 0 for RNA-seq data
    # -T number of cores
    # -d minimum length
    subread-align \
        -i /gpfs/scratch/isears1/rnaseq_outputs/subread/grch38_release98 \
        -r $fname \
        -R $paired_fname \
        -t 0 \
        -o /gpfs/scratch/isears1/rnaseq_outputs/subread/$id/alignment.bam \
        -T 32 \
        -d 20 \
        -a /gpfs/data/shared/databases/refchef_refs/grch38_release98/gtf/Homo_sapiens.GRCh38.98.gtf

done

echo '[+] Alignment completed'
