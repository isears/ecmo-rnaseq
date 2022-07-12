#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=32
#SBATCH --mem=8G
#SBATCH --time=5:00:00
#SBATCH --output ./logs/cutadapt-%j.log


rm -rf outputs/dartmouthpipeline/cutadapt_results/*
cd outputs/dartmouthpipeline/cutadapt_results

for fname in /gpfs/data/ceickhof/ECMO_RNASeq/30-573159527/00_fastq/*R1_001.fastq.gz; do
    id=`echo $fname | cut -d'/' -f8 | cut -d'.' -f 1 | cut -d'_' -f1`
    paired_fname=`echo $fname | cut -d'_' -f1,2,3`_R2_001.fastq.gz

    echo "Handling " $id
    echo "Read 1: " $fname
    echo "Read 2: " $paired_fname

    # Ref: https://support.illumina.com/bulletins/2016/12/what-sequences-do-i-use-for-adapter-trimming.html
    cutadapt \
    -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCA \
    -A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT \
    -m 20 \
    -q 20 \
    -j 32 \
    -o ./${id}_R1_001_trimmed.fastq.gz \
    -p ./${id}_R2_001_trimmed.fastq.gz \
    $fname \
    $paired_fname > ./${id}.cutadapt.report
done

echo "[+] Trimming complete"