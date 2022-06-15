#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=32
#SBATCH --mem=32G
#SBATCH --time=7:00:00
#SBATCH --output /gpfs/home/isears1/Repos/ecmo-rnaseq/logs/subread-%j.log

module load subread
featureCounts -v

for dirname in /gpfs/scratch/isears1/rnaseq_outputs/subread/*-0*; do
    id=`echo $dirname | cut -d'/' -f7`
    echo "Handling " $id

    # -p for paired-end reads
    # -Q minimum quality score
    featureCounts \
        -p \
        -t exon \
        -g gene_id \
        -Q 20 \
        -T 32 \
        -a /gpfs/data/shared/databases/refchef_refs/grch38_release98/gtf/Homo_sapiens.GRCh38.98.gtf \
        -o /gpfs/scratch/isears1/rnaseq_outputs/subread/$id/counts.txt \
        /gpfs/scratch/isears1/rnaseq_outputs/subread/$id/alignment.bam

done

echo '[+] Feature counts completed'