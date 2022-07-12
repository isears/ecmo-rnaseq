#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=32
#SBATCH --mem=40G
#SBATCH --time=5:00:00
#SBATCH --output ./logs/align-%j.log


rm -rf outputs/dartmouthpipeline/star_results/*
cd outputs/dartmouthpipeline/star_results

STAR --version

for fname in /gpfs/scratch/isears1/rnaseq_outputs/dartmouthpipeline/cutadapt_results/*R1_001_trimmed.fastq.gz; do
    id=`echo $fname | cut -d '/' -f8 | cut -d'.' -f 1 | cut -d '_' -f1`
    paired_fname=`echo $fname | cut -d'_' -f1,2,3`_R2_001_trimmed.fastq.gz

    echo "Handling " $id
    echo "Read 1: " $fname
    echo "Read 2: " $paired_fname

    STAR \
    --genomeDir /gpfs/data/shared/databases/refchef_refs/grch38_release98/STAR_2_7_10a \
    --readFilesIn $fname $paired_fname \
    --readFilesCommand zcat \
    --sjdbGTFfile /gpfs/data/shared/databases/refchef_refs/grch38_release98/gtf/Homo_sapiens.GRCh38.98.gtf \
    --runThreadN 32 \
    --outSAMtype BAM Unsorted SortedByCoordinate \
    --outFilterType BySJout \
    --outFileNamePrefix ./${id}_
done

echo "[+] Alignment complete"