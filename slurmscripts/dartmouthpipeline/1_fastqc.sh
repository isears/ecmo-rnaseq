#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=32
#SBATCH --mem=12G
#SBATCH --time=10:00:00
#SBATCH --output ./logs/fastqc-%j.log

rm -rf outputs/dartmouthpipeline/fastqc_results/*
fastqc -t 32 -o outputs/dartmouthpipeline/fastqc_results/ data/30-573159527/00_fastq/*.fastq.gz