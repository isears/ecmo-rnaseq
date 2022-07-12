#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=32
#SBATCH --mem=12G
#SBATCH --time=3:00:00
#SBATCH --output ./logs/cutadaptqc-%j.log

rm -rf outputs/dartmouthpipeline/cutadaptqc_results/*
fastqc -t 32 -o outputs/dartmouthpipeline/cutadaptqc_results/ outputs/dartmouthpipeline/cutadapt_results/*.fastq.gz
cd outputs/dartmouthpipeline/cutadaptqc_results
multiqc .