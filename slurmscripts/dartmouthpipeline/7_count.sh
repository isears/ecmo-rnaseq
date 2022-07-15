#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=32
#SBATCH --mem=40G
#SBATCH --time=2:00:00
#SBATCH --output ./logs/count-%j.log


rm -rf outputs/dartmouthpipeline/count_results/*
cd outputs/dartmouthpipeline/count_results

featureCounts \
    -p \
    -t exon \
    -g gene_id \
    -Q 20 \
    -T 32 \
    -s 0 \
    -a /gpfs/data/shared/databases/refchef_refs/grch38_release98/gtf/Homo_sapiens.GRCh38.98.gtf \
    -o ./all_counts.txt \
    ../star_results/*_Aligned.sortedByCoord.out.bam

echo "[+] Counting completed"